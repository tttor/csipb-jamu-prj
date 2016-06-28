import util
import numpy as np
import scipy.stats as stats
from collections import defaultdict
from operator import itemgetter

import config as cfg

def compute(individual, data, recallRankDict):
    inRangeFitness = getInRangeFitness(individual,data)
    recallFitness = getRecallFitness(individual,recallRankDict)

    return (inRangeFitness,recallFitness)

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

    return float(nInRange)/n

def getRecallFitness(individual,recallRankDict):
    individualStr = util.expandFuncStr(str(individual))
    assert individualStr in recallRankDict, 'individualStr NOT in recallRankDict'

    fitness,valid = recallRankDict[ util.expandFuncStr(str(individual)) ]
    assert not(fitness<0.0)

    return fitness
