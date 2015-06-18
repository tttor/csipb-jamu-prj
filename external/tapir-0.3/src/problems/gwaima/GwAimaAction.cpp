/** @file GwAimaAction.cpp
 *
 * Contains the implementations for the methods of the GwAimaAction class.
 */
#include "GwAimaAction.hpp"

#include <cstddef>                      // for size_t

#include <algorithm>                    // for copy
#include <iterator>                     // for ostream_iterator
#include <ostream>                      // for operator<<, ostream
#include <vector>                       // for vector, operator==, _Bit_const_iterator, _Bit_iterator_base, hash, vector<>::const_iterator

#include "global.hpp"

#include "problems/shared/GridPosition.hpp"  // for GridPosition, operator==, operator<<
#include "solver/abstract-problem/State.hpp"             // for State

 namespace gwaima {
GwAimaAction::GwAimaAction(ActionType actionType):
        actionType_(actionType) {
}

GwAimaAction::GwAimaAction(long code) :
        actionType_(static_cast<ActionType>(code)) {
}

std::unique_ptr<solver::Action> GwAimaAction::copy() const {
    return std::make_unique<GwAimaAction>(actionType_);
}

double GwAimaAction::distanceTo(solver::Action const &/*otherAction*/) const {
    return 0;
}

void GwAimaAction::print(std::ostream &os) const {
    switch (actionType_) {
    case ActionType::NORTH:
        os << "NORTH";
        break;
    case ActionType::EAST:
        os << "EAST";
        break;
    case ActionType::SOUTH:
        os << "SOUTH";
        break;
    case ActionType::WEST:
        os << "WEST";
        break;
    default:
        os << "ERROR-" << static_cast<long>(actionType_);
        break;
    }
}

long GwAimaAction::getBinNumber() const {
    return static_cast<long>(actionType_);
}

ActionType GwAimaAction::getActionType() const {
    return actionType_;
}

} /* namespace gwaima */
