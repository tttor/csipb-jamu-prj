# import library
import time
import operator
import os
import pickle
import shutil
import random
import sys
import numpy as np
from collections import OrderedDict
from collections import defaultdict

# import our costum modules
import config as cfg
import util
import fitness_func as ff
import algor

# import deap and scoop
from deap import tools as deapTools
from deap import base as deapBase
from deap import creator as deapCreator
from deap import gp as deapGP
from deap import algorithms as deapAlgor
from scoop import futures as fu

# These vars are made global for performance when using paralel/distributed computing
#### set D_tr
data, dataDict, dataFeature = util.loadData( cfg.datasetPath )
nClass = len(dataDict)
recallFitnessDict = defaultdict(tuple) # will contain recallFitness values of individuals
simScoreMatDict = dict() # will contain simScore of individuals

#### init Deap GP
# Set Operators and Operands 
# Note: Tanimoto: (a/(a+b+c)), Forbes: ?
nOperand = 4 # at most: a, b, c, d
primitiveSet = deapGP.PrimitiveSet("mainPrimitiveSet", nOperand)
primitiveSet.renameArguments(ARG0="a")
primitiveSet.renameArguments(ARG1="b")
primitiveSet.renameArguments(ARG2="c")
primitiveSet.renameArguments(ARG3="d")

primitiveSet.addPrimitive(np.add, arity=2, name="add")
primitiveSet.addPrimitive(np.subtract, arity=2, name="sub")
primitiveSet.addPrimitive(np.multiply, arity=2, name="mul")
primitiveSet.addPrimitive(util.protectedDiv, arity=2, name="pDiv")
# primitiveSet.addPrimitive(np.minimum, arity=2, name="min")
# primitiveSet.addPrimitive(np.maximum, arity=2, name="max")
# primitiveSet.addPrimitive(np.sqrt, arity=1, name="sqrt")
# primitiveSet.addPrimitive(util.pow, arity=1, name="pow")
# primitiveSet.addPrimitive(util.powhalf, arity=1, name="powhalf")
# primitiveSet.addPrimitive(np.log10, arity=1, name="log")
# primitiveSet.addEphemeralConstant("const", lambda: 0.5)

# Settting up the fitness and the individuals
deapCreator.create("Fitness", deapBase.Fitness, weights=(1.0,))
deapCreator.create("Individual", deapGP.PrimitiveTree, 
                    fitness=deapCreator.Fitness, primitiveSet=primitiveSet)

# Setting up the operator of Genetic Programming 
toolbox = deapBase.Toolbox()
toolbox.register("map", fu.map) # paralel and distributed computing

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

toolbox.register("evaluate", ff.compute, data=data, 
                             recallFitnessDict=recallFitnessDict, simScoreMatDict=simScoreMatDict)

toolbox.register("select", deapTools.selRoulette)# : selRandom, selBest, selWorst, selTournament, selDoubleTournament

toolbox.register("mate", deapGP.cxOnePoint)# :cxOnePointLeafBiased
toolbox.decorate("mate", deapGP.staticLimit(key=operator.attrgetter("height"), max_value=17))

toolbox.register("expr_mut", deapGP.genFull, 
                             min_=cfg.subtreeMinDepthMut, # subtree min depth
                             max_=cfg.subtreeMaxDepthMut) # subtree min depth
toolbox.register("mutate", deapGP.mutUniform, 
                            expr=toolbox.expr_mut,
                            pset=primitiveSet)
toolbox.decorate("mutate", deapGP.staticLimit(key=operator.attrgetter("height"), max_value=17))

toolbox.register("exprTanimoto", util.tanimoto, pset=primitiveSet, min_=cfg.treeMinDepth, max_=cfg.treeMaxDepth)
toolbox.register("indTanimoto", deapTools.initIterate, deapCreator.Individual, toolbox.exprTanimoto)
toolbox.register("popTanimoto", deapTools.initRepeat, list, toolbox.indTanimoto)

def main():
    seed = 318
    random.seed(seed); np.random.seed(seed)

    xprmtDir = cfg.xprmtDir+"/"+"xprmt-"+cfg.xprmtTag+"."+time.strftime("%Y%m%d-%H%M%S")
    os.makedirs(xprmtDir)
    shutil.copy2('config.py', xprmtDir+'/config.py')
    
    stats_fit = deapTools.Statistics(lambda ind: ind.fitness.values)
    stats_size = deapTools.Statistics(len)
    mstats = deapTools.MultiStatistics(fitness=stats_fit, size=stats_size)
    mstats.register("avg", np.mean); mstats.register("std", np.std)
    mstats.register("min", np.min); mstats.register("max", np.max)

    pop = toolbox.population(n=cfg.nIndividual)
    hof = deapTools.HallOfFame(cfg.nHOF) # from all generation of the whole evolution

    # evolution
    print 'Evolution begins ...'
    evolStartTime = time.time()
    pop, log = algor.eaSimple(pop, toolbox, cxpb=cfg.pCx, mutpb=cfg.pMut, ngen=cfg.nMaxGen, 
                              data=data, dataDict=dataDict, 
                              recallFitnessDict=recallFitnessDict, simScoreMatDict=simScoreMatDict,
                              xprmtDir=xprmtDir, stats=mstats, halloffame=hof, verbose=True)
    print("Evolution took %.3f minutes" % ((time.time()-evolStartTime)/60.0))

    # post evolution
    finalDir = xprmtDir + "/final"
    os.makedirs(finalDir) 

    np.savetxt(finalDir + "/individualHOF.csv", [str(i) for i in hof], fmt='%s', delimiter=';')
    np.savetxt(finalDir + "/fitnessHOF.csv", [i.fitness.values for i in hof], fmt='%s', delimiter=';')

    # for i in hof:
    #     print  str(i)
    #     print i.fitness.values
        
    return pop, log, hof

if __name__ == "__main__":
    main()
