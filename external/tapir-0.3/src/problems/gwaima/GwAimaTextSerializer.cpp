/** @file GwAimaTextSerializer.cpp
 *
 * Contains the implementations of the serialization methods for GwAima.
 */
#include "GwAimaTextSerializer.hpp"

#include <iostream>                     // for operator<<, basic_ostream, basic_ostream<>::__ostream_type, basic_istream<>::__istream_type

#include "global.hpp"                     // for make_unique
#include "problems/shared/GridPosition.hpp"  // for GridPosition
#include "solver/abstract-problem/Action.hpp"
#include "solver/abstract-problem/Observation.hpp"
#include "solver/abstract-problem/State.hpp"             // for State
#include "solver/serialization/TextSerializer.hpp"    // for TextSerializer

#include "solver/mappings/actions/enumerated_actions.hpp"
#include "solver/mappings/observations/discrete_observations.hpp"

#include "GwAimaAction.hpp"
#include "GwAimaModel.hpp"
#include "GwAimaObservation.hpp"
#include "GwAimaState.hpp"

namespace solver {
class Solver;
} /* namespace solver */

namespace gwaima {
void saveVector(std::vector<long> values, std::ostream &os) {
    os << "(";
    for (auto it = values.begin(); it != values.end(); it++) {
        os << *it;
        if ((it + 1) != values.end()) {
            os << ", ";
        }
    }
    os << ")";
}

std::vector<long> loadVector(std::istream &is) {
    std::vector<long> values;
    std::string tmpStr;
    std::getline(is, tmpStr, '(');
    std::getline(is, tmpStr, ')');
    std::istringstream sstr(tmpStr);
    while (std::getline(sstr, tmpStr, ',')) {
        long value;
        std::istringstream(tmpStr) >> value;
        values.push_back(value);
    }
    return values;
}

GwAimaTextSerializer::GwAimaTextSerializer(solver::Solver *solver) :
    solver::Serializer(solver) {
}

void GwAimaTextSerializer::saveState(solver::State const *state, std::ostream &os) {
    GwAimaState const &gwAimaState = static_cast<GwAimaState const &>(*state);
    os << gwAimaState.robotPos_.i << " " << gwAimaState.robotPos_.j;
}

std::unique_ptr<solver::State> GwAimaTextSerializer::loadState(std::istream &is) {
    long i, j;
    is >> i >> j;
    GridPosition robotPos(i, j);
    return std::make_unique<GwAimaState>(robotPos);
}

void GwAimaTextSerializer::saveObservation(solver::Observation const *obs,
        std::ostream &os) {
    if (obs == nullptr) {
        os << "()";
    } else {
        GwAimaObservation const &observation = static_cast<GwAimaObservation const &>(
                *obs);
        os << "(" << observation.position_.i << " " << observation.position_.j;
    }
}

std::unique_ptr<solver::Observation> GwAimaTextSerializer::loadObservation(
        std::istream &is) {
    std::string obsString;
    std::getline(is, obsString, '(');
    std::getline(is, obsString, ')');
    if (obsString == "") {
        return nullptr;
    }
    long i, j;
    std::string tmpStr;
    std::istringstream(obsString) >> i >> j >> tmpStr;
    return std::make_unique<GwAimaObservation>(GridPosition(i, j));
}

void GwAimaTextSerializer::saveAction(solver::Action const *action,
        std::ostream &os) {
    if (action == nullptr) {
        os << "NULL";
        return;
    }
    GwAimaAction const &a =
            static_cast<GwAimaAction const &>(*action);
    ActionType code = a.getActionType();
    switch (code) {
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
        os << "ERROR-" << static_cast<long>(code);
        break;
    }
}

std::unique_ptr<solver::Action> GwAimaTextSerializer::loadAction(
        std::istream &is) {
    std::string text;
    is >> text;
    if (text == "NULL") {
        return nullptr;
    } else if (text == "NORTH") {
        return std::make_unique<GwAimaAction>(ActionType::NORTH);
    } else if (text == "EAST") {
        return std::make_unique<GwAimaAction>(ActionType::EAST);
    } else if (text == "SOUTH") {
        return std::make_unique<GwAimaAction>(ActionType::SOUTH);
    } else if (text == "WEST") {
        return std::make_unique<GwAimaAction>(ActionType::WEST);
    } else {
        std::string tmpStr;
        std::istringstream sstr(text);
        std::getline(sstr, tmpStr, '-');
        long code;
        sstr >> code;
        debug::show_message("ERROR: Invalid action!");
        return std::make_unique<GwAimaAction>(
                static_cast<ActionType>(code));
    }
}

int GwAimaTextSerializer::getActionColumnWidth(){
    return 5;
}
int GwAimaTextSerializer::getTPColumnWidth() {
    return 0;
}
int GwAimaTextSerializer::getObservationColumnWidth() {
    return 12;
}
} /* namespace gwaima */
