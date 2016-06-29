import util
import numpy as np
import scipy.stats as stats
from collections import defaultdict
from operator import itemgetter

import config as cfg

def compute(individual, data, recallFitnessDict, simScoreMatDict):
    inRangeFitness = getInRangeFitness(individual,simScoreMatDict)
    recallFitness = getRecallFitness(individual,recallFitnessDict)

    fitness = inRangeFitness + recallFitness

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

def getZeroDivFitness():
    pass
    
