import os
import numpy as np
from deap import tools
from deap import algorithms as deapAlgor

import util

'''
Shamelessly copied from 
deap-1.0.2/deap/algorithms.py
'''
def eaSimple(population, toolbox, cxpb, mutpb, ngen, 
             data, dataDict, recallFitnessDict, simScoreMatDict,
             xprmtDir=None, stats=None, halloffame=None, verbose=__debug__):
    """This algorithm reproduce the simplest evolutionary algorithm as
    presented in chapter 7 of [Back2000]_.
    
    :param population: A list of individuals.
    :param toolbox: A :class:`~deap.base.Toolbox` that contains the evolution
                    operators.
    :param cxpb: The probability of mating two individuals.
    :param mutpb: The probability of mutating an individual.
    :param ngen: The number of generation.
    :param stats: A :class:`~deap.tools.Statistics` object that is updated
                  inplace, optional.
    :param halloffame: A :class:`~deap.tools.HallOfFame` object that will
                       contain the best individuals, optional.
    :param verbose: Whether or not to log the statistics.
    :returns: The final population and a :class:`~deap.tools.Logbook`
              with the statistics of the evolution.
    
    The algorithm takes in a population and evolves it in place using the
    :meth:`varAnd` method. It returns the optimized population and a
    :class:`~deap.tools.Logbook` with the statistics of the evolution (if
    any). The logbook will contain the generation number, the number of
    evalutions for each generation and the statistics if a
    :class:`~deap.tools.Statistics` if any. The *cxpb* and *mutpb* arguments
    are passed to the :func:`varAnd` function. The pseudocode goes as follow
    ::

        evaluate(population)
        for g in range(ngen):
            population = select(population, len(population))
            offspring = varAnd(population, toolbox, cxpb, mutpb)
            evaluate(offspring)
            population = offspring

    As stated in the pseudocode above, the algorithm goes as follow. First, it
    evaluates the individuals with an invalid fitness. Second, it enters the
    generational loop where the selection procedure is applied to entirely
    replace the parental population. The 1:1 replacement ratio of this
    algorithm **requires** the selection procedure to be stochastic and to
    select multiple times the same individual, for example,
    :func:`~deap.tools.selTournament` and :func:`~deap.tools.selRoulette`.
    Third, it applies the :func:`varAnd` function to produce the next
    generation population. Fourth, it evaluates the new individuals and
    compute the statistics on this population. Finally, when *ngen*
    generations are done, the algorithm returns a tuple with the final
    population and a :class:`~deap.tools.Logbook` of the evolution.

    .. note::

        Using a non-stochastic selection method will result in no selection as
        the operator selects *n* individuals from a pool of *n*.
    
    This function expects the :meth:`toolbox.mate`, :meth:`toolbox.mutate`,
    :meth:`toolbox.select` and :meth:`toolbox.evaluate` aliases to be
    registered in the toolbox.
    
    .. [Back2000] Back, Fogel and Michalewicz, "Evolutionary Computation 1 :
       Basic Algorithms and Operators", 2000.
    """
    logbook = tools.Logbook()
    logbook.header = ['gen'] + (stats.fields if stats else [])

    # Evaluate the individuals with an invalid fitness
    tmpRecallRankDict = util.getRecallRankDict(population,data,dataDict)
    for key,datum in tmpRecallRankDict.iteritems():
        recallFitnessDict[key] = datum

    tmpSimScoreMatDict = util.getSimScoreMatDict(population,data)
    for key,datum in tmpSimScoreMatDict.iteritems():
        simScoreMatDict[key] = datum

    fitnessDetails = list( toolbox.map(toolbox.evaluate,population) )
    fitnesses = [f[0] for f in fitnessDetails]; 
    subfitnesses = [f[1] for f in fitnessDetails]

    for ind, fit in zip(population, fitnesses):
        ind.fitness.values = fit
    
    # 
    if halloffame is not None:
        halloffame.update(population)

    record = stats.compile(population) if stats else {}
    logbook.record(gen=0, **record)
    if verbose:
        print logbook.stream

    # Begin the generational process
    for gen in range(1, ngen+1):
        # Select the next generation individuals
        offspring = toolbox.select(population, len(population))
        
        # Vary the pool of individuals
        offspring = deapAlgor.varAnd(offspring, toolbox, cxpb, mutpb)
        
        # Evaluate the individuals
        tmpRecallRankDict = util.getRecallRankDict(offspring,data,dataDict)
        for key,datum in tmpRecallRankDict.iteritems():
            recallFitnessDict[key] = datum

        tmpSimScoreMatDict = util.getSimScoreMatDict(offspring,data)
        for key,datum in tmpSimScoreMatDict.iteritems():
            simScoreMatDict[key] = datum

        fitnessDetails = list( toolbox.map(toolbox.evaluate,offspring) )
        fitnesses = [f[0] for f in fitnessDetails]; 
        subfitnesses = [f[1] for f in fitnessDetails]

        for ind, fit in zip(offspring, fitnesses):
            ind.fitness.values = fit

        # Update the hall of fame with the generated individuals
        if halloffame is not None:
            halloffame.update(offspring)
            
        # Replace the current population by the offspring
        population[:] = offspring
        
        # Append the current generation statistics to the logbook
        record = stats.compile(population) if stats else {}
        logbook.record(gen=gen, **record)
        if verbose:
            print logbook.stream        

        genDir = xprmtDir + "/gen-"+str(gen)
        os.makedirs(genDir)

        np.savetxt(genDir + "/individual.csv", [f for f in population], fmt='%s')
        np.savetxt(genDir + "/fitness.csv", [f.fitness.values for f in population], fmt='%s')
        np.savetxt(genDir + "/fitnessRecall.csv", [f['recallFitness'] for f in subfitnesses], fmt='%s')
        np.savetxt(genDir + "/fitnessInRange.csv", [f['inRangeFitness'] for f in subfitnesses], fmt='%s')
        np.savetxt(genDir + "/fitnessZeroDiv.csv", [f['zeroDivFitness'] for f in subfitnesses], fmt='%s')
        np.savetxt(genDir + "/fitnessIdentity.csv", [f['identityFitness'] for f in subfitnesses], fmt='%s')
        np.savetxt(genDir + "/fitnessSimmetry.csv", [f['simmetryFitness'] for f in subfitnesses], fmt='%s')

    return population, logbook
    