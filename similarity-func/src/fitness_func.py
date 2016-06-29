import util
import numpy as np
import scipy.stats as stats
from collections import defaultdict
from operator import itemgetter
import operator

import config as cfg

def compute(individual, data, recallFitnessDict, simScoreMatDict):
    recallFitness = getRecallFitness(individual,recallFitnessDict)
    inRangeFitness = getInRangeFitness(individual,simScoreMatDict)
    zeroDivFitness = getZeroDivFitness(individual)
    
    fitness = recallFitness + inRangeFitness + zeroDivFitness

    return (fitness,)

def getInRangeFitness(individual,simScoreMatDict):
    individualStr = util.expandFuncStr(str(individual))
    assert individualStr in simScoreMatDict, 'individualStr NOT in simScoreMatDict'

    simScoreMat = simScoreMatDict[individualStr]
    foundIdx = np.where( np.logical_and(simScoreMat>0.0,simScoreMat<=1.0) )
    nInRange = len( foundIdx[0] )
    
    return float(nInRange)/simScoreMat.size*100.0 # in percentage

def getRecallFitness(individual,recallFitnessDict):
    individualStr = util.expandFuncStr(str(individual))
    assert individualStr in recallFitnessDict, 'individualStr NOT in recallFitnessDict'

    fitness,valid = recallFitnessDict[ util.expandFuncStr(str(individual)) ]
    return fitness

def getIdentityFitness():
    pass

def getSimmetryFitness():
    pass

def getZeroDivFitness(individual):
    a = b = c = d = 0.0
    individualStr = util.expandFuncStr( str(individual) )
    individualStr = individualStr.replace('protectedDiv','operator.div')

    zeroDiv = 0.0 # not happen
    np.seterr(invalid='ignore')
    try:
        eval(individualStr)
    except ZeroDivisionError as err:
        zeroDiv = 100.0

    return zeroDiv * -1.0 # inversed as we maximize    
