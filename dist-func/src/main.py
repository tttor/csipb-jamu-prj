# import library
import time
import random
import operator
import numpy
import sys
from collections import OrderedDict
from collections import defaultdict
import os
import pickle
import shutil
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

def main(argv):
    # Init Training Data
    # assert len(argv)==2
    # dataPath = argv[1]
    dataPath = cfg.dataPath[4]
    data = util.loadData(dataPath)

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
                                    deapCreator.Individual,
                                    toolbox.expr)

    toolbox.register("population", deapTools.initRepeat,
                                    list,
                                    toolbox.individual)

    toolbox.register("compile", deapGP.compile, 
                                pset=primitiveSet)

    toolbox.register("select", deapTools.selRoulette)# : selRandom, selBest, selWorst, selTournament, selDoubleTournament
    toolbox.register("mate", deapGP.cxOnePoint)# :cvOnePointLeafBiased
    toolbox.register("expr_mut", deapGP.genFull, 
                                 min_=cfg.subtreeMinDepthMut, # subtree min depth
                                 max_=cfg.subtreeMaxDepthMut) # subtree min depth

    toolbox.register("mutate", deapGP.mutUniform, 
                                expr=toolbox.expr_mut,
                                pset=primitiveSet)

    toolbox.decorate("mate", deapGP.staticLimit(key=operator.attrgetter("height"), max_value=17))
    toolbox.decorate("mutate", deapGP.staticLimit(key=operator.attrgetter("height"), max_value=17))

### GENERATION 0-th
    path = cfg.xprmtDir+"/"+"Percobaan001_"+time.strftime("%Y-%m-%d_%H:%M:%S")

    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise

    # Log Pop per Gen
    logPopPerGen = ()
    logFitIndPerGen = ()
    print ('GENERATION 0-th ...............................')
    # init pop    
    pop = toolbox.population(cfg.nPop)

    # Evaluate the entire population
    for i in range(cfg.maxKendallTrial):
        valid,recallRankMat = ff.testKendal(toolbox,pop,data)
        if valid == True:
            break
    assert valid,'Not valid'

    for idx,ind in enumerate(pop):
        fitnessVal = numpy.mean( recallRankMat[idx,:] )
        ind.fitness.values = float(fitnessVal), # must be a tuple here
        logPopPerGen += (ind),
        logFitIndPerGen += (ind.fitness.values),

    pathGen = path+"/Gen 0"
    try:
        os.makedirs(pathGen)
    except OSError:
        if not os.path.isdir(pathGen):
            raise

    numpy.savetxt(pathGen+"/individu.csv", logPopPerGen, fmt='%s',delimiter=",")
    numpy.savetxt(pathGen + "/fitness.csv", logFitIndPerGen, fmt='%s', delimiter=",")

    ###Logging
    hof = deapTools.HallOfFame(1)
    logPop = defaultdict(list)
    logHof = defaultdict(list)
    logStats = defaultdict(list)
    stats_fit = deapTools.Statistics(lambda ind: ind.fitness.values)
    stats_size = deapTools.Statistics(len)
    mstats = deapTools.MultiStatistics(fitness=stats_fit, size=stats_size)
    mstats.register("avg", numpy.mean)
    mstats.register("std", numpy.std)
    mstats.register("min", numpy.min)
    mstats.register("max", numpy.max)
    logbook = deapTools.Logbook()
    logbook.header = ['gen', 'nevals'] + mstats.fields

    hof.update(pop)
    [logPop[0].append(str(i)) for i in pop]
    [logHof[0].append(str(i)) for i in hof]
    
    record = mstats.compile(pop) if mstats else {}
    logbook.record(gen=0, nevals=len(pop), **record)
    
    print logbook.stream
    
    
### EVOLVE GENS
    for g in range(1, cfg.nGen + 1):
        print ('GENERATION '+str(g)+'-th ...............................')
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = map(toolbox.clone, offspring)

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
        
        #log population
        [logPop[g].append(str(i)) for i in offspring]
        
        # Evaluate the entire population
        for i in range(cfg.maxKendallTrial):
            valid,recallRankMat = ff.testKendal(toolbox,offspring,data)
            if valid == True:
                break
        assert valid, 'Not valid'

        logPopPerGen = ()
        logFitIndPerGen = ()
        # Eval each individual
        for idx,ind in enumerate(offspring):
            fitnessVal = numpy.mean( recallRankMat[idx,:] )
            ind.fitness.values = float(fitnessVal), # must be a tuple here
            logPopPerGen += (ind),
            logFitIndPerGen += (ind.fitness.values),

        pathGen = path + "/Gen "+str(g)
        try:
            os.makedirs(pathGen)
        except OSError:
            if not os.path.isdir(pathGen):
                raise

        numpy.savetxt(pathGen + "/individu.csv", logPopPerGen, fmt='%s', delimiter=",")
        numpy.savetxt(pathGen + "/fitness.csv", logFitIndPerGen, fmt='%s', delimiter=",")

        # The population is entirely replaced by the offspring
        pop[:] = offspring

        #log
        hof.update(offspring)
        [logHof[g].append(str(i)) for i in hof]
        
        record = mstats.compile(pop) if mstats else {}
        logbook.record(gen=g, nevals=len(offspring), **record)
        print logbook.stream
        
        # Stopping criteria
        # if ( util.isConverged(offspring) ):
        #     break

    # Log after evolution
    logStats["0"].append(logbook.chapters["fitness"].select("avg"))
    logStats["1"].append(logbook.chapters["fitness"].select("max"))
    logStats["2"].append(logbook.chapters["fitness"].select("min"))
    logStats["3"].append(logbook.chapters["fitness"].select("std"))
    
    logStats = OrderedDict(sorted(logStats.items(), key=lambda t: t[0]))
    logPop = OrderedDict(sorted(logPop.items(), key=lambda t: t[0]))
    logHof = OrderedDict(sorted(logHof.items(), key=lambda t: t[0]))
    
    numpy.savetxt(path+"/stats_summary.csv", numpy.array(logStats.values()),
                    fmt='%s',delimiter=",")
    numpy.savetxt(path+"/fitness_best.csv", logStats.values()[2],
                    fmt='%s', delimiter=",")
    numpy.savetxt(path+"/pop_all.csv", logPop.values(),
                    fmt='%s', delimiter=",")
    numpy.savetxt(path+"/hof_all.csv", logHof.values(),
                    fmt='%s', delimiter=",")

    pickle.dump(logHof[g], open(path+"/hof.p", "wb"))
    shutil.copy2('config.py', path+'/config.py')

    return pop, logbook, hof

if __name__ == "__main__":
    start_time = time.time()
    main(sys.argv)
    print("--- %s seconds ---" % (time.time() - start_time))
