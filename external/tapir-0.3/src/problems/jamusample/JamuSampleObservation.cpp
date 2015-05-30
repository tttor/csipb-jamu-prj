/** @file JamuSampleObservation.cpp
 *
 * Contains the implementations for the methods of JamuSampleObservation.
 */
#include "JamuSampleObservation.hpp"

#include <cstddef>                      // for size_t

#include <algorithm>                    // for copy
#include <iterator>                     // for ostream_iterator
#include <ostream>                      // for operator<<, ostream
#include <vector>                       // for vector, operator==, _Bit_const_iterator, _Bit_iterator_base, hash, vector<>::const_iterator

#include "global.hpp"
#include "problems/shared/GridPosition.hpp"  // for GridPosition, operator==, operator<<
#include "solver/abstract-problem/Observation.hpp"             // for Observation

namespace jamusample {

JamuSampleObservation::JamuSampleObservation() :
        isEmpty_(true),
        isGood_(false) {
}

JamuSampleObservation::JamuSampleObservation(bool _isGood) :
        isEmpty_(false),
        isGood_(_isGood) {
}

JamuSampleObservation::JamuSampleObservation(bool _isEmpty, bool _isGood) :
        isEmpty_(_isEmpty),
        isGood_(_isGood) {
}

JamuSampleObservation::JamuSampleObservation(long code) :
        isEmpty_(code == 0),
        isGood_(code == 1) {
}

std::unique_ptr<solver::Observation> JamuSampleObservation::copy() const {
    return std::make_unique<JamuSampleObservation>(isEmpty_,isGood_);
}

double JamuSampleObservation::distanceTo(solver::Observation const &otherObs) const {
    JamuSampleObservation const &other =
            static_cast<JamuSampleObservation const &>(otherObs);
    return isGood_ == other.isGood_ ? 0 : 1;
}

bool JamuSampleObservation::equals(solver::Observation const &otherObs) const {
    JamuSampleObservation const &other =
        static_cast<JamuSampleObservation const &>(otherObs);
    return isGood_ == other.isGood_;
}

std::size_t JamuSampleObservation::hash() const {
    return isGood_ ? 1 : 0;
}

void JamuSampleObservation::print(std::ostream &os) const {
    if (isEmpty_) {
        os << "NONE";
    } else if (isGood_) {
        os << "GOOD";
    } else {
        os << "BAD";
    }
}

long JamuSampleObservation::getBinNumber() const {
    return isEmpty_ ? 0 : (isGood_ ? 1 : 2);
}

bool JamuSampleObservation::isEmpty() const {
    return isEmpty_;
}

bool JamuSampleObservation::isGood() const {
    return isGood_;
}
}
/* namespace jamusample */
