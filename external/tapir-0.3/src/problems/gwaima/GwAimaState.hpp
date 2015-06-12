/** @file GwAimaState.hpp
 *
 * Defines the GwAimaState class, which represents a state of the GwAima problem.
 */
#ifndef GWAIMASTATE_HPP_
#define GWAIMASTATE_HPP_

#include <cstddef>                      // for size_t

#include <memory>
#include <ostream>                      // for ostream
#include <vector>

#include "problems/shared/GridPosition.hpp"  // for GridPosition
#include "solver/abstract-problem/State.hpp"
#include "solver/abstract-problem/VectorState.hpp"

namespace gwaima {
/** A class representing a state in the GwAima POMDP.
 *
 * The state contains the positions of the robot.
 *
 * This class also implements solver::VectorState in order to allow the state to be easily
 * converted to a vector<double>, which can then be used inside the standard R*-tree implementation
 * of StateIndex to allow spatial lookup of states.
 */
class GwAimaState : public solver::VectorState {
    friend class GwAimaTextSerializer;
  public:
    /** Constructs a new GwAimaState with the given positions of the robot.
     */
    GwAimaState(GridPosition robotPos);

    virtual ~GwAimaState() = default;
    /** A copy constructor, for convenience. */
    GwAimaState(GwAimaState const &);
    /** The move constructor for GwAimaState is forbidden. */
    GwAimaState(GwAimaState &&) = delete;
    /** The copy assignment operator for GwAimaState is forbidden. */
    virtual GwAimaState &operator=(GwAimaState const &) = delete;
    /** The move assignment operator for GwAimaState is forbidden. */
    virtual GwAimaState &operator=(GwAimaState &&) = delete;

    std::unique_ptr<solver::Point> copy() const override;

    double distanceTo(solver::State const &otherState) const override;
    bool equals(solver::State const &otherState) const override;
    std::size_t hash() const;

    std::vector<double> asVector() const override;
    void print(std::ostream &os) const override;

    /** Returns the position of the robot. */
    GridPosition getRobotPosition() const;

  private:
    /** The position of the robot in the grid. */
    GridPosition robotPos_;
};
}// namespace gwaima

// We define a hash function directly in the std namespace.
namespace std {
/** A struct in the std namespace to define a standard hash function for the GwAimaState class. */
template<> struct hash<gwaima::GwAimaState> {
    /** Returns the hash value for the given GwAimaState. */
    std::size_t operator()(gwaima::GwAimaState const &state) const {
        return state.hash();
    }
};
} /* namespace std */

#endif
