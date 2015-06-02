/** @file ActiveTagMdpSolver.hpp
 *
 * Defines the ActiveTagMdpSolver class, which solves the fully observable version of ActiveTag in order to
 * serve as a heuristic function for the POMDP.
 *
 * This file also contains the definition for ActiveTagMdpParser, which allows this heuristic to be
 * selected via the string "exactMdp()" in the configuration file.
 */
#ifndef ACTIVETAG_MDPSOLVER_HPP_
#define ACTIVETAG_MDPSOLVER_HPP_

#include <iostream>
#include <unordered_map>
#include <vector>

#include "global.hpp"

#include "problems/shared/parsers.hpp"

#include "solver/abstract-problem/heuristics/HeuristicFunction.hpp"

#include "ActiveTagState.hpp"

namespace activetag {
class ActiveTagModel;

/** A class that solves the fully observable version of ActiveTag and stores the calculated value for
 * each state.
 */
class ActiveTagMdpSolver {
public:
    /** Creates a new ActiveTagMdpSolver which will be tied to the given ActiveTagModel instance. */
    ActiveTagMdpSolver(ActiveTagModel *model);
    virtual ~ActiveTagMdpSolver() = default;
    _NO_COPY_OR_MOVE(ActiveTagMdpSolver);

    /** Solves the MDP, using the current state of the */
    void solve();

    /** Returns the calculated MDP value for the given state. */
    double getValue(ActiveTagState const &state) const;

private:
    /** The model instance this MDP solver is associated with. */
    ActiveTagModel *model_;
    /** A map to hold the calculated value for each non-terminal state. */
    std::unordered_map<ActiveTagState, double> valueMap_;
};

/** A class to parse the command-line heuristic setting for the case "exactMdp()". */
class ActiveTagMdpParser : public shared::Parser<solver::HeuristicFunction> {
public:
    /** Creates a new MDP parser associated with the given ActiveTagModel instance. */
    ActiveTagMdpParser(ActiveTagModel *model);
    virtual ~ActiveTagMdpParser() = default;
    _NO_COPY_OR_MOVE(ActiveTagMdpParser);

    /** Creates a solver::HeuristicFunction associated with the stored ActiveTagModel instance.
     *
     * This heuristic can then be used by the ABT algorithm.
     */
    virtual solver::HeuristicFunction parse(solver::Solver *solver, std::vector<std::string> args);

private:
    /** The ActiveTagModel instance this heuristic parser is associated with. */
    ActiveTagModel *model_;
};
} /* namespace activetag */

#endif /* ACTIVETAG_MDPSOLVER_HPP_ */
