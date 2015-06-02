/** @file ActiveTagState.hpp
 *
 * Defines the ActiveTagState class, which represents a state of the ActiveTag problem.
 */
#ifndef ACTIVETAGSTATE_HPP_
#define ACTIVETAGSTATE_HPP_

#include <cstddef>                      // for size_t

#include <memory>
#include <ostream>                      // for ostream
#include <vector>

#include "problems/shared/GridPosition.hpp"  // for GridPosition
#include "solver/abstract-problem/State.hpp"
#include "solver/abstract-problem/VectorState.hpp"

namespace activetag {
/** A class representing a state in the ActiveTag POMDP.
 *
 * The state contains the positions of the robot and the opponent, as well as a boolean flag for
 * whether or not the opponent has been tagged; tagged => terminal state.
 *
 * This class also implements solver::VectorState in order to allow the state to be easily
 * converted to a vector<double>, which can then be used inside the standard R*-tree implementation
 * of StateIndex to allow spatial lookup of states.
 */
class ActiveTagState : public solver::VectorState {
    friend class ActiveTagTextSerializer;
  public:
    /** Constructs a new ActiveTagState with the given positions of the robot and opponent, and the
     * given tagged state.
     */
    ActiveTagState(GridPosition robotPos, GridPosition opponentPos, bool _isTagged);

    virtual ~ActiveTagState() = default;
    /** A copy constructor, for convenience. */
    ActiveTagState(ActiveTagState const &);
    /** The move constructor for ActiveTagState is forbidden. */
    ActiveTagState(ActiveTagState &&) = delete;
    /** The copy assignment operator for ActiveTagState is forbidden. */
    virtual ActiveTagState &operator=(ActiveTagState const &) = delete;
    /** The move assignment operator for ActiveTagState is forbidden. */
    virtual ActiveTagState &operator=(ActiveTagState &&) = delete;

    std::unique_ptr<solver::Point> copy() const override;

    double distanceTo(solver::State const &otherState) const override;
    bool equals(solver::State const &otherState) const override;
    std::size_t hash() const;

    std::vector<double> asVector() const override;
    void print(std::ostream &os) const override;

    /** Returns the position of the robot. */
    GridPosition getRobotPosition() const;
    /** Returns the position of the opponent. */
    GridPosition getOpponentPosition() const;
    /** Returns true iff the opponent has already been tagged. */
    bool isTagged() const;
  private:
    /** The position of the robot in the grid. */
    GridPosition robotPos_;
    /** The position of the opponent in the grid. */
    GridPosition opponentPos_;
    /** A flag that is true iff the opponent has been tagged. */
    bool isTagged_;
};
} /* namespace activetag */

// We define a hash function directly in the std namespace.
namespace std {
/** A struct in the std namespace to define a standard hash function for the ActiveTagState class. */
template<> struct hash<activetag::ActiveTagState> {
    /** Returns the hash value for the given ActiveTagState. */
    std::size_t operator()(activetag::ActiveTagState const &state) const {
        return state.hash();
    }
};
} /* namespace std */

#endif /* ACTIVETAGSTATE_HPP_ */
