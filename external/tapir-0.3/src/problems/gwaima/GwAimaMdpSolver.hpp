/** @file GwAimaMdpSolver.hpp
 *
 * Defines the GwAimaMdpSolver class, which solves the fully observable version of GwAima in order to
 * serve as a heuristic function for the POMDP.
 *
 * This file also contains the definition for GwAimaMdpParser, which allows this heuristic to be
 * selected via the string "exactMdp()" in the configuration file.
 */
#ifndef GWAIMA_MDPSOLVER_HPP_
#define GWAIMA_MDPSOLVER_HPP_

#include <iostream>
#include <unordered_map>
#include <vector>

#include "global.hpp"

#include "problems/shared/parsers.hpp"

#include "solver/abstract-problem/heuristics/HeuristicFunction.hpp"

#include "GwAimaState.hpp"

namespace tag {
class GwAimaModel;

/** A class that solves the fully observable version of GwAima and stores the calculated value for
 * each state.
 */
class GwAimaMdpSolver {
public:
    /** Creates a new GwAimaMdpSolver which will be tied to the given GwAimaModel instance. */
    GwAimaMdpSolver(GwAimaModel *model);
    virtual ~GwAimaMdpSolver() = default;
    _NO_COPY_OR_MOVE(GwAimaMdpSolver);

    /** Solves the MDP, using the current state of the */
    void solve();

    /** Returns the calculated MDP value for the given state. */
    double getValue(GwAimaState const &state) const;

private:
    /** The model instance this MDP solver is associated with. */
    GwAimaModel *model_;
    /** A map to hold the calculated value for each non-terminal state. */
    std::unordered_map<GwAimaState, double> valueMap_;
};

/** A class to parse the command-line heuristic setting for the case "exactMdp()". */
class GwAimaMdpParser : public shared::Parser<solver::HeuristicFunction> {
public:
    /** Creates a new MDP parser associated with the given GwAimaModel instance. */
    GwAimaMdpParser(GwAimaModel *model);
    virtual ~GwAimaMdpParser() = default;
    _NO_COPY_OR_MOVE(GwAimaMdpParser);

    /** Creates a solver::HeuristicFunction associated with the stored GwAimaModel instance.
     *
     * This heuristic can then be used by the ABT algorithm.
     */
    virtual solver::HeuristicFunction parse(solver::Solver *solver, std::vector<std::string> args);

private:
    /** The GwAimaModel instance this heuristic parser is associated with. */
    GwAimaModel *model_;
};
} /* namespace tag */

#endif // GWAIMA_MDPSOLVER_HPP_
