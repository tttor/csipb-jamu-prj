/** @file JamuSampleOptions.hpp
 *
 * Defines the JamuSampleOptions class, which specifies the configuration settings available for the
 * JamuSample problem.
 */
#ifndef JAMUSAMPLE_OPTIONS_HPP_
#define JAMUSAMPLE_OPTIONS_HPP_

#include <string>                       // for string

#include "problems/shared/SharedOptions.hpp"

namespace jamusample {
/** A class defining the configuration settings for the JamuSample problem. */
struct JamuSampleOptions : public shared::SharedOptions {
    JamuSampleOptions() = default;
    virtual ~JamuSampleOptions() = default;

    /* -------- Settings specific to the JamuSample POMDP -------- */
    /** Path to the map file. */
    std::string mapPath = "";
    /** Reward for a good jamu. */
    double goodJamuReward = 0.0;
    /** Penalty for a bad jamu. */
    double badJamuPenalty = 0.0;
    /** Reward for exiting the map. */
    double exitReward = 0.0;
    /** Penalty for an illegal move. */
    double illegalMovePenalty = 0.0;
    /** half-efficiency distance. */
    double halfEfficiencyDistance = 0.0;


    /* -------- Settings for JamuSample-specific heuristics -------- */
    /** The nature of the extra history-based data stored at each belief node. */
    std::string heuristicType = "";
    /** Restriction of search actions. */
    std::string searchHeuristicType = "";
    /** Restriction of rollout actions. */
    std::string rolloutHeuristicType = "";
    /** Whether to initialise Q-values for preferred actions with a prior bias. */
    bool usePreferredInit = false;
    /** If a bias is used, the q-value for the preferred actions. */
    double preferredQValue = 0.0;
    /** If a bias is used, the visit count for the preferred actions. */
    long preferredVisitCount = 0;

    /** Constructs an OptionParser instance that will parse configuration settings for the
     * JamuSample problem into an instance of JamuSampleOptions.
     */
    static std::unique_ptr<options::OptionParser> makeParser(bool simulating) {
        std::unique_ptr<options::OptionParser> parser = SharedOptions::makeParser(simulating,
                EXPAND_AND_QUOTE(ROOT_PATH) "/problems/jamusample");
        addJamuSampleOptions(parser.get());
        addHeuristicOptions(parser.get());
        return std::move(parser);
    }

    /** Adds the core configuration settings for the RpckSample problem to the given parser. */
    static void addJamuSampleOptions(options::OptionParser *parser) {
        parser->addOption<std::string>("problem", "mapPath", &JamuSampleOptions::mapPath);
        parser->addValueArg<std::string>("problem", "mapPath", &JamuSampleOptions::mapPath,
                "", "map", "the path to the map file (relative to the base config path)", "path");

        parser->addOption<double>("problem", "goodJamuReward", &JamuSampleOptions::goodJamuReward);
        parser->addOption<double>("problem", "badJamuPenalty", &JamuSampleOptions::badJamuPenalty);
        parser->addOption<double>("problem", "exitReward", &JamuSampleOptions::exitReward);
        parser->addOption<double>("problem", "illegalMovePenalty", &JamuSampleOptions::illegalMovePenalty);
        parser->addOption<double>("problem", "halfEfficiencyDistance", &JamuSampleOptions::halfEfficiencyDistance);
    }

    /** Adds configuration options specific to the management of history-based data, e.g. the
     * fully observed state, for JamuSample.
     */
    static void addHeuristicOptions(options::OptionParser *parser) {
        parser->addOption<std::string>("heuristics", "type", &JamuSampleOptions::heuristicType);
        parser->addOption<std::string>("heuristics", "search", &JamuSampleOptions::searchHeuristicType);
        parser->addOption<std::string>("heuristics", "rollout", &JamuSampleOptions::rolloutHeuristicType);

        parser->addOptionWithDefault<bool>("heuristics", "usePreferredInit", &JamuSampleOptions::usePreferredInit, false);
        parser->addOption<double>("heuristics", "preferredQValue", &JamuSampleOptions::preferredQValue);
        parser->addOption<long>("heuristics", "preferredVisitCount", &JamuSampleOptions::preferredVisitCount);
    }
};
} /* namespace jamusample */

#endif /* JAMUSAMPLE_OPTIONS_HPP_ */
