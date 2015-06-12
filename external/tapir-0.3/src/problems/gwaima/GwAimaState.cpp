/** @file GwAimaState.cpp
 *
 * Contains the implementation for the methods of GwAimaState.
 */
#include "GwAimaState.hpp"

#include <cstddef>                      // for size_t

#include <functional>   // for hash
#include <ostream>                      // for operator<<, ostream, basic_ostream>
#include <vector>

#include "global.hpp"
#include "problems/shared/GridPosition.hpp"  // for GridPosition, operator==, operator<<
#include "solver/abstract-problem/State.hpp"             // for State

namespace gwaima {
GwAimaState::GwAimaState(GridPosition robotPos): solver::Vector(), robotPos_(robotPos){
}

GwAimaState::GwAimaState(GwAimaState const &other) :
        GwAimaState(other.robotPos_) {
}

std::unique_ptr<solver::Point> GwAimaState::copy() const {
    return std::make_unique<GwAimaState>(robotPos_);
}

double GwAimaState::distanceTo(solver::State const &otherState) const {
    GwAimaState const &otherGwAimaState = static_cast<GwAimaState const &>(otherState);
    double distance = robotPos_.manhattanDistanceTo(otherGwAimaState.robotPos_);
    return distance;
}

bool GwAimaState::equals(solver::State const &otherState) const {
    GwAimaState const &otherGwAimaState = static_cast<GwAimaState const &>(otherState);
    return (robotPos_ == otherGwAimaState.robotPos_);
}

std::size_t GwAimaState::hash() const {
    std::size_t hashValue = 0;
    tapir::hash_combine(hashValue, robotPos_.i);
    tapir::hash_combine(hashValue, robotPos_.j);    
    return hashValue;
}

std::vector<double> GwAimaState::asVector() const {
    std::vector<double> vec(5);
    vec[0] = robotPos_.i;
    vec[1] = robotPos_.j;
    return vec;
}

void GwAimaState::print(std::ostream &os) const {
    os << "ROBOT: " << robotPos_;
}

GridPosition GwAimaState::getRobotPosition() const {
    return robotPos_;
}

}// namespace gwaima
