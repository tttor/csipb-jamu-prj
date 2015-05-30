/** @file LegalActionsPool.hpp
 *
 * Contains an ActionPool implementation for legal actions in JamuSample, which also keeps track of
 * the grid position for each belief node in order to update actions within each mapping to be
 * legal or illegal in response to changes in the model.
 */
#ifndef JAMUSAMPLE_LEGALACTIONSPOOL_HPP_
#define JAMUSAMPLE_LEGALACTIONSPOOL_HPP_

#include <memory>
#include <vector>

#include "solver/mappings/actions/enumerated_actions.hpp"
#include "problems/shared/GridPosition.hpp"

namespace solver {
class HistoricalData;
class Solver;
}

namespace jamusample {
class JamuSampleAction;
class JamuSampleModel;

class LegalActionsMap;

/** An implementation of ActionPool for legal actions in JamuSample.
 *
 * The basic functionality comes from EnumeratedActionPool, but this class creates instances of
 * LegalActionsMap instead of EnumeratedActionMap, and also keeps track of which mappings
 * are located at any given grid position; this allows access to the model in order to set which
 * actions are legal and which are illegal.
 */
class LegalActionsPool: public solver::EnumeratedActionPool {
  public:
    /** Constructs a new LegalActionsPool associated with the given model. */
    LegalActionsPool(JamuSampleModel *model);
    virtual ~LegalActionsPool() = default;
    _NO_COPY_OR_MOVE(LegalActionsPool);

    virtual std::vector<long> createBinSequence(solver::BeliefNode *node) override;

    virtual std::unique_ptr<solver::ActionMapping> createActionMapping(
            solver::BeliefNode *node) override;

    /** Adds a mapping to the saved entries for a given grid position. */
    virtual void addMapping(GridPosition position, LegalActionsMap *map);
    /** Removes a mapping from the saved entries for a given grid position. */
    virtual void removeMapping(GridPosition position, LegalActionsMap *map);

    /** Sets the legality of the given action from the current position.
     *
     * If the solver is not nullptr, it will be queried for which belief nodes are affected
     * by the current changes, so that only affected belief nodes will be modified. */
    virtual void setLegal(bool isLegal, GridPosition position, JamuSampleAction const &action,
            solver::Solver *solver);
  private:
    /** The JamuSampleModel instance this pool is associated with. */
    JamuSampleModel *model_;
    /** A mapping of grid positions to the set of actionmap. */
    std::unordered_map<GridPosition, std::unordered_set<LegalActionsMap *>> mappings_;
};

/** A custom mapping class that keeps track of which actions are legal or illegal at each belief
 * in JamuSample, even after changes have been applied.
 */
class LegalActionsMap : public solver::DiscretizedActionMap {
public:
    /** Creates a new mapping for the given belief node.
     *
     * On construction, this mapping which will be associated with the given pool, using the grid
     * position stored within the belief node. The given sequence of bins defines the legal actions
     * and the order in which they will be tried.
     */
    LegalActionsMap(solver::BeliefNode *owner, LegalActionsPool *pool, std::vector<long> binSequence);
    /** Destroys this mapping instance.
     *
     * This will also dissociate this mapping from its pool, and also destroy any children of
     * this mapping.
     */
    ~LegalActionsMap();
};

/** A custom serialization class to handle loading of LegalActionsMap instances from a file.
 *
 * This class inherits saveActionMapping() from the DiscretizedActionTextSerializer class, as
 * that functionality is OK. However, loadActionMapping must be changed in order to construct
 * an instance of LegalActionsMap instead of an instance of solver::DiscretizedActionMap.
 */
class LegalActionsPoolTextSerializer: virtual public solver::DiscretizedActionTextSerializer {
  public:
    LegalActionsPoolTextSerializer() = default;
    virtual ~LegalActionsPoolTextSerializer() = default;
    _NO_COPY_OR_MOVE(LegalActionsPoolTextSerializer);

    virtual std::unique_ptr<solver::ActionMapping> loadActionMapping(solver::BeliefNode *node,
            std::istream &is) override;
};
} /* namespace jamusample */

#endif /* JAMUSAMPLE_LEGALACTIONSPOOL_HPP_ */
