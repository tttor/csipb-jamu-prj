/** @file GwAimaAction.hpp
 *
 * Defines the GwAimaAction class, which represents an action for the GwAima problem, and also the
 * ActionType enumeration, which enumerates the different types of actions for GwAima.
 */
#ifndef GWAIMA_ACTION_HPP_
#define GWAIMA_ACTION_HPP_

#include <cstddef>                      // for size_t

#include <ostream>                      // for ostream
#include <vector>                       // for vector

#include "solver/abstract-problem/Action.hpp"
#include "solver/abstract-problem/DiscretizedPoint.hpp"             // for DiscretizedPoint

namespace gwaima {

/** An enumeration of all the available actions in the GwAima PODMP. */
enum class ActionType : long {
    /** The action to move north. */
    NORTH = 0,
    /** The action to move east. */
    EAST = 1,
    /** The action to move south. */
    SOUTH = 2,
    /** The action to move west. */
    WEST = 3,
};

/** A class representing an action in the GwAima POMDP.
 *
 * This class also implements solver::DiscretizedPoint so that the solver can use a simplistic
 * enumerated action mapping approach (EnumeratedActionPool) to store the available actions from
 * each belief node.
 */
class ActiveTagAction : public solver::DiscretizedPoint {
    friend class TagTextSerializer;
  public:
    /** Constructs a new action from the given ActionType. */
    ActiveTagAction(ActionType actionType);
    /** Constructs a new action from the given integer code. */
    ActiveTagAction(long code);

    virtual ~ActiveTagAction() = default;
    _NO_COPY_OR_MOVE(ActiveTagAction);

    std::unique_ptr<solver::Action> copy() const override;
    double distanceTo(solver::Action const &otherAction) const override;
    void print(std::ostream &os) const override;

    long getBinNumber() const override;
    /** Returns the ActionType of this action. */
    ActionType getActionType() const;

  private:
    /** The ActionType for this action in the GwAima POMDP. */
    ActionType actionType_;
};
} /* namespace gwaima */

#endif // GWAIMA_ACTION_HPP_
