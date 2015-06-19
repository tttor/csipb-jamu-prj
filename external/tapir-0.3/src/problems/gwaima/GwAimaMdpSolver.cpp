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

void GwAimaMdpSolver::solve() {
    using namespace std;
#ifndef HAS_EIGEN
    debug::show_message("ERROR: Can't use MDP Policy Iteration without Eigen!");
    std::exit(15);
#else
    if (model_->options_->hasVerboseOutput) {
        std::cout << "Solving MDP...\n";
        std::cout.flush();
    }

    valueMap_.clear();

    // Enumerated vector of actions.
    std::vector<std::unique_ptr<solver::DiscretizedPoint>> allActions = (
            model_->getAllActionsInOrder());

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
        // TODO: uniformly at random
        initialAction = ActionType::NORTH;

        allStates.push_back(state);
        stateIndex[state] = index;
        policy.push_back(static_cast<int>(initialAction));
        index += 1;
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

            double reward = -1;// move costs TODO: take from options
            GridPosition nextRobotPos = model_->getMovedPos(robotPos, actionType).first;
            
            GwAimaState nextState(nextRobotPos);
            int nextStateIndex = stateIndex[nextState];
            double probability = model_->getTransitionProbability(robotPos, nextRobotPos, actionType);
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
            possibleNextStates, transitionProbability, reward);

    iterator.fixValue(allStates.size(), 0.0);

    long numSteps = iterator.solve();
    std::vector<double> stateValues = iterator.getCurrentValues();

    // Now put all of the state values into our map.
    cout << "put all of the state values into our map\n";
    for (unsigned int stateNo = 0; stateNo < allStates.size(); stateNo++) {
        valueMap_[allStates[stateNo]] = stateValues[stateNo];
    }

    if (model_->options_->hasVerboseOutput) {
        std::cout << "Done; took " << numSteps << " steps." << std::endl << std::endl;
    }
#endif
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
