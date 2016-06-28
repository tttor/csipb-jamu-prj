import util
import numpy as np
import scipy.stats as stats
from collections import defaultdict
from operator import itemgetter

import config as cfg

def compute(individual, data, recallFitnessDict):
    inRangeFitness = getInRangeFitness(individual,data)
    recallFitness = getRecallFitness(individual,recallFitnessDict)

    fitness = inRangeFitness + recallFitness

    return (fitness,)

def getInRangeFitness(individual,data):
    n = 0
    nInRange = 0
    individualStr = util.expandFuncStr(str(individual))
    for i,sx in enumerate(data):
        for j,sy in enumerate(data[i:]):
            simScore = util.getSimScore(sx,sy,individualStr)
            n = n + 1

            if util.inRange(simScore):
                nInRange = nInRange + 1

    return float(nInRange)/n*100.0 # in percentage

def getRecallFitness(individual,recallFitnessDict):
    individualStr = util.expandFuncStr(str(individual))
    assert individualStr in recallFitnessDict, 'individualStr NOT in recallFitnessDict'

    fitness,valid = recallFitnessDict[ util.expandFuncStr(str(individual)) ]
    return fitness
