/** @file ActiveTagOptions.hpp
 *
 * Defines the ActiveTagOptions class, which specifies the configuration settings available for the
 * Tag problem.
 */
#ifndef ACTIVETAGOPTIONS_HPP_
#define ACTIVETAGOPTIONS_HPP_

#include <string>                       // for string

#include "problems/shared/SharedOptions.hpp"

namespace activetag {
/** A class defining the configuration settings for the Tag problem. */
struct ActiveTagOptions : public shared::SharedOptions {
    ActiveTagOptions() = default;
    virtual ~ActiveTagOptions() = default;

    /* -------- Settings specific to the Tag POMDP -------- */
    /** Path to the map file (relative to SharedOptions::baseConfigPath) */
    std::string mapPath = "";
    /** Cost per move. */
    double moveCost = 0.0;
    /** Reward for tagging. */
    double tagReward = 0.0;
    /** Penalty for a failed tag attempt. */
    double failedTagPenalty = 0.0;
    /** Probability the opponent will stay in place. */
    double opponentStayProbability = 0.0;
    /** Path to vrep scene tag.ttt */
    std::string vrepScenePath = "";

    /** Constructs an OptionParser instance that will parse configuration settings for the Tag
     * problem into an instance of ActiveTagOptions.
     */
    static std::unique_ptr<options::OptionParser> makeParser(bool simulating) {
        std::unique_ptr<options::OptionParser> parser = SharedOptions::makeParser(simulating,
                EXPAND_AND_QUOTE(ROOT_PATH) "/problems/activetag");
        addTagOptions(parser.get());
        return std::move(parser);
    }

    /** Adds the core configuration settings for the Tag problem to the given parser. */
    static void addTagOptions(options::OptionParser *parser) {
        parser->addOption<std::string>("problem", "mapPath", &ActiveTagOptions::mapPath);
        parser->addValueArg<std::string>("problem", "mapPath", &ActiveTagOptions::mapPath,
                "", "map", "the path to the map file (relative to the base config path)", "path");

        parser->addOption<double>("problem", "moveCost", &ActiveTagOptions::moveCost);
        parser->addOption<double>("problem", "tagReward", &ActiveTagOptions::tagReward);
        parser->addOption<double>("problem", "failedTagPenalty", &ActiveTagOptions::failedTagPenalty);
        parser->addOption<double>("problem", "opponentStayProbability",
                &ActiveTagOptions::opponentStayProbability);
        parser->addOptionWithDefault<std::string>("ros", "vrepScenePath",
                &ActiveTagOptions::vrepScenePath, "");
    }
};
} /* namespace activetag */

#endif /* ACTIVETAGOPTIONS_HPP_ */
