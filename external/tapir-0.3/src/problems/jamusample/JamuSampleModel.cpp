/** @file JamuSampleModel.cpp
 *
 * Contains the implementations for the core functionality of the JamuSample POMDP.
 */
#include "JamuSampleModel.hpp"

#include <cmath>                        // for pow, floor
#include <cstddef>                      // for size_t
#include <cstdlib>                      // for exit

#include <fstream>                      // for operator<<, basic_ostream, endl, basic_ostream<>::__ostream_type, ifstream, basic_ostream::operator<<, basic_istream, basic_istream<>::__istream_type
#include <initializer_list>
#include <iostream>                     // for cout
#include <queue>
#include <map>
#include <memory>                       // for unique_ptr, default_delete
#include <random>                       // for uniform_int_distribution, bernoulli_distribution
#include <set>                          // for set, _Rb_tree_const_iterator, set<>::iterator
#include <string>                       // for string, getline, char_traits, basic_string
#include <tuple>                        // for tie, tuple
#include <unordered_map>                // for unordered_map<>::value_type, unordered_map
#include <utility>                      // for move, pair, make_pair
#include <vector>                       // for vector, vector<>::reference, __alloc_traits<>::value_type, operator==

#include "global.hpp"                     // for RandomGenerator, make_unique

#include "problems/shared/GridPosition.hpp"  // for GridPosition, operator<<
#include "problems/shared/ModelWithProgramOptions.hpp"  // for ModelWithProgramOptions

#include "solver/abstract-problem/Action.hpp"            // for Action
#include "solver/abstract-problem/Model.hpp"             // for Model::StepResult, Model
#include "solver/abstract-problem/Observation.hpp"       // for Observation
#include "solver/abstract-problem/State.hpp"       // for State

#include "solver/indexing/RTree.hpp"
#include "solver/indexing/FlaggingVisitor.hpp"

#include "solver/mappings/actions/ActionMapping.hpp"
#include "solver/mappings/actions/enumerated_actions.hpp"
#include "solver/mappings/observations/enumerated_observations.hpp"

#include "solver/changes/ChangeFlags.hpp"        // for ChangeFlags

#include "solver/ActionNode.hpp"
#include "solver/BeliefNode.hpp"
#include "solver/StatePool.hpp"

#include "position_history.hpp"
#include "smart_history.hpp"
#include "LegalActionsPool.hpp"
#include "PreferredActionsPool.hpp"
#include "JamuSampleAction.hpp"         // for JamuSampleAction
#include "JamuSampleMdpSolver.hpp"
#include "JamuSampleObservation.hpp"    // for JamuSampleObservation
#include "JamuSampleOptions.hpp"
#include "JamuSampleState.hpp"          // for JamuSampleState
#include "JamuSampleTextSerializer.hpp"

using std::cout;
using std::endl;

namespace jamusample {
JamuSampleModel::JamuSampleModel(RandomGenerator *randGen, std::unique_ptr<JamuSampleOptions> options) :
            shared::ModelWithProgramOptions("JamuSample", randGen, std::move(options)),
            options_(const_cast<JamuSampleOptions *>(static_cast<JamuSampleOptions const *>(getOptions()))),
            goodJamuReward_(options_->goodJamuReward),
            badJamuPenalty_(options_->badJamuPenalty),
            exitReward_(options_->exitReward),
            illegalMovePenalty_(options_->illegalMovePenalty),
            halfEfficiencyDistance_(options_->halfEfficiencyDistance),
            nRows_(0), // update
            nCols_(0), // update
            nJamus_(0), // update
            startPos_(), // update
            jamuPositions_(), // push jamus
            goalPositions_(), // push goals
            mapText_(), // push rows
            envMap_(), // push rows
            goalDistances_(), // calculate distances
            jamuDistances_(), // calculate distances
            heuristicType_(parseCategory(options_->heuristicType)),
            searchCategory_(parseCategory(options_->searchHeuristicType)),
            rolloutCategory_(parseCategory(options_->rolloutHeuristicType)),
            usingPreferredInit_(options_->usePreferredInit),
            preferredQValue_(options_->preferredQValue),
            preferredVisitCount_(options_->preferredVisitCount),
            mdpSolver_(nullptr) {

    if (searchCategory_ > heuristicType_) {
        searchCategory_ = heuristicType_;
    }
    if (rolloutCategory_ > heuristicType_) {
        rolloutCategory_ = heuristicType_;
    }

    registerHeuristicParser("exactMdp", std::make_unique<JamuSampleMdpParser>(this));

    // Read the map from the file.
    std::ifstream inFile;
    inFile.open(options_->mapPath);
    if (!inFile.is_open()) {
        std::ostringstream message;
        message << "Failed to open " << options_->mapPath;
        debug::show_message(message.str());
        std::exit(1);
    }
    inFile >> nRows_ >> nCols_;
    std::string tmp;
    getline(inFile, tmp);
    for (long i = 0; i < nRows_; i++) {
        getline(inFile, tmp);
        mapText_.push_back(tmp);
    }
    inFile.close();

    initialize();
    if (options_->hasVerboseOutput) {
        cout << "Constructed the JamuSampleModel" << endl;
        cout << "Discount: " << options_->discountFactor << endl;
        cout << "Size: " << nRows_ << " by " << nCols_ << endl;
        cout << "nJamus: " << nJamus_ << endl;

        cout << "Environment:" << endl;
        drawEnv(cout);
        cout << endl;
    }
}

void JamuSampleModel::initialize() {
    nJamus_ = 0;
    GridPosition p;
    for (p.i = 0; p.i < nRows_; p.i++) {
        envMap_.emplace_back();
        for (p.j = 0; p.j < nCols_; p.j++) {
            char c = mapText_[p.i][p.j];
            RSCellType cellType;
            if (c == 'o') {
                jamuPositions_.push_back(p);
                cellType = (RSCellType) (JAMU + nJamus_);
                nJamus_++;
            } else if (c == 'G') {
                cellType = GOAL;
                goalPositions_.push_back(p);
            } else if (c == 'S') {
                startPos_ = p;
                cellType = EMPTY;
            } else if (c == 'X') {
                cellType = OBSTACLE;
            } else {
                cellType = EMPTY;
            }
            envMap_.back().push_back(cellType);
        }
    }

    options_->numberOfStateVariables = 2 + nJamus_;
    options_->minVal = -illegalMovePenalty_ / (1 - options_->discountFactor);
    options_->minVal = goodJamuReward_ * nJamus_ + exitReward_;

    goalDistances_.resize(nRows_);
    for (std::vector<int> &row : goalDistances_) {
        row.resize(nCols_);
    }

    jamuDistances_.resize(nJamus_);
    for (auto &distances : jamuDistances_) {
        distances.resize(nRows_);
        for (auto &row : distances) {
            row.resize(nCols_);
        }
    }

    recalculateAllDistances();

    if (getDistance(startPos_, -1) == -1){
        cout << "ERROR: Unreachable goal!";
        std::exit(10);
    }
}

void JamuSampleModel::recalculateAllDistances() {
    std::vector<GridPosition> realGoalPositions;
    for (GridPosition const &pos : goalPositions_) {
        if (envMap_[pos.i][pos.j] != OBSTACLE) {
            realGoalPositions.push_back(pos);
        }
    }
    recalculateDistances(goalDistances_, realGoalPositions);
    for (int jamuNo = 0; jamuNo < nJamus_; jamuNo++) {
        recalculateDistances(jamuDistances_[jamuNo],
                std::vector<GridPosition> {jamuPositions_[jamuNo]});
    }
}

void JamuSampleModel::recalculateDistances(std::vector<std::vector<int>> &grid,
        std::vector<GridPosition> targets) {
    // Preinitialize to -1 for all cells.
    for (auto &row : grid) {
        for (auto &cell : row) {
            cell = -1;
        }
    }
    std::queue<GridPosition> queue;
    for (GridPosition &pos : targets) {
        grid[pos.i][pos.j] = 0;
        queue.push(pos);
    }

    while (!queue.empty()) {
        GridPosition pos = queue.front();
        queue.pop();
        int distance = grid[pos.i][pos.j] + 1;
        for (ActionType direction : {ActionType::NORTH, ActionType::SOUTH, ActionType::WEST,
            ActionType::EAST}) {
            GridPosition nextPos;
            bool isLegal;
            std::tie(nextPos, isLegal) = makeNextPosition(pos, direction);
            // The distance matters only if the move is legal, and doesn't move into a goal.
            if (isLegal && getCellType(nextPos) != GOAL) {
                int &nextPosDistance = grid[nextPos.i][nextPos.j];
                if (nextPosDistance == -1 || nextPosDistance > distance) {
                    nextPosDistance = distance;
                    queue.push(nextPos);
                }
            }
        }
    }
}


/* --------------- The model interface proper ----------------- */
std::unique_ptr<solver::State> JamuSampleModel::sampleAnInitState() {
    return std::make_unique<JamuSampleState>(startPos_, sampleJamus());
//    return std::make_unique<JamuSampleState>(startPos_, std::vector<bool> {
//        true, false, true, false, false, false, false, false
//    });
}

std::unique_ptr<solver::State> JamuSampleModel::sampleStateUninformed() {
    while (true) {
        GridPosition position = samplePosition();
        // States that are on top of an obstacle are completely invalid.
        if (getCellType(position) != OBSTACLE) {
            return std::make_unique<JamuSampleState>(position, sampleJamus());
        }
    }
    return nullptr;
}

GridPosition JamuSampleModel::samplePosition() {
    long i = std::uniform_int_distribution<long>(0, nRows_ - 1)(*getRandomGenerator());
    long j = std::uniform_int_distribution<long>(0, nCols_ - 1)(*getRandomGenerator());
    return GridPosition(i, j);
}

std::vector<bool> JamuSampleModel::sampleJamus() {
    return decodeJamus(
            std::uniform_int_distribution<long>(0, (1 << nJamus_) - 1)(*getRandomGenerator()));
}

std::vector<bool> JamuSampleModel::decodeJamus(long val) {
    std::vector<bool> jamuStates;
    for (int j = 0; j < nJamus_; j++) {
        jamuStates.push_back(val & (1 << j));
    }
    return jamuStates;
}

long JamuSampleModel::encodeJamus(std::vector<bool> jamuStates) {
    long value = 0;
    for (int j = 0; j < nJamus_; j++) {
        if (jamuStates[j]) {
            value += (1 << j);
        }
    }
    return value;
}

bool JamuSampleModel::isTerminal(solver::State const &state) {
    JamuSampleState const &jamuSampleState = static_cast<JamuSampleState const &>(state);
    GridPosition pos = jamuSampleState.getPosition();
    return getCellType(pos) == GOAL;
}

bool JamuSampleModel::isValid(solver::State const &state) {
    JamuSampleState const &jamuSampleState = static_cast<JamuSampleState const &>(state);
    return isValid(jamuSampleState.getPosition());
}

bool JamuSampleModel::isValid(GridPosition position) {
    return (position.i >= 0 && position.i < nRows_ && position.j >= 0 && position.j < nCols_
            && getCellType(position) != RSCellType::OBSTACLE);
}

GridPosition JamuSampleModel::makeAdjacentPosition(GridPosition position, ActionType actionType) {
    if (actionType == ActionType::NORTH) {
        position.i -= 1;
    } else if (actionType == ActionType::EAST) {
        position.j += 1;
    } else if (actionType == ActionType::SOUTH) {
        position.i += 1;
    } else if (actionType == ActionType::WEST) {
        position.j -= 1;
    }
    return position;
}

std::pair<GridPosition, bool> JamuSampleModel::makeNextPosition(GridPosition position,
        ActionType actionType) {

    GridPosition oldPosition = position;

    bool isLegal = true;
    if (actionType == ActionType::CHECK) {
        // Do nothing - the state remains the same.
    } else if (actionType == ActionType::SAMPLE) {
        int jamuNo = getCellType(position) - JAMU;
        if (jamuNo < 0 || jamuNo >= nJamus_) {
            isLegal = false;
        }
    } else {
        position = makeAdjacentPosition(position, actionType);
        if (!isValid(position)) {
            position = oldPosition;
            isLegal = false;
        }
    }
    return std::make_pair(position, isLegal);
}

/* -------------------- Black box dynamics ---------------------- */
std::pair<std::unique_ptr<JamuSampleState>, bool> JamuSampleModel::makeNextState(
        JamuSampleState const &state, JamuSampleAction const &action) {

    GridPosition nextPos;
    bool isLegal;
    std::tie(nextPos, isLegal) = makeNextPosition(state.getPosition(), action.getActionType());
    if (!isLegal) {
        return std::make_pair(std::make_unique<JamuSampleState>(state), false);
    }

    std::vector<bool> jamuStates(state.getJamuStates());
    ActionType actionType = action.getActionType();
    if (actionType == ActionType::SAMPLE) {
        int jamuNo = getCellType(nextPos) - JAMU;
        jamuStates[jamuNo] = false;
    }

    return std::make_pair(std::make_unique<JamuSampleState>(nextPos, jamuStates), true);
}

std::unique_ptr<JamuSampleObservation> JamuSampleModel::makeObservation(
        JamuSampleAction const &action, JamuSampleState const &nextState) {
    ActionType actionType = action.getActionType();
    if (actionType < ActionType::CHECK) {
        return std::make_unique<JamuSampleObservation>();
    }
    long jamuNo = action.getJamuNo();
    GridPosition pos(nextState.getPosition());
    std::vector<bool> jamuStates(nextState.getJamuStates());
    double dist = pos.euclideanDistanceTo(jamuPositions_[jamuNo]);
    bool obsMatches = std::bernoulli_distribution(getSensorCorrectnessProbability(dist))(
            *getRandomGenerator());
    return std::make_unique<JamuSampleObservation>(jamuStates[jamuNo] == obsMatches);
}

double JamuSampleModel::makeReward(JamuSampleState const &state, JamuSampleAction const &action,
        JamuSampleState const &nextState, bool isLegal) {
    if (!isLegal) {
        return -illegalMovePenalty_;
    }
    if (isTerminal(nextState)) {
        return exitReward_;
    }

    ActionType actionType = action.getActionType();
    if (actionType == ActionType::SAMPLE) {
        GridPosition pos = state.getPosition();
        int jamuNo = getCellType(pos) - JAMU;
        if (0 <= jamuNo && jamuNo < nJamus_) {
            return state.getJamuStates()[jamuNo] ? goodJamuReward_ : -badJamuPenalty_;
        } else {
            debug::show_message("Invalid sample action!?!");
            return -illegalMovePenalty_;
        }
    }
    return 0;
}

std::unique_ptr<solver::State> JamuSampleModel::generateNextState(solver::State const &state,
        solver::Action const &action, solver::TransitionParameters const * /*tp*/) {
    return makeNextState(static_cast<JamuSampleState const &>(state),
            static_cast<JamuSampleAction const &>(action)).first;
}

std::unique_ptr<solver::Observation> JamuSampleModel::generateObservation(
        solver::State const * /*state*/, solver::Action const &action,
        solver::TransitionParameters const * /*tp*/, solver::State const &nextState) {
    return makeObservation(static_cast<JamuSampleAction const &>(action),
            static_cast<JamuSampleState const &>(nextState));
}

double JamuSampleModel::generateReward(solver::State const &state, solver::Action const &action,
        solver::TransitionParameters const * /*tp*/, solver::State const * /*nextState*/) {
    JamuSampleState const &jamuSampleState = (static_cast<JamuSampleState const &>(state));
    JamuSampleAction const &jamuSampleAction = (static_cast<JamuSampleAction const &>(action));
    std::unique_ptr<JamuSampleState> nextState;
    bool isLegal;
    std::tie(nextState, isLegal) = makeNextState(jamuSampleState, jamuSampleAction);
    return makeReward(jamuSampleState, jamuSampleAction, *nextState, isLegal);
}

solver::Model::StepResult JamuSampleModel::generateStep(solver::State const &state,
        solver::Action const &action) {
    JamuSampleState const &jamuSampleState = static_cast<JamuSampleState const &>(state);
    JamuSampleAction const &jamuSampleAction = (static_cast<JamuSampleAction const &>(action));
    solver::Model::StepResult result;
    result.action = action.copy();

    bool isLegal;
    std::unique_ptr<JamuSampleState> nextState;
    std::tie(nextState, isLegal) = makeNextState(jamuSampleState, jamuSampleAction);
    result.observation = makeObservation(jamuSampleAction, *nextState);
    result.reward = makeReward(jamuSampleState, jamuSampleAction, *nextState, isLegal);
    result.isTerminal = isTerminal(*nextState);
    result.nextState = std::move(nextState);
    return result;
}

/* -------------- Methods for handling model changes ---------------- */
void JamuSampleModel::applyChanges(std::vector<std::unique_ptr<solver::ModelChange>> const &changes,
            solver::Solver *solver) {
    solver::StatePool *pool = nullptr;
    if (solver != nullptr) {
        pool = solver->getStatePool();
    }

    if (options_->hasVerboseOutput && pool != nullptr)  {
        cout << "Applying model changes..." << endl;
    }

    solver::HeuristicFunction heuristic = getHeuristicFunction();
    std::vector<double> allHeuristicValues;
    if (pool != nullptr) {
        long nStates = pool->getNumberOfStates();
        allHeuristicValues.resize(nStates);
        for (long index = 0; index < nStates; index++) {
            allHeuristicValues[index] = heuristic(nullptr, pool->getInfoById(index)->getState(),
                    nullptr);
        }
    }

    // The cells that have been affected by these changes.
    std::unordered_set<GridPosition> affectedCells;

    for (auto const &change : changes) {
        JamuSampleChange const &rsChange = static_cast<JamuSampleChange const &>(*change);
        if (options_->hasVerboseOutput) {
            cout << rsChange.changeType << " " << rsChange.i0 << " "
                    << rsChange.j0;
            cout << " " << rsChange.i1 << " " << rsChange.j1 << endl;
        }

        RSCellType newCellType;
        if (rsChange.changeType == "Add Obstacles") {
            newCellType = OBSTACLE;
        } else if (rsChange.changeType == "Remove Obstacles") {
            newCellType = EMPTY;
        } else {
            cout << "Invalid change type: " << rsChange.changeType;
            continue;
        }

        for (long i = rsChange.i0; i <= rsChange.i1; i++) {
            for (long j = rsChange.j0; j <= rsChange.j1; j++) {
                RSCellType oldCellType = envMap_[i][j];
                envMap_[i][j] = newCellType;
                if (newCellType != oldCellType) {
                    affectedCells.insert(GridPosition(i, j));
                }
            }
        }

        for (GridPosition const &pos : goalPositions_) {
            if (envMap_[pos.i][pos.j] != OBSTACLE) {
                envMap_[pos.i][pos.j] = GOAL;
            }
        }

        if (pool == nullptr) {
            continue;
        }

        if (searchCategory_ == RSActionCategory::LEGAL && newCellType == RSCellType::EMPTY) {
            // Legal actions + newly empty cells => handled automatically.
        }

        // If we're adding obstacles, we need to mark the invalid states as deleted.
        solver::RTree *tree = static_cast<solver::RTree *>(pool->getStateIndex());

        std::vector<double> lowCorner;
        std::vector<double> highCorner;
        for (int i = 0; i < nJamus_+2; i++) {
            lowCorner.push_back(0.0);
            highCorner.push_back(1.0);
        }
        lowCorner[0] = rsChange.i0;
        lowCorner[1] = rsChange.j0;
        highCorner[0] = rsChange.i1;
        highCorner[1] = rsChange.j1;


        solver::ChangeFlags flags = solver::ChangeFlags::DELETED;
        if (newCellType == RSCellType::EMPTY) {
            flags = solver::ChangeFlags::TRANSITION;
            lowCorner[0] -= 1;
            lowCorner[1] -= 1;
            highCorner[0] += 1;
            highCorner[1] += 1;
        }

        solver::FlaggingVisitor visitor(pool, flags);
        tree->boxQuery(visitor, lowCorner, highCorner);
    }

    // Only modify actions if we're working with a legal-only search.
    if (solver != nullptr && searchCategory_ == RSActionCategory::LEGAL) {
        LegalActionsPool *actionPool = static_cast<LegalActionsPool *>(solver->getActionPool());
        for (GridPosition cell : affectedCells) {
            bool isLegal = (envMap_[cell.i][cell.j] != OBSTACLE);
            ActionType actionPairs[4][2] = {
                    {ActionType::NORTH, ActionType::SOUTH},
                    {ActionType::EAST, ActionType::WEST},
                    {ActionType::SOUTH, ActionType::NORTH},
                    {ActionType::WEST, ActionType::EAST}
            };

            for (auto &pair : actionPairs) {
                GridPosition adjacentCell = makeAdjacentPosition(cell, pair[0]);
                // Ignore cells that are out of bounds.
                if (!isWithinBounds(adjacentCell)) {
                    continue;
                }
                actionPool->setLegal(isLegal, adjacentCell, JamuSampleAction(pair[1]), solver);
            }
        }
    }

    // Recalculate all the distances.
    recalculateAllDistances();

    if (mdpSolver_ != nullptr) {
        mdpSolver_->solve();
    }

    // Check for heuristic changes.
    if (pool != nullptr) {
        long nStates = pool->getNumberOfStates();
        for (long index = 0; index < nStates; index++) {
            double oldValue = allHeuristicValues[index];
            solver::StateInfo *info = pool->getInfoById(index);
            double newValue = heuristic(nullptr, info->getState(), nullptr);
            if (std::abs(newValue - oldValue) > 1e-5) {
                pool->setChangeFlags(info, solver::ChangeFlags::HEURISTIC);
            }
        }
    }

    if (options_->hasVerboseOutput && pool != nullptr) {
        cout << "Done applying model changes..." << endl;
    }
}


/* ------------ Methods for handling particle depletion -------------- */
std::vector<std::unique_ptr<solver::State>> JamuSampleModel::generateParticles(
        solver::BeliefNode * /*previousBelief*/, solver::Action const &action,
        solver::Observation const &obs, long nParticles,
        std::vector<solver::State const *> const &previousParticles) {
    std::vector<std::unique_ptr<solver::State>> newParticles;

    JamuSampleAction const &a = static_cast<JamuSampleAction const &>(action);
    if (a.getActionType() == ActionType::CHECK) {
        long jamuNo = a.getJamuNo();
        typedef std::unordered_map<JamuSampleState, double> WeightMap;
        WeightMap weights;
        double weightTotal = 0;
        for (solver::State const *state : previousParticles) {
            JamuSampleState const *jamuSampleState = static_cast<JamuSampleState const *>(state);
            GridPosition pos(jamuSampleState->getPosition());
            double dist = pos.euclideanDistanceTo(jamuPositions_[jamuNo]);
            bool jamuIsGood = jamuSampleState->getJamuStates()[jamuNo];

            double probability = getSensorCorrectnessProbability(dist);
            JamuSampleObservation const &observation =
                    (static_cast<JamuSampleObservation const &>(obs));
            if (jamuIsGood != observation.isGood()) {
                probability = 1 - probability;
            }
            weights[*jamuSampleState] += probability;
            weightTotal += probability;
        }
        double scale = nParticles / weightTotal;
        for (WeightMap::value_type &it : weights) {
            double proportion = it.second * scale;
            long numToAdd = static_cast<long>(proportion);
            if (std::bernoulli_distribution(proportion - numToAdd)(*getRandomGenerator())) {
                numToAdd += 1;
            }
            for (int i = 0; i < numToAdd; i++) {
                newParticles.push_back(std::make_unique<JamuSampleState>(it.first));
            }
        }

    } else {
        // It's not a CHECK action, so we just add each resultant state.
        for (solver::State const *state : previousParticles) {
            JamuSampleState const *jamuSampleState = (static_cast<JamuSampleState const *>(state));
            JamuSampleAction const &jamuSampleAction =
                    (static_cast<JamuSampleAction const &>(action));
            newParticles.push_back(makeNextState(*jamuSampleState, jamuSampleAction).first);
        }
    }
    return newParticles;
}

std::vector<std::unique_ptr<solver::State>> JamuSampleModel::generateParticles(
        solver::BeliefNode *previousBelief, solver::Action const &action,
        solver::Observation const &obs, long nParticles) {
    // Retrieve the fully observed part of the state.
    GridPosition oldPosition = static_cast<JamuSampleState const &>(
            *previousBelief->getStates()[0]).getPosition();

    std::vector<std::unique_ptr<solver::State>> particles;
    while ((long) particles.size() < nParticles) {
        JamuSampleState oldState(oldPosition, sampleJamus());
        solver::Model::StepResult result = generateStep(oldState, action);
        if (obs == *result.observation) {
            particles.push_back(std::move(result.nextState));
        }
    }
    return particles;
}

/* ------------------- Pretty printing methods --------------------- */
void JamuSampleModel::dispCell(RSCellType cellType, std::ostream &os) {
    if (cellType >= JAMU) {
        os << std::hex << cellType - JAMU;
        os << std::dec;
        return;
    }
    switch (cellType) {
    case EMPTY:
        os << '.';
        break;
    case GOAL:
        os << 'G';
        break;
    case OBSTACLE:
        os << 'X';
        break;
    default:
        os << "ERROR-" << cellType;
        break;
    }
}

void JamuSampleModel::drawEnv(std::ostream &os) {
    for (std::vector<RSCellType> &row : envMap_) {
        for (RSCellType cellValue : row) {
            dispCell(cellValue, os);
        }
        os << endl;
    }
}

void JamuSampleModel::drawDistances(std::vector<std::vector<int>> &grid, std::ostream &os) {
    for (auto &row : grid) {
        for (int cellValue : row) {
            if (cellValue == -1) {
                os << ".";
            } else {
                os << std::hex << cellValue;
            }
        }
        os << endl;
    }
}

void JamuSampleModel::drawSimulationState(solver::BeliefNode const *belief,
        solver::State const &state, std::ostream &os) {
    JamuSampleState const &jamuSampleState = static_cast<JamuSampleState const &>(state);
    std::vector<solver::State const *> particles = belief->getStates();
    GridPosition pos(jamuSampleState.getPosition());
    std::vector<double> goodProportions(nJamus_);
    for (solver::State const *particle : particles) {
        JamuSampleState const &rss = static_cast<JamuSampleState const &>(*particle);
        for (long i = 0; i < nJamus_; i++) {
            if (rss.getJamuStates()[i]) {
                goodProportions[i] += 1;
            }
        }
    }
    for (long i = 0; i < nJamus_; i++) {
        goodProportions[i] /= particles.size();
    }

    std::vector<int> colors { 196, 161, 126, 91, 56, 21, 26, 31, 36, 41, 46 };
    if (options_->hasColorOutput) {
        os << "Color map: ";
        for (int color : colors) {
            os << "\033[38;5;" << color << "m";
            os << '*';
            os << "\033[0m";
        }
        os << endl;
    }
    for (std::size_t i = 0; i < envMap_.size(); i++) {
        for (std::size_t j = 0; j < envMap_[0].size(); j++) {
            long jamuNo = envMap_[i][j] - JAMU;
            if (jamuNo >= 0 && options_->hasColorOutput) {
                int color = colors[goodProportions[jamuNo] * (colors.size() - 1)];
                os << "\033[38;5;" << color << "m";
            }
            if ((long) i == pos.i && (long) j == pos.j) {
                os << "r";
            } else {
                dispCell(envMap_[i][j], os);
            }
            if (jamuNo >= 0 && options_->hasColorOutput) {
                os << "\033[0m";
            }
        }
        os << endl;
    }
    for (double p : goodProportions) {
        os << p << " ";
    }
    os << endl;
}

/* ---------------------- Basic customizations  ---------------------- */
double JamuSampleModel::getDefaultHeuristicValue(solver::HistoryEntry const * /*entry*/,
        solver::State const *state, solver::HistoricalData const * /*data*/) {
    JamuSampleState const &jamuSampleState = static_cast<JamuSampleState const &>(*state);
    double qVal = 0;
    double currentDiscount = 1;
    GridPosition currentPos(jamuSampleState.getPosition());
    std::vector<bool> jamuStates(jamuSampleState.getJamuStates());

    std::set<int> goodJamus;
    for (int i = 0; i < nJamus_; i++) {
        // Only bother with reachable jamus.
        if (jamuStates[i] && getDistance(currentPos, i) != -1) {
            goodJamus.insert(i);
        }
    }

    // Visit the jamus in a greedy order.
    while (!goodJamus.empty()) {
        std::set<int>::iterator it = goodJamus.begin();
        int bestJamu = *it;
        long lowestDist = getDistance(currentPos, bestJamu);
        ++it;
        for (; it != goodJamus.end(); ++it) {
            long dist = getDistance(currentPos, *it);
            if (dist < lowestDist) {
                bestJamu = *it;
                lowestDist = dist;
            }
        }
        currentDiscount *= std::pow(options_->discountFactor, lowestDist);
        qVal += currentDiscount * goodJamuReward_;
        goodJamus.erase(bestJamu);
        currentPos = jamuPositions_[bestJamu];
    }

    // Now move to a goal square.
    currentDiscount *= std::pow(options_->discountFactor, getDistance(currentPos, -1));
    qVal += currentDiscount * exitReward_;
    return qVal;
}

std::unique_ptr<JamuSampleAction> JamuSampleModel::getRandomAction() {
    long binNumber = std::uniform_int_distribution<int>(0, 4 + nJamus_)(*getRandomGenerator());
    return std::make_unique<JamuSampleAction>(binNumber);
}
std::unique_ptr<JamuSampleAction> JamuSampleModel::getRandomAction(std::vector<long> binNumbers) {
    if (binNumbers.empty()) {
        return nullptr;
    }
    long index = std::uniform_int_distribution<int>(0, binNumbers.size() - 1)(
            *getRandomGenerator());
    return std::make_unique<JamuSampleAction>(binNumbers[index]);
}

std::unique_ptr<solver::Action> JamuSampleModel::getRolloutAction(
        solver::HistoryEntry const * /*entry*/, solver::State const * /*state*/,
        solver::HistoricalData const *data) {
    if (rolloutCategory_ == RSActionCategory::ALL) {
        return getRandomAction();
    } else if (rolloutCategory_ == RSActionCategory::LEGAL) {
        if (heuristicType_ == RSActionCategory::LEGAL) {
            return getRandomAction(static_cast<PositionData const &>(*data).generateLegalActions());
        } else if (heuristicType_ == RSActionCategory::PREFERRED) {
            return getRandomAction(
                    static_cast<PositionAndJamuData const &>(*data).generateLegalActions());
        }
    } else {
        return getRandomAction(
                static_cast<PositionAndJamuData const &>(*data).generatePreferredActions());
    }
    return nullptr;
}

/* ------- Customization of more complex solver functionality  --------- */
std::vector<std::unique_ptr<solver::DiscretizedPoint>> JamuSampleModel::getAllActionsInOrder() {
    std::vector<std::unique_ptr<solver::DiscretizedPoint>> allActions;
    for (long code = 0; code < 5 + nJamus_; code++) {
        allActions.push_back(std::make_unique<JamuSampleAction>(code));
    }
    return std::move(allActions);
}

std::unique_ptr<solver::ActionPool> JamuSampleModel::createActionPool(solver::Solver * /*solver*/) {
    switch (heuristicType_) {
    case RSActionCategory::LEGAL:
        return std::make_unique<LegalActionsPool>(this);
    case RSActionCategory::PREFERRED:
        return std::make_unique<PreferredActionsPool>(this);
    default:
        return std::make_unique<solver::EnumeratedActionPool>(this, getAllActionsInOrder());
    }
}
std::unique_ptr<solver::HistoricalData> JamuSampleModel::createRootHistoricalData() {
    switch (heuristicType_) {
    case RSActionCategory::LEGAL:
        return std::make_unique<PositionData>(this, getStartPosition());
    case RSActionCategory::PREFERRED:
        return std::make_unique<PositionAndJamuData>(this, getStartPosition());
    default:
        return nullptr;
    }
}

std::vector<std::unique_ptr<solver::DiscretizedPoint>> JamuSampleModel::getAllObservationsInOrder() {
    std::vector<std::unique_ptr<solver::DiscretizedPoint>> allObservations_;
    for (long code = 0; code < 3; code++) {
        allObservations_.push_back(std::make_unique<JamuSampleObservation>(code));
    }
    return allObservations_;
}
std::unique_ptr<solver::ObservationPool> JamuSampleModel::createObservationPool(
        solver::Solver *solver) {
    return std::make_unique<solver::EnumeratedObservationPool>(solver, getAllObservationsInOrder());
}

std::unique_ptr<solver::Serializer> JamuSampleModel::createSerializer(solver::Solver *solver) {
    switch (heuristicType_) {
    case RSActionCategory::LEGAL:
        return std::make_unique<JamuSampleLegalActionsTextSerializer>(solver);
    case RSActionCategory::PREFERRED:
        return std::make_unique<JamuSamplePreferredActionsTextSerializer>(solver);
    default:
        return std::make_unique<JamuSampleBasicTextSerializer>(solver);
    }
}
} /* namespace jamusample */
