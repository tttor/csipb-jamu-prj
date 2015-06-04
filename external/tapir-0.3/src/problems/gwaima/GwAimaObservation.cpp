/** @file GwAimaObservation.cpp
 *
 * Contains the implementations for the methods of GwAimaObservation.
 */
#include "GwAimaObservation.hpp"

#include <cstddef>                      // for size_t

#include <algorithm>                    // for copy
#include <iterator>                     // for ostream_iterator
#include <ostream>                      // for operator<<, ostream
#include <vector>                       // for vector, operator==, _Bit_const_iterator, _Bit_iterator_base, hash, vector<>::const_iterator

#include "global.hpp"

#include "problems/shared/GridPosition.hpp"  // for GridPosition, operator==, operator<<
#include "solver/abstract-problem/Observation.hpp"             // for Observation

namespace gwaima {
GwAimaObservation::GwAimaObservation(GridPosition position): position_(position) {
}

std::unique_ptr<solver::Observation>
GwAimaObservation::copy() const {
    return std::make_unique<GwAimaObservation>(position_);
}

bool GwAimaObservation::equals(
        solver::Observation const &otherObs) const {
    GwAimaObservation const &other =
        static_cast<GwAimaObservation const &>(otherObs);
    return position_ == other.position_ && seesOpponent_ == other.seesOpponent_;
}

std::size_t GwAimaObservation::hash() const {
    std::size_t hashValue = 0;
    tapir::hash_combine(hashValue, position_.i);
    tapir::hash_combine(hashValue, position_.j);
    return hashValue;
}

void GwAimaObservation::print(std::ostream &os) const {
}

GridPosition GwAimaObservation::getPosition() const {
    return position_;
}

} /* namespace gwaima */