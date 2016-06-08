# import library
import time
import random
import operator
import numpy
from collections import OrderedDict
from collections import defaultdict
from operator import itemgetter

import configdataset as cfgData
import config as cfg
import util
import fitness_func as ff

# import deap
from deap import tools as deapTools
from deap import base as deapBase
from deap import creator as deapCreator
from deap import gp as deapGP

def main():
    # Init Training Data
    data = util.loadData(cfg.dataPath[0])

    # init Deap GP
    # Operators and Operands are based on Tanimoto (a/(a+b+c))
    nOperand = 3 # a, b, c
    primitiveSet = deapGP.PrimitiveSet("mainPrimitiveSet", nOperand)
    primitiveSet.renameArguments(ARG0="a")
    primitiveSet.renameArguments(ARG1="b")
    primitiveSet.renameArguments(ARG2="c")

    nTermForAdd = 2
    primitiveSet.addPrimitive(numpy.add, nTermForAdd, name="add")

    nTermForDiv = 2
    primitiveSet.addPrimitive(util.protectedDiv, nTermForDiv)

    # Settting up the fitness and the individuals
    deapCreator.create("FitnessMin", deapBase.Fitness, weights=(-1.0,))
    deapCreator.create("Individual", deapGP.PrimitiveTree, fitness=deapCreator.FitnessMin, primitiveSet=primitiveSet)

    # Setting up the operator of Genetic Programming such as Evaluation, Selection, Crossover, Mutation
    # register the generation functions into a Toolbox
    toolbox = deapBase.Toolbox()
    toolbox.register("expr", deapGP.genHalfAndHalf, # Half-full, halfGrow
                             pset=primitiveSet, 
                             min_=cfg.treeMinDepth, # tree min depth 
                             max_=cfg.treeMaxDepth) # tree min depth

    toolbox.register("individual", deapTools.initIterate, # alternatives: initRepeat, initCycle
                                  deapCreator.Individual, toolbox.expr)

    toolbox.register("population", deapTools.initRepeat, 
                                   list, toolbox.individual)

    toolbox.register("compile", deapGP.compile, 
                                pset=primitiveSet)

    toolbox.register("evaluate", ff.evalRecall)
    toolbox.register("select", deapTools.selRoulette)# : selRandom, selBest, selWorst, selTournament, selDoubleTournament
    toolbox.register("mate", deapGP.cxOnePoint)# :cvOnePointLeafBiased
    toolbox.register("expr_mut", deapGP.genFull, 
                                 min_=cfg.subtreeMinDepthMut, # subtree min depth
                                 max_=cfg.subtreeMinDepthMut) # subtree min depth

    toolbox.register("mutate", deapGP.mutUniform, 
                               expr=toolbox.expr_mut, pset=primitiveSet)

    toolbox.decorate("mate", deapGP.staticLimit(key=operator.attrgetter("height"), max_value=17))
    toolbox.decorate("mutate", deapGP.staticLimit(key=operator.attrgetter("height"), max_value=17))

    while
### GENERATION 0-th
    # init pop    
    pop = toolbox.population(cfg.nPop)

    # Evaluate the entire population
    # invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    for i in range(cfg.maxKendallTrial):
        valid = ff.testKendal(pop,data)
    assert valid

    fitnesses = map(toolbox.evaluate, pop)
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

### EVOLVE GENS
    for g in range(1, cfg.nGen + 1):
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))

        # Apply crossover on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if numpy.random.binomial(1, cfg.pCx):
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        # Apply mutation on the offspring
        for mutant in offspring:
            if numpy.random.binomial(1, cfg.pMut):
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Eval each individual
        for i in range(cfg.maxKendallTrial):
            valid = ff.testKendal(pop,data)
        assert valid
        
        fitnesses = map(toolbox.evaluate, offspring)
        for ind, fit in zip(offspring, fitnesses):
            ind.fitness.values = fit

        # The population is entirely replaced by the offspring
        pop[:] = offspring

        # Stopping criteria
        if ( util.converge() ):
            break

    # Log after evolution
    logstat["0"].append(logbook.chapters["fitness"].select("avg"))
    logstat["1"].append(logbook.chapters["fitness"].select("max"))
    logstat["2"].append(logbook.chapters["fitness"].select("min"))
    logstat["3"].append(logbook.chapters["fitness"].select("std"))

    logstat = OrderedDict(sorted(logstat.items(), key=lambda t: t[0]))
    logPop = OrderedDict(sorted(logPop.items(), key=lambda t: t[0]))
    loghof = OrderedDict(sorted(loghof.items(), key=lambda t: t[0]))

    numpy.savetxt(cfg.xprmtDir+"Logstat-"+cfg.LOGSTAT, numpy.array(logstat.values()),
                    fmt='%s',delimiter=",")
    numpy.savetxt(cfg.xprmtDir+"Fitness -" + cfg.LOGSTAT, logstat.values()[2],
                    fmt='%s', delimiter=",")
    numpy.savetxt(cfg.xprmtDir+"LogPop-"+cfg.LOGPOP, logPop.values(),
                    fmt='%s', delimiter=",")
    numpy.savetxt(cfg.xprmtDir+"Loghof-"+cfg.LOGHOF, loghof.values(),
                    fmt='%s', delimiter=",")
    
    #
    return pop, logbook, hof

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
