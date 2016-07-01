import util
import numpy as np
import scipy.stats as stats
import operator
import time

import config as cfg

def compute(individual, data, recallPercentileRankDict, simScoreMatDict):
    individualStr = util.expandFuncStr(str(individual))
    assert individualStr in simScoreMatDict, 'individualStr NOT in simScoreMatDict'
    assert individualStr in recallPercentileRankDict, 'individualStr NOT in recallPercentileRankDict'
    simScoreMat = simScoreMatDict[individualStr]

    recallFitness = getRecallFitness(individualStr,recallPercentileRankDict)
    inRangeFitness = getInRangeFitness(simScoreMat)
    zeroDivFitness = getZeroDivFitness(individualStr)
    identityFitness = getIdentityFitness(simScoreMat)
    simmetryFitness = getSimmetryFitness(simScoreMat)
    
    fitness = recallFitness + inRangeFitness + zeroDivFitness + identityFitness + simmetryFitness
    fitnessDict = {'recallFitness':recallFitness, 'inRangeFitness':inRangeFitness, 
                   'zeroDivFitness':zeroDivFitness, 'identityFitness':identityFitness,
                   'simmetryFitness':simmetryFitness }

    return ( (fitness,),fitnessDict )

def getRecallFitness(individualStr,recallPercentileRankDict):
    percentileRankList,independent = recallPercentileRankDict[individualStr]
    percentileRank = np.average(percentileRankList)

    maxPercentile = 100.0
    fitness = maxPercentile - percentileRank # normalized so that 100.0 is the best

    if not(independent):
        timeStr = time.strftime("%Y%m%d-%H%M%S")
        with open(cfg.xprmtDir+"/warn_not_independent_occurred_at_"+timeStr, "wb") as f:
            f.write(str(log))

    return fitness # in percentile

def getInRangeFitness(simScoreMat):
    foundIdx = np.where( np.logical_and(simScoreMat>0.0,simScoreMat<=1.0) )
    nInRange = len( foundIdx[0] )
    
    return float(nInRange)/simScoreMat.size * 100.0 # in percentage

def getZeroDivFitness(individualStr):
    a = b = c = d = 0.0 # assume all are zeroed
    individualStr = individualStr.replace('protectedDiv','operator.div')

    inPercent = 100
    zeroDivFitness = inPercent # not happen
    np.seterr(invalid='ignore')
    try:
        r = eval(individualStr)
        if np.isnan(r) or np.isinf(r):
            zeroDivFitness = 0.0
    except ZeroDivisionError as err:
        zeroDivFitness = 0.0

    return zeroDivFitness

def getIdentityFitness(simScoreMat):
    nViolation = 0
    eps = 0.00001
    for i in range(simScoreMat.shape[0]):
        for j in range(simScoreMat.shape[1]):
            simScore = simScoreMat[i][j]
            if i==j:
                if not((simScore>1.0-eps)and(simScore<1.0+eps)):
                    nViolation = nViolation + 1
            else:
                if (simScore>1.0-eps)and(simScore<1.0+eps):
                    nViolation = nViolation + 1
    return float((simScoreMat.size - nViolation))/simScoreMat.size * 100.0 # in percentage

def getSimmetryFitness(simScoreMat):
    assert simScoreMat.shape[0]==simScoreMat.shape[1]

    nViolation = 0
    for i in range(0,simScoreMat.shape[0]):
        for j in range(i+1,simScoreMat.shape[1]):
            if simScoreMat[i][j] != simScoreMat[j][i]:
                nViolation = nViolation + 1

    return float((simScoreMat.size - nViolation))/simScoreMat.size * 100.0 # in percentage
