/** @file JamuSampleTextSerializer.cpp
 *
 * Contains the implementations of the serialization methods for JamuSample.
 */
#include "JamuSampleTextSerializer.hpp"

#include <iostream>                     // for operator<<, basic_ostream, basic_istream<>::__istream_type, basic_ostream<>::__ostream_type, endl
#include <string>                       // for operator>>, string
#include <vector>                       // for vector

#include "global.hpp"                     // for make_unique
#include "problems/shared/GridPosition.hpp"  // for GridPosition

#include "solver/abstract-problem/Action.hpp"
#include "solver/abstract-problem/State.hpp"
#include "solver/abstract-problem/Observation.hpp"

#include "solver/mappings/actions/enumerated_actions.hpp"
#include "solver/mappings/observations/enumerated_observations.hpp"

#include "solver/serialization/TextSerializer.hpp"    // for TextSerializer

#include "JamuSampleAction.hpp"         // for JamuSampleAction
#include "JamuSampleObservation.hpp"    // for JamuSampleObservation
#include "JamuSampleState.hpp"          // for JamuSampleState
#include "JamuSampleModel.hpp"

namespace solver {
class Solver;
} /* namespace solver */

namespace jamusample {
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

JamuSampleTextSerializer::JamuSampleTextSerializer(solver::Solver *solver) :
        Serializer(solver) {
}

/* ------------------ Saving change sequences -------------------- */
void JamuSampleTextSerializer::saveModelChange(solver::ModelChange const &change, std::ostream &os) {
    JamuSampleChange const &rsChange = static_cast<JamuSampleChange const &>(change);
    os << rsChange.changeType;
    os << ": ";
    saveVector(std::vector<long> {rsChange.i0, rsChange.j0}, os);
    os << " ";
    saveVector(std::vector<long> {rsChange.i1, rsChange.j1}, os);
}


std::unique_ptr<solver::ModelChange> JamuSampleTextSerializer::loadModelChange(std::istream &is) {
    std::unique_ptr<JamuSampleChange> change = std::make_unique<JamuSampleChange>();
    std::getline(is, change->changeType, ':');
    std::vector<long> v0 = loadVector(is);
    std::vector<long> v1 = loadVector(is);
    change->i0 = v0[0];
    change->j0 = v0[1];
    change->i1 = v1[0];
    change->j1 = v1[1];
    return std::move(change);
}

void JamuSampleTextSerializer::saveState(solver::State const *state, std::ostream &os) {
    if (state == nullptr) {
        os << "NULL";
        return;
    }
    JamuSampleState const &jamuSampleState = static_cast<JamuSampleState const &>(*state);
    os << jamuSampleState.position_.i << " " << jamuSampleState.position_.j << " ";
    for (bool isGood : jamuSampleState.getJamuStates()) {
        if (isGood) {
            os << 'G';
        } else {
            os << 'B';
        }
    }
}

std::unique_ptr<solver::State> JamuSampleTextSerializer::loadState(std::istream &is) {
    std::string text;
    is >> text;
    if (text == "NULL") {
        return nullptr;
    }
    long i, j;
    std::istringstream(text) >> i;
    std::string jamuString;
    std::vector<bool> jamuStates;

    is >> j >> jamuString;
    for (char c : jamuString) {
        if (c == 'G') {
            jamuStates.push_back(true);
        } else if (c == 'B') {
            jamuStates.push_back(false);
        } else {
            std::ostringstream message;
            message << "ERROR: Invalid jamu state: " << c;
            debug::show_message(message.str());
        }
    }
    return std::make_unique<JamuSampleState>(GridPosition(i, j), jamuStates);
}

void JamuSampleTextSerializer::saveObservation(solver::Observation const *obs, std::ostream &os) {
    if (obs == nullptr) {
        os << "NULL";
        return;
    }
    JamuSampleObservation const &observation = static_cast<JamuSampleObservation const &>(*obs);
    if (observation.isEmpty()) {
        os << "NONE";
    } else if (observation.isGood_) {
        os << "GOOD";
    } else {
        os << "BAD";
    }
}

std::unique_ptr<solver::Observation> JamuSampleTextSerializer::loadObservation(std::istream &is) {
    std::string text;
    is >> text;
    if (text == "NULL") {
        return nullptr;
    } else if (text == "NONE") {
        return std::make_unique<JamuSampleObservation>(true, true);
    } else if (text == "GOOD") {
        return std::make_unique<JamuSampleObservation>(false, true);
    } else if (text == "BAD") {
        return std::make_unique<JamuSampleObservation>(false, false);
    } else {
        debug::show_message("ERROR: Invalid observation!");
        return nullptr;
    }
}

void JamuSampleTextSerializer::saveAction(solver::Action const *action, std::ostream &os) {
    if (action == nullptr) {
        os << "NULL";
        return;
    }
    JamuSampleAction const &a = static_cast<JamuSampleAction const &>(*action);
    ActionType code = a.getActionType();
    if (code == ActionType::CHECK) {
        os << "CHECK-" << a.getJamuNo();
        return;
    }
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
    case ActionType::SAMPLE:
        os << "SAMPLE";
        break;
    default:
        os << "ERROR-" << static_cast<long>(code);
        break;
    }
}

std::unique_ptr<solver::Action> JamuSampleTextSerializer::loadAction(std::istream &is) {
    std::string text;
    is >> text;
    if (text == "NULL") {
        return nullptr;
    } else if (text == "NORTH") {
        return std::make_unique<JamuSampleAction>(ActionType::NORTH);
    } else if (text == "EAST") {
        return std::make_unique<JamuSampleAction>(ActionType::EAST);
    } else if (text == "SOUTH") {
        return std::make_unique<JamuSampleAction>(ActionType::SOUTH);
    } else if (text == "WEST") {
        return std::make_unique<JamuSampleAction>(ActionType::WEST);
    } else if (text == "SAMPLE") {
        return std::make_unique<JamuSampleAction>(ActionType::SAMPLE);
    } else if (text.find("CHECK") != std::string::npos) {
        std::string tmpStr;
        std::istringstream sstr(text);
        std::getline(sstr, tmpStr, '-');
        long jamuNo;
        sstr >> jamuNo;
        return std::make_unique<JamuSampleAction>(ActionType::CHECK, jamuNo);
    } else {
        std::string tmpStr;
        std::istringstream sstr(text);
        std::getline(sstr, tmpStr, '-');
        long code;
        sstr >> code;
        std::ostringstream message;
        message << "ERROR: Invalid action; code " << code;
        debug::show_message(message.str());
        return std::make_unique<JamuSampleAction>(static_cast<ActionType>(code));
    }
}

int JamuSampleTextSerializer::getActionColumnWidth() {
    return 7;
}
int JamuSampleTextSerializer::getTPColumnWidth() {
    return 0;
}
int JamuSampleTextSerializer::getObservationColumnWidth() {
    return 4;
}

JamuSampleBasicTextSerializer::JamuSampleBasicTextSerializer(solver::Solver *solver) :
        Serializer(solver) {
}
JamuSampleLegalActionsTextSerializer::JamuSampleLegalActionsTextSerializer(solver::Solver *solver) :
        Serializer(solver) {
}
JamuSamplePreferredActionsTextSerializer::JamuSamplePreferredActionsTextSerializer(
        solver::Solver *solver) :
        Serializer(solver) {
}
} /* namespace jamusample */
