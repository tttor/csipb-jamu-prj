/** @file smart_history.cpp
 *
 * Contains the implementations for PositionAndJamuData and PositionAndJamuDataTextSerializer.
 */
#include "smart_history.hpp"

#include <iostream>
#include <sstream>

#include "JamuSampleAction.hpp"
#include "JamuSampleObservation.hpp"
#include "JamuSampleModel.hpp"

#include "solver/ActionNode.hpp"
#include "solver/BeliefNode.hpp"

#include "solver/abstract-problem/Action.hpp"

namespace jamusample {
/* ---------------------- PositionAndJamuData --------------------- */
PositionAndJamuData::PositionAndJamuData(JamuSampleModel *model, GridPosition position) :
        model_(model),
        position_(position),
        allJamuData_(model_->getNumberOfJamus()) {
}

PositionAndJamuData::PositionAndJamuData(PositionAndJamuData const &other) :
        model_(other.model_),
        position_(other.position_),
        allJamuData_(other.allJamuData_) {
}

std::unique_ptr<solver::HistoricalData> PositionAndJamuData::copy() const {
    return std::make_unique<PositionAndJamuData>(*this);
}

std::unique_ptr<solver::HistoricalData> PositionAndJamuData::createChild(
        solver::Action const &action, solver::Observation const &observation) const {
    JamuSampleAction const &rsAction = static_cast<JamuSampleAction const &>(action);

    std::unique_ptr<PositionAndJamuData> nextData = (std::make_unique<PositionAndJamuData>(*this));

    bool isLegal;
    std::tie(nextData->position_, isLegal) = model_->makeNextPosition(position_,
            rsAction.getActionType());
    if (!isLegal) {
        debug::show_message("ERROR: An illegal action was taken!?");
        return std::move(nextData);
    }

    if (rsAction.getActionType() == ActionType::SAMPLE) {
        int jamuNo = model_->getCellType(position_) - JamuSampleModel::JAMU;
        nextData->allJamuData_[jamuNo].chanceGood = 0.0;
        nextData->allJamuData_[jamuNo].checkCount = 10;
        nextData->allJamuData_[jamuNo].goodnessNumber = -10;
    } else if (rsAction.getActionType() == ActionType::CHECK) {
        int jamuNo = rsAction.getJamuNo();

        GridPosition jamuPos = model_->getJamuPosition(jamuNo);
        double distance = position_.euclideanDistanceTo(jamuPos);
        double probabilityCorrect = (model_->getSensorCorrectnessProbability(distance));
        double probabilityIncorrect = 1 - probabilityCorrect;

        JamuSampleObservation const &rsObs =
                (static_cast<JamuSampleObservation const &>(observation));

        JamuData &jamuData = nextData->allJamuData_[jamuNo];
        jamuData.checkCount++;
        double likelihoodGood = jamuData.chanceGood;
        double likelihoodBad = 1 - jamuData.chanceGood;
        if (rsObs.isGood()) {
            jamuData.goodnessNumber++;
            likelihoodGood *= probabilityCorrect;
            likelihoodBad *= probabilityIncorrect;
        } else {
            jamuData.goodnessNumber--;
            likelihoodGood *= probabilityIncorrect;
            likelihoodBad *= probabilityCorrect;
        }
        jamuData.chanceGood = likelihoodGood / (likelihoodGood + likelihoodBad);
    }
    return std::move(nextData);
}

std::vector<long> PositionAndJamuData::generateLegalActions() const {
    std::vector<long> legalActions;
    for (std::unique_ptr<solver::DiscretizedPoint> const &action : model_->getAllActionsInOrder()) {
        JamuSampleAction const &rsAction = static_cast<JamuSampleAction const &>(*action);
        GridPosition nextPosition;
        bool isLegal;
        std::tie(nextPosition, isLegal) = model_->makeNextPosition(position_,
                rsAction.getActionType());
        if (isLegal) {
            legalActions.push_back(rsAction.getBinNumber());
        }
    }
    return legalActions;
}

std::vector<long> PositionAndJamuData::generatePreferredActions() const {
    std::vector<long> preferredActions;

    int nJamus = model_->getNumberOfJamus();

    // Check if we're currently on top of a jamu.
    int jamuNo = model_->getCellType(position_) - JamuSampleModel::JAMU;
    // If we are on top of a jamu, and it has more +ve than -ve observations
    // then we will sample it.
    if (jamuNo >= 0 && jamuNo < nJamus) {
        JamuData const &jamuData = allJamuData_[jamuNo];
        if (jamuData.chanceGood == 1.0 || jamuData.goodnessNumber > 0) {
            preferredActions.push_back(static_cast<long>(ActionType::SAMPLE));
            return preferredActions;
        }
    }

    bool worthwhileJamuFound = false;
    bool northWorthwhile = false;
    bool southWorthwhile = false;
    bool eastWorthwhile = false;
    bool westWorthwhile = false;

    // Check to see which jamus are worthwhile.
    for (int i = 0; i < nJamus; i++) {
        JamuData const &jamuData = allJamuData_[i];
        if (jamuData.chanceGood != 0.0 && jamuData.goodnessNumber >= 0) {
            worthwhileJamuFound = true;
            GridPosition pos = model_->getJamuPosition(i);
            if (pos.i > position_.i) {
                southWorthwhile = true;
            } else if (pos.i < position_.i) {
                northWorthwhile = true;
            }

            if (pos.j > position_.j) {
                eastWorthwhile = true;
            } else if (pos.j < position_.j) {
                westWorthwhile = true;
            }
        }
    }
    // If no jamus are worthwhile head east.
    if (!worthwhileJamuFound) {
        preferredActions.push_back(static_cast<long>(ActionType::EAST));
        return preferredActions;
    }

    if (northWorthwhile) {
        preferredActions.push_back(static_cast<long>(ActionType::NORTH));
    }
    if (southWorthwhile) {
        preferredActions.push_back(static_cast<long>(ActionType::SOUTH));
    }
    if (eastWorthwhile) {
        preferredActions.push_back(static_cast<long>(ActionType::EAST));
    }
    if (westWorthwhile) {
        preferredActions.push_back(static_cast<long>(ActionType::WEST));
    }

    // See which jamus we might want to check
    for (int i = 0; i < nJamus; i++) {
        JamuData const &jamuData = allJamuData_[i];
        if (jamuData.chanceGood != 0.0 && jamuData.chanceGood != 1.0
                && std::abs(jamuData.goodnessNumber) < 2) {
            preferredActions.push_back(static_cast<long>(ActionType::CHECK) + i);
        }
    }
    return preferredActions;
}

void PositionAndJamuData::print(std::ostream &os) const {
    os << "Position: " << position_ << std::endl;
    os << "Chances of goodness: ";
    for (JamuData const &jamuData : allJamuData_) {
        tapir::print_double(jamuData.chanceGood, os, 6, 4);
        os << " ";
    }
    os << std::endl;
}

/* --------------------- PreferredActionsTextSerializer -------------------- */
void PositionAndJamuDataTextSerializer::saveHistoricalData(solver::HistoricalData const *data,
        std::ostream &os) {
    os << std::endl;
    os << "CUSTOM DATA:" << std::endl;
    PositionAndJamuData const &prData = (static_cast<PositionAndJamuData const &>(*data));
    os << "Position: " << prData.position_ << std::endl;
    for (JamuData const &jamuData : prData.allJamuData_) {
        os << "p = ";
        tapir::print_double(jamuData.chanceGood, os, 7, 5);
        os << " from " << jamuData.checkCount << " checks ( ";
        os << std::showpos << jamuData.goodnessNumber << std::noshowpos;
        os << " )" << std::endl;
    }
    os << std::endl;
}
std::unique_ptr<solver::HistoricalData> PositionAndJamuDataTextSerializer::loadHistoricalData(
        std::istream &is) {

    std::string line;
    std::getline(is, line); // Blank line
    std::getline(is, line); // Header

    std::getline(is, line);
    std::string tmpStr;
    GridPosition position;
    std::istringstream(line) >> tmpStr >> position;

    JamuSampleModel *model = dynamic_cast<JamuSampleModel *>(getModel());
    std::unique_ptr<PositionAndJamuData> data = (std::make_unique<PositionAndJamuData>(model,
            position));

    for (JamuData &jamuData : data->allJamuData_) {
        std::getline(is, line);
        std::istringstream sstr(line);

        sstr >> tmpStr >> tmpStr >> jamuData.chanceGood;
        sstr >> tmpStr >> jamuData.checkCount >> tmpStr >> tmpStr;
        sstr >> jamuData.goodnessNumber;
    }

    std::getline(is, line); // Blank line

    return std::move(data);
}
} /* namespace jamusample */
