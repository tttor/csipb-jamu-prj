/** @file ActiveTagObservation.cpp
 *
 * Contains the implementations for the methods of ActiveTagObservation.
 */
#include "ActiveTagObservation.hpp"

#include <cstddef>                      // for size_t

#include <algorithm>                    // for copy
#include <iterator>                     // for ostream_iterator
#include <ostream>                      // for operator<<, ostream
#include <vector>                       // for vector, operator==, _Bit_const_iterator, _Bit_iterator_base, hash, vector<>::const_iterator

#include "global.hpp"

#include "problems/shared/GridPosition.hpp"  // for GridPosition, operator==, operator<<
#include "solver/abstract-problem/Observation.hpp"             // for Observation

#include "ActiveTagModel.hpp"

namespace activetag {
ActiveTagObservation::ActiveTagObservation(GridPosition position,
            bool _seesOpponent) :
                    position_(position),
                    seesOpponent_(_seesOpponent) {
}
std::unique_ptr<solver::Observation>
ActiveTagObservation::copy() const {
    return std::make_unique<ActiveTagObservation>(position_, seesOpponent_);
}

double ActiveTagObservation::distanceTo(
        solver::Observation const &otherObs) const {
    ActiveTagObservation const &other =
            static_cast<ActiveTagObservation const &>(otherObs);
    return seesOpponent_ == other.seesOpponent_ ? 0 : 1;
}

bool ActiveTagObservation::equals(
        solver::Observation const &otherObs) const {
    ActiveTagObservation const &other =
        static_cast<ActiveTagObservation const &>(otherObs);
    return position_ == other.position_ && seesOpponent_ == other.seesOpponent_;
}

std::size_t ActiveTagObservation::hash() const {
    std::size_t hashValue = 0;
    tapir::hash_combine(hashValue, position_.i);
    tapir::hash_combine(hashValue, position_.j);
    tapir::hash_combine(hashValue, seesOpponent_);
    return hashValue;
}

void ActiveTagObservation::print(std::ostream &os) const {
    os << position_ << " ";
    if (seesOpponent_) {
        os << "SEEN";
    } else {
        os << "UNSEEN";
    }
}

GridPosition ActiveTagObservation::getPosition() const {
    return position_;
}

bool ActiveTagObservation::seesOpponent() const {
    return seesOpponent_;
}
}
/* namespace activetag */
