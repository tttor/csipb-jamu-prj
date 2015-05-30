/** @file JamuSampleAction.cpp
 *
 * Contains the implementations for the methods of the JamuSampleAction class.
 */
#include "JamuSampleAction.hpp"

#include <cstddef>                      // for size_t
#include <cstdint>

#include <algorithm>                    // for copy
#include <iterator>                     // for ostream_iterator
#include <ostream>                      // for operator<<, ostream
#include <vector>                       // for vector, operator==, _Bit_const_iterator, _Bit_iterator_base, hash, vector<>::const_iterator

#include "global.hpp"
#include "problems/shared/GridPosition.hpp"  // for GridPosition, operator==, operator<<
#include "solver/abstract-problem/State.hpp"             // for State

namespace jamusample {
JamuSampleAction::JamuSampleAction(ActionType actionType, uint8_t jamuNo) :
        actionType_(actionType),
        jamuNo_(jamuNo) {
}

JamuSampleAction::JamuSampleAction(long code) :
        actionType_(code <= 5 ? static_cast<ActionType>(code) : ActionType::CHECK),
        jamuNo_(actionType_ == ActionType::CHECK ? code-5 : 0) {
}

std::unique_ptr<solver::Action> JamuSampleAction::copy() const {
    return std::make_unique<JamuSampleAction>(actionType_,jamuNo_);
}

double JamuSampleAction::distanceTo(solver::Action const &/*otherAction*/) const {
    return 0;
}

void JamuSampleAction::print(std::ostream &os) const {
    os << actionType_;
    if (actionType_ == ActionType::CHECK) {
        os << static_cast<long>(jamuNo_);
    }
}

long JamuSampleAction::getBinNumber() const {
    long code = static_cast<long>(actionType_);
    if (actionType_ == ActionType::CHECK) {
        code += jamuNo_;
    }
    return code;
}

ActionType JamuSampleAction::getActionType() const {
    return actionType_;
}

long JamuSampleAction::getJamuNo() const {
    return jamuNo_;
}
} /* namespace jamusample */
