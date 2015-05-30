/** @file JamuSampleState.hpp
 *
 * Defines the JamuSampleState class, which represents a state of the JamuSample problem.
 */
#ifndef JAMUSAMPLE_STATE_HPP_
#define JAMUSAMPLE_STATE_HPP_

#include <cstddef>                      // for size_t

#include <ostream>                      // for ostream
#include <vector>                       // for vector

#include "problems/shared/GridPosition.hpp"  // for GridPosition
#include "solver/abstract-problem/State.hpp"             // for State
#include "solver/abstract-problem/VectorState.hpp"             // for VectorState

namespace jamusample {
/** A class representing a state in the JamuSample POMDP.
 *
 * The state contains the position of the robot (a composer agent), as well as 
 * a boolean value for jamu formula at the current position, representing whether it is good (true => good, false => bad).
 *
 * This class also implements solver::VectorState in order to allow the state to be easily
 * converted to a vector<double>, which can then be used inside the standard R*-tree implementation
 * of StateIndex to allow spatial lookup of states.
 */
class JamuSampleState : public solver::VectorState {
    friend class JamuSampleTextSerializer;
  public:
    /** Constructs a new JamuSampleState with the given robot position, and the given goodness states
     * for all of the jamus.
     */
    JamuSampleState(GridPosition position, std::vector<bool> jamuStates);
    virtual ~JamuSampleState() = default;

    std::unique_ptr<solver::State> copy() const override;
    double distanceTo(solver::State const &otherState) const override;
    bool equals(solver::State const &otherState) const override;
    std::size_t hash() const override;
    void print(std::ostream &os) const override;

    std::vector<double> asVector() const override;

    /** Returns the position of the robot. */
    GridPosition getPosition() const;
    /** Returns the goodness states for all of the jamus (true => good). */
    std::vector<bool> getJamuStates() const;

  private:
    /** The position of the robot. */
    GridPosition position_;
    /** The goodness states of the jamus in this JamuSampleState. */
    std::vector<bool> jamuStates_;
};
} /* namespace jamusample */

// We define a hash function directly in the std namespace.
namespace std {
/** A struct in the std namespace to define a standard hash function for the
 * JamuSampleState class.
 */
template<> struct hash<jamusample::JamuSampleState> {
    /** Returns the hash value for the given JamuSampleState. */
    std::size_t operator()(jamusample::JamuSampleState const &state) const {
        return state.hash();
    }
};
} /* namespace std */

#endif /* JamuSampleSTATE_HPP_ */
