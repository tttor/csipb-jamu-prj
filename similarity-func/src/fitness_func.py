import util
import numpy as np
import scipy.stats as stats
import operator

import config as cfg

def compute(individual, data, recallFitnessDict, simScoreMatDict):
    individualStr = util.expandFuncStr(str(individual))
    assert individualStr in simScoreMatDict, 'individualStr NOT in simScoreMatDict'
    assert individualStr in recallFitnessDict, 'individualStr NOT in recallFitnessDict'
    simScoreMat = simScoreMatDict[individualStr]

    recallFitness = getRecallFitness(individualStr,recallFitnessDict)
    inRangeFitness = getInRangeFitness(simScoreMat)
    zeroDivFitness = getZeroDivFitness(individualStr)
    identityFitness = getIdentityFitness(simScoreMat)
    simmetryFitness = getSimmetryFitness(simScoreMat)
    
    fitness = recallFitness + inRangeFitness + zeroDivFitness + identityFitness + simmetryFitness

    return (fitness,)

def getRecallFitness(individualStr,recallFitnessDict):
    fitness,valid = recallFitnessDict[individualStr]
    return fitness

def getInRangeFitness(simScoreMat):
    foundIdx = np.where( np.logical_and(simScoreMat>0.0,simScoreMat<=1.0) )
    nInRange = len( foundIdx[0] )
    
    return float(nInRange)/simScoreMat.size*100.0 # in percentage

def getZeroDivFitness(individualStr):
    a = b = c = d = 0.0 # assume all are zeroed
    individualStr = individualStr.replace('protectedDiv','operator.div')

    zeroDiv = 0.0 # not happen
    np.seterr(invalid='ignore')
    try:
        eval(individualStr)
    except ZeroDivisionError as err:
        zeroDiv = 100.0

    return zeroDiv * -1.0 # inversed as we maximize    

def getIdentityFitness(simScoreMat):
    nViolation = 0
    for i in range(simScoreMat.shape[0]):
        for j in range(simScoreMat.shape[1]):
            simScore = simScoreMat[i][j]
            if i==j:
                if simScore!=1.0:
                    nViolation = nViolation + 1
            else:
                if simScore==1.0:
                    nViolation = nViolation + 1

    return (simScoreMat.size - nViolation)/simScoreMat.size * 100.0

def getSimmetryFitness(simScoreMat):
    assert simScoreMat.shape[0]==simScoreMat.shape[1]

    nViolation = 0
    for i in range(0,simScoreMat.shape[0]):
        for j in range(i+1,simScoreMat.shape[1]):
            if simScoreMat[i][j] != simScoreMat[j][i]:
                nViolation = nViolation + 1

    return (simScoreMat.size - nViolation)/simScoreMat.size * 100.0
