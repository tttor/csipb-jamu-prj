/** @file GwAimaModel.hpp
 *
 * Contains GwAimaModel, which implements the core Model interface for the GridWorld AIMA POMDP.
 */
#ifndef GWAIMAMODEL_HPP_
#define GWAIMAMODEL_HPP_

#include <memory>                       // for unique_ptr
#include <ostream>                      // for ostream
#include <string>                       // for string
#include <utility>                      // for pair
#include <vector>                       // for vector

#include "global.hpp"                     // for RandomGenerator

#include "problems/shared/GridPosition.hpp"  // for GridPosition
#include "problems/shared/ModelWithProgramOptions.hpp"  // for ModelWithProgramOptions

#include "solver/abstract-problem/Model.hpp"             // for Model::StepResult, Model
#include "solver/abstract-problem/ModelChange.hpp"             // for ModelChange
#include "solver/abstract-problem/TransitionParameters.hpp"
#include "solver/abstract-problem/Action.hpp"            // for Action
#include "solver/abstract-problem/Observation.hpp"       // for Observation
#include "solver/abstract-problem/State.hpp"

#include "solver/mappings/actions/enumerated_actions.hpp"
#include "solver/mappings/observations/discrete_observations.hpp"


#include "GwAimaAction.hpp"
#include "GwAimaOptions.hpp"
#include "GwAimaMdpSolver.hpp"

namespace gwaima {
/** A parser for a simple upper bound heuristic for GwAima.
 *
 * The actual function is defined in GwAimaModel::getUpperBoundHeuristicValue; this parser allows
 * that heuristic to be selected by using the string "upper()" in the configuration file.
 */
class GwAimaUBParser : public shared::Parser<solver::HeuristicFunction> {
public:
    /** Creates a new GwAimaUBParser associated with the given GwAimaModel instance. */
    GwAimaUBParser(GwAimaModel *model);
    virtual ~GwAimaUBParser() = default;
    _NO_COPY_OR_MOVE(GwAimaUBParser);

    virtual solver::HeuristicFunction parse(solver::Solver *solver, std::vector<std::string> args);

private:
    /** The GwAimaModel instance this heuristic parser is associated with. */
    GwAimaModel *model_;
};

/** The implementation of the Model interface for the GwAima POMDP.
 *
 * This class inherits from shared::ModelWithProgramOptions in order to use custom text-parsing
 * functionality to select many of the core ABT parameters, allowing the configuration options
 * to be changed easily via the configuration interface without having to recompile the code.
 */
class GwAimaModel: public shared::ModelWithProgramOptions {
    friend class GwAimaObservation;
    friend class GwAimaMdpSolver;

  public:
    /** Constructs a new GwAimaModel instance with the given random number engine, and the given set
     * of configuration options.
     */
    GwAimaModel(RandomGenerator *randGen, std::unique_ptr<GwAimaOptions> options);

    ~GwAimaModel() = default;
    _NO_COPY_OR_MOVE(GwAimaModel);

    /** The cells are either empty or walls. */
    enum class GwAimaCellType : int {
        /** An empty cell. */
        EMPTY = 0,
        /* The goal cell(s). */
        GOAL = 1,
        /* The boom cell(s). */
        BOOM = 2,
        /* A wall. */
        WALL = -1
    };

    /** Returns the resulting coordinates of an agent after it takes the given action type from the
     * given position.
     *
     * The boolean flag will be false if the agent's move represents an attempt to move into an
     * obstacle or off the edge of the map, which in the GwAima POMDP simply causes them to stay
     * in the same position.
     *
     * This flag is mostly not used as there is no penalty for this in GwAima, and the returned
     * position already reflects them staying still.
     */
    std::pair<GridPosition, bool> getMovedPos(GridPosition const &position, ActionType action);

    /* ---------- Custom getters for extra functionality  ---------- */
    /** Returns the number of rows in the map for this GwAimaModel instance. */
    long getNRows() const {
        return nRows_;
    }
    /** Returns the number of columns in the map for this GwAimaModel instance. */
    long getNCols() const {
        return nCols_;
    }

    /** Get a vector of valid grid positions */
    std::vector<GridPosition> getEmptyCells();

    /** Get 2D vector representing the current environment map */
    inline const std::vector<std::vector<GwAimaCellType>>& getEnvMap() {
        return envMap_;
    }

    /**
     * Returns proportion of belief particles about the target's
     * position for each grid position in the map
     */
    std::vector<std::vector<float>> getBeliefProportions(solver::BeliefNode const *belief);

    /** Initializes a GwAimaMdpSolver for this GwAimaModel, which can then be used to return heuristic
     * values for each state.
     */
    void makeMdpSolver() {
        mdpSolver_ = std::make_unique<GwAimaMdpSolver>(this);
        mdpSolver_->solve();
    }

    /** Returns the GwAimaMdpSolver solver (if any) owned by this model. */
    GwAimaMdpSolver *getMdpSolver() {
        return mdpSolver_.get();
    }

    /** Returns the distance within the map between the two given positions. */
    int getMapDistance(GridPosition p1, GridPosition p2);

    /** Obtain the transitino probability */
    double getTransitionProbability(GridPosition nextRobotPos, GridPosition robotPos, ActionType actionType);

    /* --------------- The model interface proper ----------------- */
    std::unique_ptr<solver::State> sampleAnInitState() override;
    std::unique_ptr<solver::State> sampleStateUninformed() override;
    bool isTerminal(solver::State const &state) override;
    bool isTerminalGoal(solver::State const &state);
    bool isTerminalBoom(solver::State const &state);
    bool isValid(solver::State const &state) override;

    /* -------------------- Black box dynamics ---------------------- */
    virtual std::unique_ptr<solver::State> generateNextState(
            solver::State const &state,
            solver::Action const &action,
            solver::TransitionParameters const * /*tp*/) override;
    virtual std::unique_ptr<solver::Observation> generateObservation(
            solver::State const * /*state*/,
            solver::Action const &action,
            solver::TransitionParameters const * /*tp*/,
            solver::State const &nextState) override;
    virtual double generateReward(
                solver::State const &state,
                solver::Action const &action,
                solver::TransitionParameters const * /*tp*/,
                solver::State const * /*nextState*/) override;
    virtual Model::StepResult generateStep(solver::State const &state,
            solver::Action const &action) override;

    std::pair<GridPosition, bool> sampleNextRobotPosition(GridPosition robotPos, 
                                                          ActionType desiredAction);

    /* ------------ Methods for handling particle depletion -------------- */
    /** Generates particles for GwAima using a particle filter from the previous belief.
      *
      * For each previous particle, possible next states are calculated based on consistency with
      * the given action and observation. These next states are then added to the output vector
      * in accordance with their probability of having been generated.
      */
    virtual std::vector<std::unique_ptr<solver::State>> generateParticles(
            solver::BeliefNode *previousBelief,
            solver::Action const &action,
            solver::Observation const &obs,
            long nParticles,
            std::vector<solver::State const *> const &previousParticles) override;

    /** Generates particles for GwAima according to an uninformed prior.
     *
     * Previous states are sampled uniformly at random, a single step is generated, and only states
     * consistent with the action and observation are kept.
     */
    virtual std::vector<std::unique_ptr<solver::State>> generateParticles(
            solver::BeliefNode *previousBelief,
            solver::Action const &action,
            solver::Observation const &obs,
            long nParticles) override;

    /* --------------- Pretty printing methods ----------------- */
    /** Prints a single cell of the map out to the given output stream. */
    virtual void dispCell(GwAimaCellType cellType, std::ostream &os);
    virtual void drawEnv(std::ostream &os) override;
    virtual void drawSimulationState(solver::BeliefNode const *belief,
            solver::State const &state,
            std::ostream &os) override;


    /* ---------------------- Basic customizations  ---------------------- */
    virtual double getDefaultHeuristicValue(solver::HistoryEntry const *entry,
                solver::State const *state, solver::HistoricalData const *data) override;

    /** Returns an upper bound heuristic value for the given state.
     *
     * This upper bound assumes that ... TODO
     */
    virtual double getUpperBoundHeuristicValue(solver::State const &state);

    /* ------- Customization of more complex solver functionality  --------- */
    /** Returns all of the actions available for the GwAima POMDP, in the order of their enumeration
     * (as specified by gwaima::ActionType).
     */
    virtual std::vector<std::unique_ptr<solver::DiscretizedPoint>> getAllActionsInOrder();
    virtual std::unique_ptr<solver::ActionPool> createActionPool(solver::Solver *solver) override;

    virtual std::unique_ptr<solver::Serializer> createSerializer(solver::Solver *solver) override;

  private:
    /** Calculates the distances from the given position to all other parts of the map. */
    void calculateDistancesFrom(GridPosition position);
    /** Calculates all pairwise distances on the map. */
    void calculatePairwiseDistances();

    /** Initialises the required data structures and variables for this model. */
    void initialize();

    /** Generates a random empty grid cell. */
    GridPosition randomEmptyCell();

    /** Generates a next state for the given state and action, as well as a boolean flag that will
     * be true if the action moved into a wall, and false otherwise.
     *
     * Moving into a wall in GwAima simply means nothing happens - there is no associated penalty;
     * as such, this flag is mostly not used in the GwAima problem.
     */
    std::pair<std::unique_ptr<GwAimaState>, bool> makeNextState(
            solver::State const &state, solver::Action const &action);

    /** Generates an observation given the resulting next state, after the GwAima robot has made its
     * action.
     */
    std::unique_ptr<solver::Observation> makeObservation(GwAimaState const &nextState);

    /** Retrieves the reward via the next state. */
    double makeReward( GwAimaState const &state, GwAimaAction const &action,
                       GwAimaState const &nextState, bool isLegal);

    /** Returns true iff the given GridPosition represents a valid square that an agent could be
     * in - that is, the square must be empty, and within the bounds of the map.
     */
    bool isValid(GridPosition const &pos);

    /** The GwAimaOptions instance associated with this model. */
    GwAimaOptions *options_;

    /** The reward for successfully reach the goal state. */
    double goalReward_;
    /** The penalty for each movement action. */
    double moveCost_;
    /** The penalty for stepping into a boom cell. */
    double boomCost_;

    /** The starting position. */
    GridPosition startPos_;
    /** The coordinates of the booms. */
    std::vector<GridPosition> boomPositions_;
    /** The coordinates of the goal squares. */
    std::vector<GridPosition> goalPositions_;

    /** The number of rows in the map. */
    long nRows_;
    /** The number of columns in the map. */
    long nCols_;

    /** The environment map in text form. */
    std::vector<std::string> mapText_;
    /** The environment map in vector form. */
    std::vector<std::vector<GwAimaCellType>> envMap_;

    /** The number of possible actions in the GwAima POMDP. */
    long nActions_;

    /** Solver for the MDP version of the problem. */
    std::unique_ptr<GwAimaMdpSolver> mdpSolver_;

    /** The pairwise distances between each pair of cells in the map. */
    std::vector<std::vector<std::vector<std::vector<int>>>> pairwiseDistances_;
};
}// namespace gwaima

#endif
