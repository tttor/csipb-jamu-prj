/** @file PreferredActionsPool.cpp
 *
 * Contains the implementation of the mapping classes for dealing with preferred actions in the
 * JamuSample problem, a la POMCP's "smart" tree knowledge.
 */
#include "PreferredActionsPool.hpp"

#include "JamuSampleAction.hpp"
#include "JamuSampleModel.hpp"
#include "smart_history.hpp"

namespace jamusample {
PreferredActionsPool::PreferredActionsPool(JamuSampleModel *model) :
        EnumeratedActionPool(model, model->getAllActionsInOrder()),
        model_(model) {
}

std::vector<long> PreferredActionsPool::createBinSequence(solver::BeliefNode *node) {
    solver::HistoricalData const *data = node->getHistoricalData();
    JamuSampleModel::RSActionCategory category = model_->getSearchActionCategory();
    if (category == JamuSampleModel::RSActionCategory::LEGAL) {
        std::vector<long> bins = static_cast<PositionAndJamuData const *>(data)->generateLegalActions();
        std::shuffle(bins.begin(), bins.end(), *model_->getRandomGenerator());
        return std::move(bins);
    } else if (category == JamuSampleModel::RSActionCategory::PREFERRED) {
        std::vector<long> bins = static_cast<PositionAndJamuData const *>(data)->generatePreferredActions();
        std::shuffle(bins.begin(), bins.end(), *model_->getRandomGenerator());
        return std::move(bins);
    } else {
        return EnumeratedActionPool::createBinSequence(node);
    }
}

std::unique_ptr<solver::ActionMapping> PreferredActionsPool::createActionMapping(
        solver::BeliefNode *node) {
    std::unique_ptr<solver::DiscretizedActionMap> discMap = (
            std::make_unique<solver::DiscretizedActionMap>(node, this, createBinSequence(node)));

    PositionAndJamuData const &data =
            static_cast<PositionAndJamuData const &>(*node->getHistoricalData());

    if (model_->usingPreferredInit()) {
        for (JamuSampleAction const &action : data.generatePreferredActions()) {
            long visitCount = model_->getPreferredVisitCount();
            discMap->getEntry(action)->update(visitCount, visitCount * model_->getPreferredQValue());
        }
    }

    return std::move(discMap);
}
} /* namespace jamusample */
