/** @file JamuSampleMdpSolver.hpp
 *
 * Defines the JamuSampleMdpSolver class, which solves the fully observable version of
 * JamuSample in order to serve as a heuristic function for the POMDP.
 *
 * This file also contains the definition for JamuSampleMdpSolver, which allows this heuristic to be
 * selected via the string "exactMdp()" in the configuration file.
 */
#ifndef JAMUSAMPLE_MDPSOLVER_HPP_
#define JAMUSAMPLE_MDPSOLVER_HPP_

#include <iostream>
#include <map>
#include <unordered_set>
#include <utility>

#include "global.hpp"

#include "problems/shared/GridPosition.hpp"
#include "problems/shared/parsers.hpp"

#include "solver/abstract-problem/heuristics/HeuristicFunction.hpp"

namespace jamusample {
class JamuSampleModel;
class JamuSampleState;

/** A class that solves a fully observable version of JamuSample, 
 * in which it is known which jamus are good and which ones are bad.
 */
class JamuSampleMdpSolver {
public:
    /** Constructs a new MDP solver for the given model. */
    JamuSampleMdpSolver(JamuSampleModel *model);
    virtual ~JamuSampleMdpSolver() = default;
    _NO_COPY_OR_MOVE(JamuSampleMdpSolver);

    /** Solves the MDP again from scratch, using the current state of the model. */
    void solve();

    /** Calculates the exact value for the given state in the MDP. */
    double getQValue(JamuSampleState const &state) const;

private:
    /** Calculates the q-value for the given action, from the current position
     * with the given jamu state code (encoded into a number).
     *
     * The action is a simplified MDP action:
     * -1 => exit the map
     * 0+ => go to the given jamu and sample it (the jamu is assumed to be good)
     */
    double calculateQValue(GridPosition pos,
            long jamuStateCode, long action) const;

    JamuSampleModel *model_;
    std::map<std::pair<int, int>, double> valueMap_;
};

/** A class to parse the command-line heuristic setting for the case "exactMdp()". */
class JamuSampleMdpParser : public shared::Parser<solver::HeuristicFunction> {
public:
    /** Creates a new MDP parser associated with the given JamuSampleModel instance. */
    JamuSampleMdpParser(JamuSampleModel *model);
    virtual ~JamuSampleMdpParser() = default;
    _NO_COPY_OR_MOVE(JamuSampleMdpParser);

    /** Creates a solver::HeuristicFunction associated with the stored JamuSampleModel instance.
     *
     * This heuristic can then be used by the ABT algorithm.
     */
    virtual solver::HeuristicFunction parse(solver::Solver *solver, std::vector<std::string> args);

private:
    /** The JamuSampleModel instance this heuristic parser is associated with. */
    JamuSampleModel *model_;
};
} /* namespace jamusample */

#endif /* JAMUSAMPLE_MDPSOLVER_HPP_ */
