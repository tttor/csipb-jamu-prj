/** @file GwAimaOptions.hpp
 *
 * Defines the GwAimaOptions class, which specifies the configuration settings available for the
 * GwAima problem.
 */
#ifndef GWAIMAOPTIONS_HPP_
#define GWAIMAOPTIONS_HPP_

#include <string>                       // for string

#include "problems/shared/SharedOptions.hpp"

namespace gwaima {
/** A class defining the configuration settings for the GwAima problem. */
struct GwAimaOptions : public shared::SharedOptions {
    GwAimaOptions() = default;
    virtual ~GwAimaOptions() = default;

    /* -------- Settings specific to the GwAima POMDP -------- */
    /** Path to the map file (relative to SharedOptions::baseConfigPath) */
    std::string mapPath = "";
    /** Cost per move. */
    double moveCost = 0.0;
    /** Cost per being in the boom cell. */
    double boomCost = 0.0;
    /** Reward per being in the goal cell. */
    double goalReward = 0.0;
    /** Path to vrep scene gwaima.ttt */
    std::string vrepScenePath = "";

    /** Constructs an OptionParser instance that will parse configuration settings for the GwAima
     * problem into an instance of GwAimaOptions.
     */
    static std::unique_ptr<options::OptionParser> makeParser(bool simulating) {
        std::unique_ptr<options::OptionParser> parser = SharedOptions::makeParser(simulating,
                EXPAND_AND_QUOTE(ROOT_PATH) "/problems/gwaima");
        addGwAimaOptions(parser.get());
        return std::move(parser);
    }

    /** Adds the core configuration settings for the GwAima problem to the given parser. */
    static void addGwAimaOptions(options::OptionParser *parser) {
        parser->addOption<std::string>("problem", "mapPath", &GwAimaOptions::mapPath);
        parser->addValueArg<std::string>("problem", "mapPath", &GwAimaOptions::mapPath,
                "", "map", "the path to the map file (relative to the base config path)", "path");

        parser->addOption<double>("problem", "moveCost", &GwAimaOptions::moveCost);
        parser->addOption<double>("problem", "boomCost", &GwAimaOptions::boomCost);
        parser->addOption<double>("problem", "goalReward", &GwAimaOptions::goalReward);

        parser->addOptionWithDefault<std::string>("ros", "vrepScenePath", &GwAimaOptions::vrepScenePath, "");
    }
};
} /* namespace gwaima */

#endif /* GWAIMAOPTIONS_HPP_ */
