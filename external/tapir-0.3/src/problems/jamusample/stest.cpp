/** @file jamusample/stest.cpp
 *
 * Defines the main method for the "stest" executable for the JamuSample POMDP, which tests the
 * serialization methods for JamuSample by deserializing and re-serializing a policy file.
 */
#include "problems/shared/stest.hpp"

#include "JamuSampleModel.hpp"          // for JamuSampleModel
#include "JamuSampleOptions.hpp"        // for JamuSampleOptions

/** The main method for the "stest" executable for JamuSample. */
int main(int argc, char const *argv[]) {
    return stest<jamusample::JamuSampleModel, jamusample::JamuSampleOptions>(argc, argv);
}