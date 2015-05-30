/** @file JamuSampleState.cpp
 *
 * Contains the implementation for the methods of JamuSampleState.
 */
#include "JamuSampleState.hpp"

#include <cstddef>                      // for size_t

#include <algorithm>                    // for copy
#include <iterator>                     // for ostream_iterator
#include <ostream>                      // for operator<<, ostream
#include <vector>                       // for vector, operator==, _Bit_const_iterator, _Bit_iterator_base, hash, vector<>::const_iterator

#include "global.hpp"
#include "problems/shared/GridPosition.hpp"  // for GridPosition, operator==, operator<<
#include "solver/abstract-problem/State.hpp"             // for State

namespace jamusample {
JamuSampleState::JamuSampleState(GridPosition position,
        std::vector<bool> jamuStates) :
    solver::Vector(),
    position_(position),
    jamuStates_(jamuStates) {
}

std::unique_ptr<solver::Point> JamuSampleState::copy() const {
    return std::make_unique<JamuSampleState>(position_, jamuStates_);
}

double JamuSampleState::distanceTo(solver::State const &otherState) const {
    JamuSampleState const &otherJamuSampleState =
        static_cast<JamuSampleState const &>(otherState);
    double distance = position_.manhattanDistanceTo(
                otherJamuSampleState.position_) / 10.0;
    typedef std::vector<bool>::const_iterator BoolIt;
    BoolIt it1 = jamuStates_.cbegin();
    BoolIt it2 = otherJamuSampleState.jamuStates_.cbegin();
    for (; it1 != jamuStates_.cend(); it1++, it2++) {
        if (*it1 != *it2) {
            distance += 1;
        }
    }
    return distance;
}

bool JamuSampleState::equals(solver::State const &otherState) const {
    JamuSampleState const &otherJamuSampleState =
        static_cast<JamuSampleState const &>(otherState);
    return (position_ == otherJamuSampleState.position_
            && jamuStates_ == otherJamuSampleState.jamuStates_);
}

std::size_t JamuSampleState::hash() const {
    std::size_t hashValue = 0;
    tapir::hash_combine(hashValue, position_.i);
    tapir::hash_combine(hashValue, position_.j);
    tapir::hash_combine(hashValue, jamuStates_);
    return hashValue;
}

void JamuSampleState::print(std::ostream &os) const {
    os << position_ << " GOOD: {";
    std::vector<int> goodJamus;
    std::vector<int> badJamus;
    for (std::size_t i = 0; i < jamuStates_.size(); i++) {
        if (jamuStates_[i]) {
            goodJamus.push_back(i);
        } else {
            badJamus.push_back(i);
        }
    }
    std::copy(goodJamus.begin(), goodJamus.end(),
            std::ostream_iterator<double>(os, " "));
    os << "}; BAD: {";
    std::copy(badJamus.begin(), badJamus.end(),
            std::ostream_iterator<double>(os, " "));
    os << "}";
}


std::vector<double> JamuSampleState::asVector() const {
    std::vector<double> vec(2 + jamuStates_.size());
    vec[0] = position_.i;
    vec[1] = position_.j;
    for (std::size_t i = 0; i < jamuStates_.size(); i++) {
        vec[i + 2] = jamuStates_[i] ? 1 : 0;
    }
    return vec;
}

GridPosition JamuSampleState::getPosition() const {
     return position_;
}

 std::vector<bool> JamuSampleState::getJamuStates() const {
     return jamuStates_;
 }
} /* namespace jamusample */
