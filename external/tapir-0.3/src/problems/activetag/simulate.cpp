/** @file problems/activetag/simulate.cpp
 *
 * Defines the main method for the "simulate" executable for the ActiveTag POMDP, which runs online
 * simulations to test the performance of the solver.
 */
#include "problems/shared/simulate.hpp"

#include "ActiveTagModel.hpp"                 // for ActiveTagModel
#include "ActiveTagOptions.hpp"               // for ActiveTagOptions

/** The main method for the "simulate" executable for ActiveTag. */
int main(int argc, char const *argv[]) {
    return simulate<activetag::ActiveTagModel, activetag::ActiveTagOptions>(argc, argv);
}
