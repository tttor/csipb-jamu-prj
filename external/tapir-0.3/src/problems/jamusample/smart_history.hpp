/** @file smart_history.hpp
 *
 * Defines a class to keep track of the position of the robot in JamuSample, as well as explicitly
 * calculated probabilities for the goodness of each jamu.
 */
#ifndef JAMUSAMPLE_SMART_HISTORY_HPP_
#define JAMUSAMPLE_SMART_HISTORY_HPP_

#include "solver/abstract-problem/HistoricalData.hpp"

#include "solver/serialization/TextSerializer.hpp"

#include "problems/shared/GridPosition.hpp"

namespace jamusample {
class JamuSampleAction;
class JamuSampleModel;

/** Stores data about each jamu.
 */
struct JamuData {
    /** The number of times this jamu has been checked. */
    long checkCount = 0;
    /** The "goodness number"; +1 for each good observation of this jamu, and -1 for each bad
     * observation of this jamu.
     */
    long goodnessNumber = 0;
    /** The calculated probability that this jamu is good. */
    double chanceGood = 0.5;
};

/** A class to store the robot position associated with a given belief node, as well as
 * explicitly calculated probabilities of goodness for each jamu.
 */
class PositionAndJamuData : public solver::HistoricalData {
    friend class PreferredActionsMap;
    friend class PositionAndJamuDataTextSerializer;
public:
    /** Constructs a new PositionAndJamuData instance for the given model, in the given position,
     * with default data values for each jamu.
     */
    PositionAndJamuData(JamuSampleModel *model, GridPosition position);
    virtual ~PositionAndJamuData() = default;

    /** We define a copy constructor for this class, for convenience. */
    PositionAndJamuData(PositionAndJamuData const &other);
    /** Deleted move constructor. */
    PositionAndJamuData(PositionAndJamuData &&other) = delete;
    /** Deleted copy assignment operator. */
    PositionAndJamuData &operator=(PositionAndJamuData const &other) = delete;
    /** Deleted move assignment operator. */
    PositionAndJamuData &operator=(PositionAndJamuData &&other) = delete;

    std::unique_ptr<solver::HistoricalData> copy() const;

    std::unique_ptr<solver::HistoricalData> createChild(
            solver::Action const &action,
            solver::Observation const &observation) const override;

    /** Generates the legal actions that are available from this position. */
    std::vector<long> generateLegalActions() const;
    /** Generates a set of preferred actions, based on the knowledge stored in this
     * instance.
     */
    std::vector<long> generatePreferredActions() const;

    void print(std::ostream &os) const override;

private:
    /** The associated model instance. */
    JamuSampleModel *model_;
    /** The grid position. */
    GridPosition position_;
    /** The data for each jamu, in order of jamu number. */
    std::vector<JamuData> allJamuData_;
};

/** An implementation of the serialization methods for the
 * PositionAndJamuDataTextSerializer class.
 */
class PositionAndJamuDataTextSerializer : virtual public solver::TextSerializer {
public:
    void saveHistoricalData(solver::HistoricalData const *data, std::ostream &os) override;
    std::unique_ptr<solver::HistoricalData> loadHistoricalData(std::istream &is) override;
};
} /* namespace jamusample */

#endif /* JAMUSAMPLE_SMART_HISTORY_HPP_ */
