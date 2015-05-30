/** @file JamuSampleMdpSolver.cpp
 *
 * Contains the implementations for JamuSampleMdpSolver and JamuSampleMdpParser.
 */
#include "JamuSampleMdpSolver.hpp"

#include <iostream>

#include "problems/shared/GridPosition.hpp"

#include "solver/HistoryEntry.hpp"

#include "JamuSampleModel.hpp"
#include "JamuSampleState.hpp"

namespace jamusample {
JamuSampleMdpSolver::JamuSampleMdpSolver(JamuSampleModel *model) :
            model_(model),
            valueMap_() {
}

void JamuSampleMdpSolver::solve() {
    if (model_->options_->hasVerboseOutput) {
        std::cout << "Solving MDP...";
        std::cout.flush();
    }

    valueMap_.clear();

    // States are represented as pairs of integers.
    // The first number encodes the states of the jamus.
    // The second number encodes the current position (which jamu you're on top of).
    std::set<std::pair<int, int>> states;
    std::set<std::pair<int, int>> newStates;

    // Start with a base case where all jamus are bad.
    for (int i = 0; i < model_->nJamus_; i++) {
        newStates.insert(std::make_pair(0, i));
    }

    for (int i = 0; i < model_->nJamus_; i++) {
        states = newStates;
        newStates.clear();
        for (std::pair<int, int> entry : states) {
            long jamuStateCode = entry.first;
            long positionNo = entry.second;
            GridPosition pos = model_->jamuPositions_[positionNo];

            // The value of going straight to the goal is a simple lower bound.
            double value = calculateQValue(pos, jamuStateCode, -1);
            if (valueMap_[entry] < value) {
                valueMap_[entry] = value;
            } else {
                value = valueMap_[entry];
            }

            for (int j = 0; j < model_->nJamus_; j++) {
                // Try propagating to the jamu we came from - it can't  be
                // the current jamu, and we must have sampled it so it
                // must be bad now.
                if (j != positionNo && (jamuStateCode & (1 << j)) == 0) {
                    long prevCode = jamuStateCode | (1 << positionNo);
                    GridPosition prevPos = model_->jamuPositions_[j];
                    std::pair<int, int> index = std::make_pair(prevCode, j);
                    double prevValue = calculateQValue(prevPos, prevCode, positionNo);
                    if (valueMap_[index] < prevValue) {
                        valueMap_[index] = prevValue;
                    }
                    newStates.insert(index);
                }
            }
        }
    }

    if (model_->options_->hasVerboseOutput) {
        std::cout << "                   Done." << std::endl << std::endl;
    }
}

double JamuSampleMdpSolver::getQValue(JamuSampleState const &state) const {
    GridPosition pos = state.getPosition();
    long jamuStateCode = model_->encodeJamus(state.getJamuStates());

    // Check the value of leaving the map.
    double value = calculateQValue(pos, jamuStateCode, -1);

    for (int i = 0; i < model_->nJamus_; i++) {
        // Only try to sample good jamus!
        if ((jamuStateCode & (1 << i)) != 0) {
            double newValue = calculateQValue(pos, jamuStateCode, i);
            if (newValue > value) {
                value = newValue;
            }
        }
    }
    return value;
}

double JamuSampleMdpSolver::calculateQValue(GridPosition pos, long jamuStateCode,
        long action) const {
    long actionsUntilReward = model_->getDistance(pos, action);
    if (actionsUntilReward == -1) {
        // Impossible!
        return -std::numeric_limits<double>::infinity();
    }

    double reward;
    double nextQValue;

    if (action == -1) {
        // Reward is received as you move into the goal square, not afterwards.
        actionsUntilReward -= 1;
        reward = model_->exitReward_;
        nextQValue = 0; // Terminal.
    } else {
        if ((jamuStateCode & (1 << action)) == 0) {
            debug::show_message("ERROR: No reward for this action!");
            reward = -model_->badJamuPenalty_;
        } else {
            reward = model_->goodJamuReward_;
        }

        long nextCode = jamuStateCode & ~(1 << action);
        nextQValue = valueMap_.at(std::make_pair(nextCode, action));
    }

    double discountFactor = model_->options_->discountFactor;
    return std::pow(discountFactor, actionsUntilReward) * (reward + discountFactor * nextQValue);
}


JamuSampleMdpParser::JamuSampleMdpParser(JamuSampleModel *model) :
        model_(model) {
}

solver::HeuristicFunction JamuSampleMdpParser::parse(solver::Solver* /*solver*/,
        std::vector<std::string> /*args*/) {
    if (model_->getMdpSolver() == nullptr) {
        model_->makeMdpSolver();
    }
    return [this] (solver::HistoryEntry const *, solver::State const *state,
            solver::HistoricalData const *) {
        JamuSampleMdpSolver *solver = model_->getMdpSolver();
        return solver->getQValue(static_cast<JamuSampleState const &>(*state));
    };
}
} /* namespace jamusample */
