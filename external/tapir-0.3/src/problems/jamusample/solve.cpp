/** @file jamusample/solve.cpp
 *
 * Defines the main method for the "solve" executable for the JamuSample POMDP, which generates an
 * initial policy.
 */
#include "problems/shared/solve.hpp"

#include "JamuSampleModel.hpp"          // for JamuSampleModel
#include "JamuSampleOptions.hpp"        // for JamuSampleOptions

/** The main method for the "solve" executable for JamuSample. */
int main(int argc, char const *argv[]) {
    return solve<jamusample::JamuSampleModel, jamusample::JamuSampleOptions>(argc, argv);
}
