/** @file problems/activetag/solve.cpp
 *
 * Defines the main method for the "solve" executable for the ActiveTag POMDP, which generates an
 * initial policy.
 */
#include "problems/shared/solve.hpp"

#include "ActiveTagModel.hpp"                 // for ActiveTagModel
#include "ActiveTagOptions.hpp"               // for ActiveTagOptions

/** The main method for the "solve" executable for ActiveTag. */
int main(int argc, char const *argv[]) {
    return solve<activetag::ActiveTagModel, activetag::ActiveTagOptions>(argc, argv);
}
