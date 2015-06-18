/** @file GwAimaModel.cpp
 *
 * Contains the implementations for the core functionality of the GwAima POMDP.
 */
#include "GwAimaModel.hpp"

#include <cmath>                        // for floor, pow
#include <cstddef>                      // for size_t
#include <cstdlib>                      // for exit

#include <memory>
#include <fstream>                      // for ifstream, basic_istream, basic_istream<>::__istream_type
#include <iomanip>                      // for operator<<, setw
#include <iostream>                     // for cout
#include <random>                       // for uniform_int_distribution, bernoulli_distribution
#include <unordered_map>                // for _Node_iterator, operator!=, unordered_map<>::iterator, _Node_iterator_base, unordered_map
#include <utility>                      // for make_pair, move, pair

#include "global.hpp"                     // for RandomGenerator, make_unique
#include "problems/shared/GridPosition.hpp"  // for GridPosition, operator==, operator!=, operator<<
#include "problems/shared/ModelWithProgramOptions.hpp"  // for ModelWithProgramOptions

#include "solver/abstract-problem/Action.hpp"            // for Action
#include "solver/abstract-problem/Model.hpp"             // for Model::StepResult, Model
#include "solver/abstract-problem/Observation.hpp"       // for Observation
#include "solver/abstract-problem/State.hpp"             // for State, operator<<, operator==

#include "solver/changes/ChangeFlags.hpp"        // for ChangeFlags

#include "solver/indexing/FlaggingVisitor.hpp"
#include "solver/indexing/RTree.hpp"
#include "solver/indexing/SpatialIndexVisitor.hpp"             // for State, operator<<, operator==

#include "solver/mappings/actions/enumerated_actions.hpp"
#include "solver/mappings/observations/discrete_observations.hpp"

#include "solver/ActionNode.hpp"
#include "solver/BeliefNode.hpp"
#include "solver/StatePool.hpp"

#include "GwAimaAction.hpp"
#include "GwAimaObservation.hpp"
#include "GwAimaOptions.hpp"
#include "GwAimaState.hpp"                 // for GwAimaState
#include "GwAimaTextSerializer.hpp"

using std::cout;
using std::endl;

namespace gwaima {

GwAimaUBParser::GwAimaUBParser(GwAimaModel *model) :
        model_(model) {
}

solver::HeuristicFunction GwAimaUBParser::parse(solver::Solver * /*solver*/, std::vector<std::string> /*args*/) {
    return [this] (solver::HistoryEntry const *, solver::State const *state,
            solver::HistoricalData const *) {
        return model_->getUpperBoundHeuristicValue(*state);
    };
}

GwAimaModel::GwAimaModel(RandomGenerator *randGen, std::unique_ptr<GwAimaOptions> options) :
            ModelWithProgramOptions("GwAima", randGen, std::move(options)),
            options_(const_cast<GwAimaOptions *>(static_cast<GwAimaOptions const *>(getOptions()))),
            goalReward_(0.0),//TODO take from options
            moveCost_(options_->moveCost),
            boomCost_(0.0),//TODO take from options
            startPos_(), // update
            boomPositions_(),
            goalPositions_(), // push goals
            nRows_(0), // to be updated
            nCols_(0), // to be updated
            mapText_(), // will be pushed to
            envMap_(), // will be pushed to
            nActions_(options_->nActions),
            mdpSolver_(nullptr),
            pairwiseDistances_() {
    options_->numberOfStateVariables = 5;//TODO why 5?
    options_->minVal = -boomCost_ / (1 - options_->discountFactor);
    options_->maxVal = goalReward_;

    // Register the upper bound heuristic parser.
    registerHeuristicParser("upper", std::make_unique<GwAimaUBParser>(this));
    // Register the exact MDP heuristic parser.
    registerHeuristicParser("exactMdp", std::make_unique<GwAimaMdpParser>(this));

    // Read the map from the file.
    std::ifstream inFile;
    inFile.open(options_->mapPath);
    if (!inFile.is_open()) {
        std::ostringstream message;
        message << "ERROR: Failed to open " << options_->mapPath;
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
        cout << "Constructed the GwAimaModel" << endl;
        cout << "Discount: " << options_->discountFactor << endl;
        cout << "Size: " << nRows_ << " by " << nCols_ << endl;
        cout << "move cost: " << moveCost_ << endl;
        cout << "nActions: " << nActions_ << endl;
        cout << "nStVars: " << options_->numberOfStateVariables << endl;
        cout << "minParticleCount: " << options_->minParticleCount << endl;
        cout << "Environment:" << endl << endl;
        drawEnv(cout);
    }
}

int GwAimaModel::getMapDistance(GridPosition p1, GridPosition p2) {
    return pairwiseDistances_[p1.i][p1.j][p2.i][p2.j];
}

double GwAimaModel::getTransitionProbability(GridPosition nextRobotPos, 
                                             GridPosition robotPos, ActionType actionType) {
    int drow, dcol;
    drow = nextRobotPos.i - robotPos.i;
    dcol = nextRobotPos.j - robotPos.j;

    switch (static_cast<int>(actionType)) {
        case static_cast<int>(ActionType::NORTH): {
            if (drow > 0 and dcol==0) return 0.0;
            else if (drow < 0 and dcol==0) return 0.8;
            else if (drow==0 and dcol>0) return 0.1;
            else if (drow==0 and dcol<0) return 0.1;
            else if (drow==0 and dcol==0) return 0.8;// stay in place due to the wall
        }
        case static_cast<int>(ActionType::SOUTH): {
            if (drow > 0 and dcol==0) return 0.8;
            else if (drow < 0 and dcol==0) return 0.0;
            else if (drow==0 and dcol>0) return 0.1;
            else if (drow==0 and dcol<0) return 0.1;
            else if (drow==0 and dcol==0) return 0.8;// stay in place due to the wall
        }
        case static_cast<int>(ActionType::EAST): {
            if (drow > 0 and dcol==0) return 0.1;
            else if (drow < 0 and dcol==0) return 0.1;
            else if (drow==0 and dcol>0) return 0.8;
            else if (drow==0 and dcol<0) return 0.0;
            else if (drow==0 and dcol==0) return 0.8;// stay in place due to the wall
        }
        case static_cast<int>(ActionType::WEST): {
            if (drow > 0 and dcol==0) return 0.1;
            else if (drow < 0 and dcol==0) return 0.1;
            else if (drow==0 and dcol>0) return 0.0;
            else if (drow==0 and dcol<0) return 0.8;
            else if (drow==0 and dcol==0) return 0.8;// stay in place due to the wall
        }
        default: {
            assert (false && "UNKNOWN ActionType");
        }
    }
}

void GwAimaModel::calculateDistancesFrom(GridPosition position) {
    auto &distanceGrid = pairwiseDistances_[position.i][position.j];
    // Fill the grid with "-1", for inaccessible cells.
    for (auto &row : distanceGrid) {
        for (auto &cell : row) {
            cell = -1;
        }
    }
    if (envMap_[position.i][position.j] == GwAimaCellType::WALL) {
        return;
    }

    std::queue<GridPosition> queue;
    // Start at 0 for the current position.
    distanceGrid[position.i][position.j] = 0;
    queue.push(position);
    while (!queue.empty()) {
        GridPosition pos = queue.front();
        queue.pop();
        int distance = distanceGrid[pos.i][pos.j] + 1;
        for (ActionType direction : { ActionType::NORTH, ActionType::SOUTH, ActionType::WEST,
                ActionType::EAST }) {
            GridPosition nextPos;
            bool isLegal;
            std::tie(nextPos, isLegal) = getMovedPos(pos, direction);
            // If it's legal and it's an improvement it needs to be queued.
            if (isLegal) {
                int &nextPosDistance = distanceGrid[nextPos.i][nextPos.j];
                if (nextPosDistance == -1 || nextPosDistance > distance) {
                    nextPosDistance = distance;
                    queue.push(nextPos);
                }
            }
        }
    }
}

void GwAimaModel::calculatePairwiseDistances() {
    for (int i = 0; i < nRows_; i++) {
        for (int j = 0; j < nCols_; j++) {
            calculateDistancesFrom(GridPosition(i, j));
        }
    }
}

void GwAimaModel::initialize() {
    GridPosition p;
    envMap_.resize(nRows_);
    for (p.i = nRows_ - 1; p.i >= 0; p.i--) {
        envMap_[p.i].resize(nCols_);
        for (p.j = 0; p.j < nCols_; p.j++) {
            char c = mapText_[p.i][p.j];
            GwAimaCellType cellType;
            if (c == 'X') {
                cellType = GwAimaCellType::WALL;
            } else if (c == 'G') {
                cellType = GwAimaCellType::GOAL;
                goalPositions_.push_back(p);
            } else if (c == 'B') {
                cellType = GwAimaCellType::BOOM;   
                boomPositions_.push_back(p);
            } else {
                cellType = GwAimaCellType::EMPTY;
            }
            envMap_[p.i][p.j] = cellType;
        }
    }

    pairwiseDistances_.resize(nRows_);
    for (auto &rowOfGrids : pairwiseDistances_) {
        rowOfGrids.resize(nCols_);
        for (auto &grid : rowOfGrids) {
            grid.resize(nRows_);
            for (auto &row : grid) {
                row.resize(nCols_);
            }
        }
    }

    calculatePairwiseDistances();
}

GridPosition GwAimaModel::randomEmptyCell() {
    GridPosition pos;
    while (true) {
        pos.i = std::uniform_int_distribution<long>(0, nRows_ - 1)(
                *getRandomGenerator());
        pos.j = std::uniform_int_distribution<long>(0, nCols_ - 1)(
                *getRandomGenerator());
        if (envMap_[pos.i][pos.j] == GwAimaCellType::EMPTY) {
            break;
        }
    }
    return pos;
}

std::vector<GridPosition> GwAimaModel::getEmptyCells() {
    std::vector<GridPosition> emptyCells;
    for (long row = 0; row < this->getNRows(); row++) {
        for (long col = 0; col < this->getNCols(); col++) {
            // Ignore impossible states.
            if (envMap_[row][col] == GwAimaCellType::EMPTY) {
                emptyCells.emplace_back(row, col);
            }
        }
    }
    return emptyCells;
}

/* --------------- The model interface proper ----------------- */
std::unique_ptr<solver::State> GwAimaModel::sampleAnInitState() {
    return sampleStateUninformed();
}

std::unique_ptr<solver::State> GwAimaModel::sampleStateUninformed() {
    GridPosition robotPos = randomEmptyCell();
    return std::make_unique<GwAimaState>(robotPos);
}

bool GwAimaModel::isTerminal(solver::State const &state) {
    return (static_cast<GwAimaState const &>(state)==GwAimaState(goalPositions_[0])
            or 
            static_cast<GwAimaState const &>(state)==GwAimaState(boomPositions_[0])
           );
}

bool GwAimaModel::isTerminalGoal(solver::State const &state) {
    return (static_cast<GwAimaState const &>(state)==GwAimaState(goalPositions_[0]));
}

bool GwAimaModel::isTerminalBoom(solver::State const &state) {
    return (static_cast<GwAimaState const &>(state)==GwAimaState(boomPositions_[0]));
}

bool GwAimaModel::isValid(solver::State const &state) {
    GwAimaState const gwAimaState = static_cast<GwAimaState const &>(state);
    return isValid(gwAimaState.getRobotPosition());
}

/* -------------------- Black box dynamics ---------------------- */
std::pair<GridPosition, bool> GwAimaModel::sampleNextRobotPosition(GridPosition robotPos, 
                                                                   ActionType desiredAction) {
    
    // Take into account the transition probability via the actual action selection
    // For example, if the desired action is North, then
    // the probability of actual action  Get robot action based on transition probability
    std::discrete_distribution<int> distribution {0.8, 0.1, 0.1, 0.0};
    unsigned int actionNo = distribution(*getRandomGenerator());

    const unsigned int nActions = 4;
    int actualAction = -1;
    switch (actionNo) {
        case 0: { // go straight
            actualAction = static_cast<int>(desiredAction);
            break;
        }
        case 1: { // turn right
            actualAction = static_cast<int>(desiredAction) + 1;
            actualAction %= nActions; 
            break;
        }
        case 2: { // turn left
            if (static_cast<int>(desiredAction)==0)
                actualAction = static_cast<int>(ActionType::WEST);
            else
                actualAction = static_cast<int>(desiredAction) - 1;
            break;
        }
        case 3: { // turn back
            break;
        }
        default: {
            assert (false && "UNKNOWN ActionType");
        }
    }

    return getMovedPos(robotPos, static_cast<ActionType>(actualAction));
}

std::pair<GridPosition, bool> GwAimaModel::getMovedPos(GridPosition const &position,
                                                       ActionType action) {
    GridPosition movedPos = position;
    switch (action) {
        case ActionType::NORTH:
            movedPos.i -= 1;
            break;
        case ActionType::EAST:
            movedPos.j += 1;
            break;
        case ActionType::SOUTH:
            movedPos.i += 1;
            break;
        case ActionType::WEST:
            movedPos.j -= 1;
            break;
        default:
            std::ostringstream message;
            message << "Invalid action: " << (long) action;
            debug::show_message(message.str());
            break;
    }

    bool wasValid = isValid(movedPos);
    if (!wasValid) {
        movedPos = position;
    }

    return std::make_pair(movedPos, wasValid);
}

bool GwAimaModel::isValid(GridPosition const &position) {
    return (position.i >= 0 && position.i < nRows_ && position.j >= 0
            && position.j < nCols_ && envMap_[position.i][position.j] != GwAimaCellType::WALL);
}

std::pair<std::unique_ptr<GwAimaState>, bool> 
GwAimaModel::makeNextState(solver::State const &state, solver::Action const &action) {
	GwAimaState const &gwAimaState = static_cast<GwAimaState const &>(state);
	GwAimaAction const &gwAimaAction = static_cast<GwAimaAction const &>(action);
    
    GridPosition robotPos = gwAimaState.getRobotPosition();
    ActionType actionType = gwAimaAction.getActionType();

    GridPosition newRobotPos;
    bool wasValid;
    std::tie(newRobotPos, wasValid) = sampleNextRobotPosition(robotPos, actionType);
        
    return std::make_pair(std::make_unique<GwAimaState>(newRobotPos), wasValid);
}

std::unique_ptr<solver::State> 
GwAimaModel::generateNextState(
                                solver::State const &state, solver::Action const &action,
                                solver::TransitionParameters const * /*tp*/) {
    return makeNextState(static_cast<GwAimaState const &>(state), action).first;
}

double GwAimaModel::makeReward( GwAimaState const &state, GwAimaAction const &action,
                                GwAimaState const &nextState, bool isLegal) {
    if (isTerminalGoal(nextState)) {
        return goalReward_;
    }
    else if (isTerminalBoom(nextState)) {
        return -boomCost_;
    }
    else {
        return -moveCost_;
    }

    return 0.0;
}

double GwAimaModel::generateReward( solver::State const &state,
                                    solver::Action const &action,
                                    solver::TransitionParameters const * /*tp*/,
                                    solver::State const * /*nextState*/) {
    GwAimaState const &gwAimaState = (static_cast<GwAimaState const &>(state));
    GwAimaAction const &gwAimaAction = (static_cast<GwAimaAction const &>(action));

    std::unique_ptr<GwAimaState> nextState;
    bool isLegal;
    std::tie(nextState, isLegal) = makeNextState(gwAimaState, gwAimaAction);
    
    return makeReward(gwAimaState, gwAimaAction, *nextState, isLegal);
}


std::unique_ptr<solver::Observation> GwAimaModel::makeObservation(GwAimaState const &nextState) {
    return std::make_unique<GwAimaObservation>( nextState.getRobotPosition() );
}

std::unique_ptr<solver::Observation> 
GwAimaModel::generateObservation(
                                solver::State const * /*state*/, solver::Action const &/*action*/,
                                solver::TransitionParameters const * /*tp*/,
                                solver::State const &nextState) {
    return makeObservation(static_cast<GwAimaState const &>(nextState));
}

solver::Model::StepResult GwAimaModel::generateStep(solver::State const &state,
                                                    solver::Action const &action) {
    solver::Model::StepResult result;
    result.action = action.copy();
    std::unique_ptr<GwAimaState> nextState = makeNextState(state, action).first;

    result.observation = makeObservation(*nextState);
    result.reward = generateReward(state, action, nullptr, nullptr);
    result.isTerminal = isTerminal(*nextState);
    result.nextState = std::move(nextState);

    return result;
}

/* ------------ Methods for handling particle depletion -------------- */
std::vector<std::unique_ptr<solver::State>> 
GwAimaModel::generateParticles(
                                solver::BeliefNode * /*previousBelief*/, solver::Action const &action,
                                solver::Observation const &obs,
                                long nParticles,
                                std::vector<solver::State const *> const &previousParticles) {
    std::vector<std::unique_ptr<solver::State>> newParticles;
    // TODO fix me
    // GwAimaObservation const &observation = (static_cast<GwAimaObservation const &>(obs));
    // ActionType actionType = (static_cast<GwAimaAction const &>(action).getActionType());

    // typedef std::unordered_map<GwAimaState, double> WeightMap;
    // WeightMap weights;
    // double weightTotal = 0;

    // GridPosition newRobotPos(observation.getPosition());

    // for (solver::State const *state : previousParticles) {
    //     GwAimaState const *tagState = static_cast<GwAimaState const *>(state);
    //     GridPosition oldRobotPos(tagState->getRobotPosition());
    //     // Ignore states that do not match knowledge of the robot's position.
    //     if (newRobotPos != getMovedPos(oldRobotPos, actionType).first) {
    //         continue;
    //     }

    //     // Get the probability distribution for opponent moves.
    //     GridPosition oldOpponentPos(tagState->getOpponentPosition());
    //     std::unordered_map<GridPosition, double> opponentPosDistribution = (
    //             getNextOpponentPositionDistribution(oldRobotPos, oldOpponentPos));

    //     for (auto const &entry : opponentPosDistribution) {
    //         if (entry.first != newRobotPos) {
    //             GwAimaState newState(newRobotPos, entry.first, false);
    //             weights[newState] += entry.second;
    //             weightTotal += entry.second;
    //         }
    //     }
    // }
    // double scale = nParticles / weightTotal;
    // for (WeightMap::iterator it = weights.begin(); it != weights.end();
    //         it++) {
    //     double proportion = it->second * scale;
    //     long numToAdd = static_cast<long>(proportion);
    //     if (std::bernoulli_distribution(proportion - numToAdd)(
    //             *getRandomGenerator())) {
    //         numToAdd += 1;
    //     }
    //     for (int i = 0; i < numToAdd; i++) {
    //         newParticles.push_back(std::make_unique<GwAimaState>(it->first));
    //     }
    // }
    return newParticles;
}

std::vector<std::unique_ptr<solver::State>> 
GwAimaModel::generateParticles( solver::BeliefNode * /*previousBelief*/, solver::Action const &action,
                                solver::Observation const &obs, long nParticles) {
    std::vector<std::unique_ptr<solver::State>> newParticles;
    // TODO fix me
    // GwAimaObservation const &observation = (static_cast<GwAimaObservation const &>(obs));
    // ActionType actionType = (static_cast<GwAimaAction const &>(action).getActionType());
    // GridPosition newRobotPos(observation.getPosition());
    
    // while ((long)newParticles.size() < nParticles) {
    //     std::unique_ptr<solver::State> state = sampleStateUninformed();
    //     solver::Model::StepResult result = generateStep(*state, action);
    //     if (obs == *result.observation) {
    //         newParticles.push_back(std::move(result.nextState));
    //     }
    // }
    
    return newParticles;
}

/* --------------- Pretty printing methods ----------------- */
void GwAimaModel::dispCell(GwAimaCellType cellType, std::ostream &os) {
    switch (cellType) {
    case GwAimaCellType::EMPTY:
        os << ".";
        break;
    case GwAimaCellType::WALL:
        os << "X";
        break;
    default:
        os << "ER";
        break;
    }
}

void GwAimaModel::drawEnv(std::ostream &os) {
    for (std::vector<GwAimaCellType> &row : envMap_) {
        for (GwAimaCellType cellType : row) {
            dispCell(cellType, os);
            os << " ";
        }
        os << endl;
    }
}

void GwAimaModel::drawSimulationState(solver::BeliefNode const *belief,
        solver::State const &state, std::ostream &os) {
    // TODO fix drawSimulationState()
    // TagState const &tagState = static_cast<TagState const &>(state);
    // std::vector<solver::State const *> particles = belief->getStates();
    // std::vector<std::vector<long>> particleCounts(nRows_,
    //         std::vector<long>(nCols_));
    // for (solver::State const *particle : particles) {
    //     GridPosition opponentPos =
    //             static_cast<TagState const &>(*particle).getOpponentPosition();
    //     particleCounts[opponentPos.i][opponentPos.j] += 1;
    // }

    // std::vector<int> colors { 196, 161, 126, 91, 56, 21, 26, 31, 36, 41, 46 };
    // if (options_->hasColorOutput) {
    //     os << "Color map: ";
    //     for (int color : colors) {
    //         os << "\033[38;5;" << color << "m";
    //         os << '*';
    //         os << "\033[0m";
    //     }
    //     os << endl;
    // }
    // for (std::size_t i = 0; i < envMap_.size(); i++) {
    //     for (std::size_t j = 0; j < envMap_[0].size(); j++) {
    //         double proportion = (double) particleCounts[i][j]
    //                 / particles.size();
    //         if (options_->hasColorOutput) {
    //             if (proportion > 0) {
    //                 int color = colors[proportion * (colors.size() - 1)];
    //                 os << "\033[38;5;" << color << "m";
    //             }
    //         }
    //         GridPosition pos(i, j);
    //         bool hasRobot = (pos == tagState.getRobotPosition());
    //         bool hasOpponent = (pos == tagState.getOpponentPosition());
    //         if (hasRobot) {
    //             if (hasOpponent) {
    //                 os << "#";
    //             } else {
    //                 os << "r";
    //             }
    //         } else if (hasOpponent) {
    //             os << "o";
    //         } else {
    //             if (envMap_[i][j] == GwAimaCellType::WALL) {
    //                 os << "X";
    //             } else {
    //                 os << ".";
    //             }
    //         }
    //         if (options_->hasColorOutput) {
    //             os << "\033[0m";
    //         }
    //     }
    //     os << endl;
    // }
}

/* ---------------------- Basic customizations  ---------------------- */
double GwAimaModel::getDefaultHeuristicValue(solver::HistoryEntry const * /*entry*/,
            solver::State const *state, solver::HistoricalData const * /*data*/) {
    return 0.0;
    // TODO fix getDefaultHeuristicValue()
    // TagState const &tagState = static_cast<TagState const &>(*state);
    // if (tagState.isTagged()) {
    //     return 0;
    // }
    // GridPosition robotPos = tagState.getRobotPosition();
    // GridPosition opponentPos = tagState.getOpponentPosition();
    // long dist = getMapDistance(robotPos, opponentPos);
    // double nSteps = dist / opponentStayProbability_;
    // double finalDiscount = std::pow(options_->discountFactor, nSteps);
    // double qVal = -moveCost_ * (1 - finalDiscount) / (1 - options_->discountFactor);
    // qVal += finalDiscount * tagReward_;
    // return qVal;
}

double GwAimaModel::getUpperBoundHeuristicValue(solver::State const &state) {
    return 0.0;
    // TODO fix getUpperBoundHeuristicValue
    // TagState const &tagState = static_cast<TagState const &>(state);
    // if (tagState.isTagged()) {
    //     return 0;
    // }
    // GridPosition robotPos = tagState.getRobotPosition();
    // GridPosition opponentPos = tagState.getOpponentPosition();
    // long dist = getMapDistance(robotPos, opponentPos);
    // double finalDiscount = std::pow(options_->discountFactor, dist);
    // double qVal = -moveCost_ * (1 - finalDiscount) / (1 - options_->discountFactor);
    // qVal += finalDiscount * tagReward_;
    // return qVal;
}

/* ------- Customization of more complex solver functionality  --------- */
std::vector<std::unique_ptr<solver::DiscretizedPoint>> GwAimaModel::getAllActionsInOrder() {
    std::vector<std::unique_ptr<solver::DiscretizedPoint>> allActions;
    for (long code = 0; code < nActions_; code++) {
        allActions.push_back(std::make_unique<GwAimaAction>(code));
    }
    return allActions;
}

std::unique_ptr<solver::ActionPool> GwAimaModel::createActionPool(solver::Solver * /*solver*/) {
    return std::make_unique<solver::EnumeratedActionPool>(this, getAllActionsInOrder());
}

std::unique_ptr<solver::Serializer> GwAimaModel::createSerializer(solver::Solver *solver) {
    return std::make_unique<GwAimaTextSerializer>(solver);
}


}// namespace gwaima
