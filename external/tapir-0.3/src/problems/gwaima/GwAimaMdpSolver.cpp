/** @file GwAimaMdpSolver.cpp
 *
 * Contains the implementations for GwAimaMdpSolver and GwAimaMdpParser.
 */
#include "GwAimaMdpSolver.hpp"

#include <iostream>
#include <memory>
#include <unordered_map>
#include <vector>

#include "global.hpp"

#ifdef HAS_EIGEN
#include "problems/shared/policy_iteration.hpp"
#endif

#include "problems/shared/parsers.hpp"
#include "solver/abstract-problem/heuristics/HeuristicFunction.hpp"

#include "GwAimaModel.hpp"
#include "GwAimaState.hpp"

namespace gwaima {
/* ---------------------- GwAimaMdpSolver --------------------- */
GwAimaMdpSolver::GwAimaMdpSolver(GwAimaModel *model) :
            model_(model),
            valueMap_() {
}

void GwAimaMdpSolver::solve_via_value_iter() {
    if (model_->options_->hasVerboseOutput) {
        std::cout << "Solving MDP using value_iteration...";
        std::cout.flush();
    }

    valueMap_.clear();

    // States are represented as pairs of integers
    // That is an element of <i,j>
    std::set<std::pair<int,int>> states;
    std::set<std::pair<int,int>> newStates;

    for (int i = 0; i < model_->nRows_; ++i) {
        for (int j = 0; j < model_->nCols_; ++j) {
            newStates.insert(std::make_pair(i,j));
        }
    }

    states = newStates;
    for (std::pair<int,int> entry : states) {
        GridPosition pos(entry.first, entry.second);

        // The value of going straight to the goal is a simple lower bound.
        // TODO lower bound = ...?
        double value = calculateQValue(pos, -1);// -1 => exit the map

        // take the max:
        // valueMap_[entry] = value = max (valueMap_[entry], value)
        if (valueMap_[entry] < value) {
            valueMap_[entry] = value;
        } else {
            value = valueMap_[entry];
        }

        // TODO follow solution in gw-aima (in python)
        // the implementation in rocksample is too specific
    }

    if (model_->options_->hasVerboseOutput) {
        std::cout << ": Done." << std::endl << std::endl;
    }
}

double GwAimaMdpSolver::calculateQValue(GridPosition pos, long action) const {
    long actionsUntilReward = model_->getDistance(pos);
    if (actionsUntilReward == -1) {
        // The goal is Impossible to reach!
        return -std::numeric_limits<double>::infinity();
    }

    double reward;
    double nextQValue;

    if (action == -1) {
        // Reward is received as you move in to the goal, not afterwards
        actionsUntilReward -= 1;// decrement by one as the agent moves in the goal
        
        reward = model_->goalReward_;
        nextQValue = 0; // Terminal
    }
    else {
        //TODO

        // reward = 
        // nextQValue = 
    }

    double discountFactor = model_->options_->discountFactor;
    return std::pow(discountFactor, actionsUntilReward) * (reward + discountFactor * nextQValue);
}

void GwAimaMdpSolver::solve_via_policy_iter() {
    using namespace std;
#ifndef HAS_EIGEN
    debug::show_message("ERROR: Can't use MDP Policy Iteration without Eigen!");
    std::exit(15);
#else
    if (model_->options_->hasVerboseOutput) {
        std::cout << "Solving MDP using policy_iteration...\n";
        std::cout.flush();
    }

    valueMap_.clear();

    // Enumerated vector of actions.
    std::vector<std::unique_ptr<solver::DiscretizedPoint>> 
    allActions = (model_->getAllActionsInOrder());

    // Vector of valid grid positions.
    std::vector<GridPosition> emptyCells;
    for (long row = 0; row < model_->getNRows(); row++) {
        for (long col = 0; col < model_->getNCols(); col++) {
            // Ignore impossible states.
            if (model_->envMap_[row][col] == GwAimaModel::GwAimaCellType::EMPTY) {
                emptyCells.emplace_back(row, col);
            }
        }
    }

    // An initial policy
    mdp::Policy policy;
    // Enumerated vector of all states.
    std::vector<GwAimaState> allStates;
    // Mapping from each state to its assigned index.
    std::unordered_map<GwAimaState, int> stateIndex;

    int index = 0;
    for (GridPosition const &robotPos : emptyCells) {
        GwAimaState state(robotPos);

        ActionType initialAction;
        // Set a default initial action for our initial policy.
        long initialActionRaw = std::uniform_int_distribution<long>(0, model_->nActions_ - 1)
                                (*model_->getRandomGenerator());
        initialAction = static_cast<ActionType>(initialActionRaw);

        allStates.push_back(state);
        stateIndex[state] = index;
        policy.push_back(static_cast<int>(initialAction));
        index++;
    }
    // An index of size (past the end of the array!!) will be used to represent terminal states.
    // A default action for the terminal state is meaningless, but we need it anyway.
    // TODO Why does not include this terminal state in allStates? why should past the end of array?
    policy[index] = static_cast<int>(ActionType::NORTH);// TODO: fix this action!

    // Initialise the state transitions.
    cout << "Initialise the state transitions.:BEGIN\n";
    std::vector<std::vector<std::unordered_map<int, std::pair<double, double>>>> transitions;
    transitions.resize(allStates.size() + 1);
    for (unsigned int stateNo = 0; stateNo <= allStates.size(); stateNo++) {
        GwAimaState const &state = allStates[stateNo];
        GridPosition robotPos = state.getRobotPosition();

        transitions[stateNo].resize(allActions.size());
        for (unsigned int actionNo = 0; actionNo < allActions.size(); actionNo++) {
            ActionType actionType = static_cast<ActionType>(actionNo);
            auto &nextStateTransitions = transitions[stateNo][actionNo];
            
            GridPosition nextRobotPos = model_->getMovedPos(robotPos, actionType).first;
            GwAimaState nextState(nextRobotPos);
            int nextStateIndex = stateIndex[nextState];

            double probability = model_->getTransitionProbability(robotPos, nextRobotPos, actionType);
            double reward = model_->moveCost_;// TODO: recheck! consider other costs?
            nextStateTransitions[nextStateIndex] = std::make_pair(probability, reward);
        }
    }

    cout << "std::function<std::vector<int>(int, int)> possibleNextStates\n";
    std::function<std::vector<int>(int, int)> possibleNextStates =
            [transitions](int state, int action) {
                std::vector<int> nextStates;
                for (auto const &entry : transitions[state][action]) {
                    nextStates.push_back(entry.first);
                }
                return std::move(nextStates);
            };

    cout << "std::function<double(int, int, int)> transitionProbability\n";
    std::function<double(int, int, int)> transitionProbability =
            [transitions](int state, int action, int nextState) {
                return transitions[state][action].at(nextState).first;
            };

    cout << "std::function<double(int, int, int)> reward\n";        
    std::function<double(int, int, int)> reward =
            [transitions](int state, int action, int nextState) {
                return transitions[state][action].at(nextState).second;
            };

    cout << "mdp::PolicyIterator iterator()\n";
    mdp::PolicyIterator iterator(policy, model_->options_->discountFactor,
                                 allStates.size() + 1, allActions.size(),
                                 possibleNextStates, transitionProbability, 
                                 reward);

    /** Sets the value of the given state as a fixed quantity - this is used to set reward values
    * for terminal states, if any exist.
    */
    iterator.fixValue(allStates.size(), 0.0);

    /** Solves the MDP via policy iteration and returns the number of policy iteration steps taken
     * in attempting to solve the problem.
     */
    long numSteps = iterator.solve();

    if (model_->options_->hasVerboseOutput) {
        std::cout << "Done; took " << numSteps << " steps." << std::endl << std::endl;
    }

    // Evaluate the resulted policy
    mdp::Policy bestPolicy;
    bestPolicy = iterator.getBestPolicy();
    print(bestPolicy, allStates);

    std::vector<double> stateValues;
    stateValues = iterator.getCurrentValues();
    
    cout << "stateValues.size()= " << stateValues.size() << endl;
    for (size_t i=0; i<stateValues.size(); ++i) {
        cout << "stateValues["<< i << "]= " << stateValues.at(i) << endl;
    }
    // for (unsigned int stateNo = 0; stateNo < allStates.size(); stateNo++) {
    //     valueMap_[allStates[stateNo]] = stateValues[stateNo];
    // }
#endif
}

void GwAimaMdpSolver::print(const mdp::Policy& policy, const std::vector<GwAimaState>& states) {
    using namespace std;

    std::vector<std::vector<long>> 
    policyMap(model_->getNRows(), 
              std::vector<long>(model_->getNCols(),-1));

    for (size_t i=0; i<policy.size(); ++i) {
        GwAimaState state = states.at(i);
        GridPosition robotPos = state.getRobotPosition();
        policyMap.at(robotPos.i).at(robotPos.j) = policy.at(i);
        // cout << "at (" <<  robotPos.i << ", " << robotPos.j << ")= " 
        //      << policy.at(i) << endl;
    }

    for (size_t i=0; i<policyMap.size(); ++i) {
        for (size_t j=0; j<policyMap.at(i).size(); ++j) {
            ActionType action;
            action = static_cast<ActionType>( policyMap.at(i).at(j) );

            switch (action) {
                case ActionType::NORTH:
                    cout << "^";
                    break;
                case ActionType::EAST:
                    cout << ">";
                    break;
                case ActionType::SOUTH:
                    cout << "v";
                    break;
                case ActionType::WEST:
                    cout << "<";
                    break;
                default:
                    cout << "X";
                    break;
            }
            cout << " ";
        }
        cout << endl;
    }
}

double GwAimaMdpSolver::getValue(GwAimaState const &state) const {
    // if this state is a terminal state, then
    // return 0 because the reward is applied on the previous timestep.
    if (model_->isTerminal(state)) {
        std::cout << "model_->isTerminal(state) return 0\n";
        return 0;
    }

    try {
        std::cout << "return valueMap_.at(state);\n";
        return valueMap_.at(state);
    } 
    catch (std::out_of_range const &oor) {
        // INVALID STATE => return 0
        std::cout << "NOTE: Queried heuristic value of an invalid state." << std::endl;
        return 0;
    }
}

/* ---------------------- GwAimaMdpParser --------------------- */
GwAimaMdpParser::GwAimaMdpParser(GwAimaModel *model) :
        model_(model) {
}

solver::HeuristicFunction GwAimaMdpParser::parse(solver::Solver * /*solver*/,
        std::vector<std::string> /*args*/) {
    if (model_->getMdpSolver() == nullptr) {
        model_->makeMdpSolver();
    }
    return [this] (solver::HistoryEntry const *, solver::State const *state,
            solver::HistoricalData const *) {
        GwAimaMdpSolver *solver = model_->getMdpSolver();
        return solver->getValue(static_cast<GwAimaState const &>(*state));
    };
}
} /* namespace gwaima */
