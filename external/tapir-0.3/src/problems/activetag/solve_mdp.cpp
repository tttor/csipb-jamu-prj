// solve_mdp.cpp
// Solve _merely_ the MDP version of the ActiveTag problem
#include <fstream>                      // for operator<<, endl, ostream, ofstream, basic_ostream, basic_ostream<>::__ostream_type
#include <iostream>                     // for cout
#include <memory>                       // for unique_ptr
#include <string>                       // for string
#include <utility>                      // for move                // IWYU pragma: keep

#include "global.hpp"                     // for RandomGenerator, make_unique
#include "options/option_parser.hpp"
#include "ActiveTagMdpSolver.hpp"
#include "ActiveTagModel.hpp"

using std::cout;
using std::endl;

/** A template method to calculate an initial policy for the given MDP model and options classes, and
 * then save the policy to a file.
 */
template<typename ModelType, typename OptionsType>
int solve_mdp(int argc, char const *argv[]) {
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

    // if (options.seed == 0) {
    //     options.seed = std::time(nullptr);
    // }
    // cout << "Seed: " << options.seed << endl;
    // RandomGenerator randGen;
    // randGen.seed(options.seed);
    // randGen.discard(10);

    // std::unique_ptr<ModelType> newModel = std::make_unique<ModelType>(&randGen,
    //         std::make_unique<OptionsType>(options));
    // if (!options.baseConfigPath.empty()) {
    //     tapir::change_directory(workingDir);
    // }

    // solver::Solver solver(std::move(newModel));
    // solver.initializeEmpty();

    // double totT;
    // double tStart;
    // tStart = tapir::clock_ms();

    // solver.improvePolicy();

    // totT = tapir::clock_ms() - tStart;
    // cout << "Total solving time: " << totT << "ms" << endl;

    // cout << "Saving to file...";
    // cout.flush();
    // std::ofstream outFile(options.policyPath);
    // outFile << std::setprecision(std::numeric_limits<double>::max_digits10);
    // solver.getSerializer()->save(outFile);
    // outFile.close();
    // cout << "    Done." << endl;

    return 0;
}


int main(int argc, char const *argv[]) {
	return solve_mdp<activetag::ActiveTagModel, activetag::ActiveTagOptions>(argc, argv);

	// // Define the MDP model
	// std::unique_ptr<ActiveTagModel> activeTagModel;
	// activeTagModel = std::make_unique<ActiveTagModel>(&randGen, std::make_unique<OptionsType>(options));

	// std::unique_ptr<ActiveTagMdpSolver> mdpSolver_;	
 //    mdpSolver_ = std::make_unique<ActiveTagMdpSolver>(this);

 //    mdpSolver_->solve();

	// return 0;
}