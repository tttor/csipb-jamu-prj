/** @file GwAimaTextSerializer.hpp
 *
 * Contains text-based serialization methods for the core classes implementing GwAima, that is:
 * TagChange, TagState, TagAction, and TagObservation.
 */
#ifndef GWAIMATEXTSERIALIZER_HPP_
#define GWAIMATEXTSERIALIZER_HPP_

#include <iosfwd>                       // for istream, ostream
#include <memory>                       // for unique_ptr

#include "global.hpp"

#include "solver/abstract-problem/Action.hpp"
#include "solver/abstract-problem/ModelChange.hpp"
#include "solver/abstract-problem/Observation.hpp"
#include "solver/abstract-problem/State.hpp"

#include "solver/mappings/actions/enumerated_actions.hpp"
#include "solver/mappings/observations/discrete_observations.hpp"

#include "solver/serialization/TextSerializer.hpp"    // for TextSerializer

namespace solver {
class Solver;
}  /* namespace solver */

namespace gwaima {
/** A simple method to serialize a vector of longs to an output stream. */
void saveVector(std::vector<long> values, std::ostream &os);
/** A simple method to de-serialize a vector of longs from an input stream. */
std::vector<long> loadVector(std::istream &is);

/** A serialization class for the GwAima problem.
 *
 * This contains serialization methods for GwAimaChange, GwAimaState, GwAimaAction, and GwAimaObservation;
 * this class also inherits from solver::EnumeratedActionTextSerializer in order to serialize
 * the action mappings, and from solver::DiscreteObservationTextSerializer in order to serialize
 * the observation mappings.
 */
class TagTextSerializer: virtual public solver::TextSerializer,
        virtual public solver::EnumeratedActionTextSerializer,
        virtual public solver::DiscreteObservationTextSerializer {
  public:
    /** Creates a new TagTextSerializer instance, associated with the given solver. */
    TagTextSerializer(solver::Solver *solver);

    virtual ~TagTextSerializer() = default;
    _NO_COPY_OR_MOVE(TagTextSerializer);

    void saveState(solver::State const *state, std::ostream &os) override;
    std::unique_ptr<solver::State> loadState(std::istream &is) override;

    void saveObservation(solver::Observation const *obs,
            std::ostream &os) override;
    std::unique_ptr<solver::Observation> loadObservation(
            std::istream &is) override;

    void saveAction(solver::Action const *action, std::ostream &os) override;
    std::unique_ptr<solver::Action> loadAction(std::istream &is) override;


    virtual int getActionColumnWidth() override;
    virtual int getTPColumnWidth() override;
    virtual int getObservationColumnWidth() override;
};
} /* namespace gwaima */

#endif /* GWAIMATEXTSERIALIZER_HPP_ */
