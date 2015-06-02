/** @file ActiveTagState.cpp
 *
 * Contains the implementation for the methods of ActiveTagState.
 */
#include "ActiveTagState.hpp"

#include <cstddef>                      // for size_t

#include <functional>   // for hash
#include <ostream>                      // for operator<<, ostream, basic_ostream>
#include <vector>

#include "global.hpp"
#include "problems/shared/GridPosition.hpp"  // for GridPosition, operator==, operator<<
#include "solver/abstract-problem/State.hpp"             // for State

namespace activetag {
ActiveTagState::ActiveTagState(GridPosition robotPos, GridPosition opponentPos,
        bool _isTagged) :
    solver::Vector(),
    robotPos_(robotPos),
    opponentPos_(opponentPos),
    isTagged_(_isTagged) {
}

ActiveTagState::ActiveTagState(ActiveTagState const &other) :
        ActiveTagState(other.robotPos_, other.opponentPos_, other.isTagged_) {
}

std::unique_ptr<solver::Point> ActiveTagState::copy() const {
    return std::make_unique<ActiveTagState>(robotPos_, opponentPos_, isTagged_);
}

double ActiveTagState::distanceTo(solver::State const &otherState) const {
    ActiveTagState const &otherTagState = static_cast<ActiveTagState const &>(otherState);
    double distance = robotPos_.manhattanDistanceTo(otherTagState.robotPos_);
    distance += opponentPos_.manhattanDistanceTo(otherTagState.opponentPos_);
    distance += (isTagged_ == otherTagState.isTagged_) ? 0 : 1;
    return distance;
}

bool ActiveTagState::equals(solver::State const &otherState) const {
    ActiveTagState const &otherTagState = static_cast<ActiveTagState const &>(otherState);
    return (robotPos_ == otherTagState.robotPos_
            && opponentPos_ == otherTagState.opponentPos_
            && isTagged_ == otherTagState.isTagged_);
}

std::size_t ActiveTagState::hash() const {
    std::size_t hashValue = 0;
    tapir::hash_combine(hashValue, robotPos_.i);
    tapir::hash_combine(hashValue, robotPos_.j);
    tapir::hash_combine(hashValue, opponentPos_.i);
    tapir::hash_combine(hashValue, opponentPos_.j);
    tapir::hash_combine(hashValue, isTagged_);
    return hashValue;
}

std::vector<double> ActiveTagState::asVector() const {
    std::vector<double> vec(5);
    vec[0] = robotPos_.i;
    vec[1] = robotPos_.j;
    vec[2] = opponentPos_.i;
    vec[3] = opponentPos_.j;
    vec[4] = isTagged_ ? 1 : 0;
    return vec;
}

void ActiveTagState::print(std::ostream &os) const {
    os << "ROBOT: " << robotPos_ << " OPPONENT: " << opponentPos_;
    if (isTagged_) {
        os << " TAGGED!";
    }
}


GridPosition ActiveTagState::getRobotPosition() const {
    return robotPos_;
}

GridPosition ActiveTagState::getOpponentPosition() const {
    return opponentPos_;
}

bool ActiveTagState::isTagged() const {
    return isTagged_;
}
} /* namespace activetag */
