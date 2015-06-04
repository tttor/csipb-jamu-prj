/** @file GwAimaObservation.hpp
 *
 * Defines the GwAimaObservation class, which represents an observation in the GwAima POMDP.
 */
#ifndef GWAIMA_OBSERVATION_HPP_
#define GWAIMA_OBSERVATION_HPP_

#include <cstddef>                      // for size_t

#include <ostream>                      // for ostream
#include <vector>                       // for vector

#include "global.hpp"                     // for RandomGenerator

#include "problems/shared/GridPosition.hpp"
#include "solver/abstract-problem/DiscretizedPoint.hpp"
#include "solver/abstract-problem/Observation.hpp"

namespace gwaima {
/** A class representing an observation in the GwAima POMDP.
 *
 * This includes an observation of the robot's own position.
 */
class GwAimaObservation : public solver::Point {
    friend class GwAimaTextSerializer;
  public:
    /** Constructs a new GwAimaObservation for the given robot position.
     */
    GwAimaObservation(GridPosition myPosition);

    virtual ~GwAimaObservation() = default;
    _NO_COPY_OR_MOVE(GwAimaObservation);

    std::unique_ptr<solver::Observation> copy() const override;
    bool equals(solver::Observation const &otherObs) const override;
    std::size_t hash() const override;
    void print(std::ostream &os) const override;

    /** Returns the position the robot has observed itself in. */
    GridPosition getPosition() const;

  private:
    /** The position the robot sees itself in. */
    GridPosition position_;
};
} /* namespace gwaima */
#endif /* GWAIMA_OBSERVATION_HPP_ */
