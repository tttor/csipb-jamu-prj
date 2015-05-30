/** @file jamusample/simulate.cpp
 *
 * Defines the main method for the "simulate" executable for the JamuSample POMDP, which runs
 * online simulations to test the performance of the solver.
 */
#include "problems/shared/simulate.hpp"

#include "JamuSampleModel.hpp"          // for JamuSampleModel
#include "JamuSampleOptions.hpp"        // for JamuSampleOptions

/** The main method for the "simulate" executable for JamuSample. */
int main(int argc, char const *argv[]) {
    return simulate<jamusample::JamuSampleModel, jamusample::JamuSampleOptions>(argc, argv);
}
