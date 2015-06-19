// solve_mdp.cpp
// Solve _merely_ the MDP version of the GwAima problem
#include <fstream>                      // for operator<<, endl, ostream, ofstream, basic_ostream, basic_ostream<>::__ostream_type
#include <iostream>                     // for cout
#include <memory>                       // for unique_ptr
#include <string>                       // for string
#include <utility>                      // for move                // IWYU pragma: keep
#include <cassert>

#include "global.hpp"                     // for RandomGenerator, make_unique
#include "options/option_parser.hpp"
#include "GwAimaMdpSolver.hpp"
#include "GwAimaModel.hpp"
#include "GwAimaState.hpp"

using std::cout;
using std::endl;

/** A template method to calculate an initial policy for the given MDP model and options classes, and
 * then save the policy to a file.
 */
template<typename ModelType, typename OptionsType>
int solve_mdp(int argc, char const *argv[]) {
    using namespace gwaima;

    std::unique_ptr<options::OptionParser> parser = OptionsType::makeParser(false);

    OptionsType options;
    std::string workingDir = tapir::get_current_directory();
    try {
        parser->setOptions(&options);
        parser->parseCmdLine(argc, argv);
        if (!options.baseConfigPath.empty()) {
            tapir::change_directory(options.baseConfigPath);
        }
        if (!options.configPath.empty()) {
            parser->parseCfgFile(options.configPath);
        }
        parser->finalize();
    } catch (options::OptionParsingException const &e) {
        std::cerr << e.what() << std::endl;
        return 2;
    }

    if (!options.baseConfigPath.empty()) {
        tapir::change_directory(workingDir);
    }

    if (options.seed == 0) {
        options.seed = std::time(nullptr);
    }
    cout << "Seed: " << options.seed << endl;
    RandomGenerator randGen;
    randGen.seed(options.seed);
    randGen.discard(10);

    // Define the MDP model of the problem
    ModelType* model;
    model = new ModelType(&randGen,
                          std::make_unique<OptionsType>(options));

    // Define the mdp solver
    std::unique_ptr<gwaima::GwAimaMdpSolver> mdpSolver;  
    mdpSolver = std::make_unique<gwaima::GwAimaMdpSolver>(model);

    //
    mdpSolver->solve();

    // // Vector of valid grid positions.
    // std::vector<GridPosition> emptyCells;
    // emptyCells = model->getEmptyCells();
    // cout << "emptyCells.size()= " << emptyCells.size() << endl;

    // for (GridPosition const &robotPos : emptyCells) {
    //     GwAimaState state(robotPos);
    //     cout << "mdpSolver->getValue(state)= " << mdpSolver->getValue(state) << endl;
    // }

    delete model;
    return 0;
}

int main(int argc, char const *argv[]) {
	return solve_mdp<gwaima::GwAimaModel, gwaima::GwAimaOptions>(argc, argv);
}
