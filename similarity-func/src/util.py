import os
import numpy as np
from collections import defaultdict
from scoop import futures as fu
from scipy import stats

import config as cfg
import util

def equalIndividual(i1,i2):
    eps = 0.00001
    assert len(i1.fitness.values)==1
    return (str(i1)==str(i2)) and (abs(i2.fitness.values[0]-i1.fitness.values[0])<eps)

def saveGenLog(xprmtDir,gen,population,subfitnesses,hof):
    genDir = xprmtDir + "/gen-"+str(gen)
    os.makedirs(genDir)

    np.savetxt(genDir + "/individual.csv", [f for f in population], fmt='%s')
    np.savetxt(genDir + "/fitness.csv", [f.fitness.values for f in population], fmt='%s')
    np.savetxt(genDir + "/fitnessRecall.csv", [f['recallFitness'] for f in subfitnesses], fmt='%s')
    np.savetxt(genDir + "/fitnessInRange.csv", [f['inRangeFitness'] for f in subfitnesses], fmt='%s')
    np.savetxt(genDir + "/fitnessZeroDiv.csv", [f['zeroDivFitness'] for f in subfitnesses], fmt='%s')
    np.savetxt(genDir + "/fitnessIdentity.csv", [f['identityFitness'] for f in subfitnesses], fmt='%s')
    np.savetxt(genDir + "/fitnessSimmetry.csv", [f['simmetryFitness'] for f in subfitnesses], fmt='%s')

    np.savetxt(genDir + "/hofIndividual.csv", [str(i) for i in hof], fmt='%s', delimiter=';')
    np.savetxt(genDir + "/hofFitness.csv", [i.fitness.values for i in hof], fmt='%s', delimiter=';')

def getSimScoreMat(individualStr, data):
    nData = len(data)
    simScoreMat = np.zeros( (nData,nData) )

    for i,x1 in enumerate(data):
        for j,x2 in enumerate(data):
            simScore = util.getSimScore(x1,x2,individualStr)
            simScoreMat[i][j] = simScore

    return simScoreMat

def getSimScoreMatDict(population, data):    
    # List unique individual
    populationStr = list(set( [expandFuncStr( str(i) ) for i in population] ))
    nUniqueIndividual = len(populationStr); assert nUniqueIndividual!=0

    simScoreMatList = list( fu.map(getSimScoreMat,populationStr,[data]*nUniqueIndividual) )

    simScoreMatDict = dict()
    for idx,simScoreMat in enumerate(simScoreMatList):
        simScoreMatDict[ populationStr[idx] ] = simScoreMat
    assert len(simScoreMatDict)!=0, 'empty simScoreMatDict'

    return simScoreMatDict

def getMedianRecallDict(individualStr, data, dataDict, refAndRemIdxDict):
    medianRecallDict = defaultdict(float)
    for classIdx, classData in dataDict.iteritems():
        refIdxList = refAndRemIdxDict[classIdx][0]
        nRecallList = [] # from all refIdx of this class

        for refIdx in refIdxList:
            refStringIdx = classData[refIdx]
            refString = data[refStringIdx]

            # Compute simScore for each pair of (ref, rem)
            simScoreList = [] # each element contains 3-tuple of (simScore, refClassLabel, remClassLabel)
            for remClassIdx, refAndRemIdx in refAndRemIdxDict.iteritems():
                remIdxList = refAndRemIdx[1]
                for remIdx in remIdxList:
                    remStringIdx = dataDict[remClassIdx][remIdx]
                    remString = data[remStringIdx]

                    simScore = util.getSimScore(refString,remString,individualStr)
                    simScoreList.append( (simScore,classIdx,remClassIdx) )

            # Sort simScoreList based descending order of SimScore
            sortedSimScoreListIdx = sorted(range(len(simScoreList)), key=lambda k: simScoreList[k][0],reverse=True)

            nTop = int(cfg.nTopInPercentage/100.0 * len(sortedSimScoreListIdx))
            sortedSimScoreListIdx = sortedSimScoreListIdx[0:nTop]

            # Get the number of recall/tp
            nRecall = 0
            for i in sortedSimScoreListIdx:
                refClass = simScoreList[i][1]
                remClass = simScoreList[i][2]
                if (refClass==remClass):
                    nRecall += 1
            nRecallList.append(nRecall) # Add true positive value for this class for this refIdx.

        median = np.median(nRecallList) # Calculate median of nRecall of this class over all refIdx
        medianRecallDict[classIdx] = median
    return medianRecallDict

def getRecallRankDict(pop, data, dataDict):
    # Get refERENCE and remAINING idx
    refAndRemIdxDict = defaultdict(tuple)
    for classIdx,classData in dataDict.iteritems():
        nSample = len(classData)
        nRef = int( cfg.nRefPerClassInPercentage/100.0 * nSample )
        refIdxList = np.random.randint(0,nSample, size=nRef)
        remIdxList = [idx for idx in range(nSample) if idx not in refIdxList]

        refAndRemIdxDict[classIdx] = (refIdxList,remIdxList)

    # List unique individual
    popStr = list(set( [expandFuncStr( str(i) ) for i in pop] ))
    nUniqueIndividual = len(popStr); assert nUniqueIndividual!=0

    # Get Recall Matrix along with some other fitness
    medianRecallDicts = list( fu.map( getMedianRecallDict, popStr,
                                      [data]*nUniqueIndividual,
                                      [dataDict]*nUniqueIndividual,
                                      [refAndRemIdxDict]*nUniqueIndividual ) )

    # Get median recall Ranking Matrix and recallFitness (agnostic to iid)
    nClass = len(dataDict)
    medianRecallRankMat = np.zeros( (nUniqueIndividual, nClass) )
    for classIdx in range(nClass):
        medianRecall = [] # from all individuals of this classIdx
        for medianRecallDict in medianRecallDicts:
            assert classIdx in medianRecallDict
            medianRecall.append( medianRecallDict[classIdx] )
        assert len(medianRecall)==nUniqueIndividual

        sortedMedianRecallIdx = sorted( range(nUniqueIndividual), 
                                        key=lambda k: medianRecall[k],reverse=True ) # descending

        individualRanks = [] # in this classIdx
        for individualIdx in range(nUniqueIndividual):
            rank = sortedMedianRecallIdx.index(individualIdx)
            individualRanks.append(rank)

        percentileIndividualRanks = []
        for rank in individualRanks:
            percentile = stats.percentileofscore(individualRanks, rank)
            percentileIndividualRanks.append(percentile)

        medianRecallRankMat[:,classIdx] = percentileIndividualRanks

    # Test i.i.d (independent and identically distributed)
    # with H0 = two rank lists are independent
    # Thus id p-value is less than a threshold then we accept H0
    # If H0 is accepted, then we can average the rank
    pValueList = []
    for i in range(nClass-1):
        for j in range(i+1,nClass):
            x1 = medianRecallRankMat[:, i]
            x2 = medianRecallRankMat[:, j]

            tau, pval = stats.kendalltau(x1, x2)
            pValueList.append(pval)

    independent = False
    if np.average(pValueList) <= cfg.pValueAcceptance:
        independent = True

    #
    recallRankDict = defaultdict(tuple)
    for individualIdx, individual in enumerate(popStr):
        recallFitness = list( medianRecallRankMat[individualIdx,:] )# of all classes
        recallRankDict[individual] = (recallFitness,independent)

    return recallRankDict
    
def getSimScore(x1,x2,funcStr):
    a = getFeatureA(x1,x2); b = getFeatureB(x1,x2)
    c = getFeatureC(x1,x2); d = getFeatureD(x1,x2)

    return eval(funcStr)

def inRange(simScore):
    return (simScore>0.0 and simScore<=1.0)

def computeGram(X, funcStr):
    print 'computeGram with ', funcStr
    shape = (len(X),len(X))
    gram = np.zeros(shape)

    for i, x1 in enumerate(X):
        for j,x2 in enumerate(X[i:]):
            a = getFeatureA(x1,x2); b = getFeatureB(x1,x2)
            c = getFeatureC(x1,x2); d = getFeatureD(x1,x2)

            simScore = getSimScore(x1,x2,funcStr)
            assert simScore>0.0 
            assert simScore<=1.0

            gram[i][j] = gram [j][i] = simScore

    return gram

def expandFuncStr(istr):
    expansionDict = {'add': 'np.add', 'sub': 'np.subtract', 'mul': 'np.multiply',
                     'pDiv': 'protectedDiv', 'min': 'np.minimum', 'max': 'np.maximum' }

    fstr = istr
    for key, d in expansionDict.iteritems():
        fstr = fstr.replace(key,d)

    return fstr

def tanimotoStr():
    return 'pDiv(a, add(a, add(b, c)))'

def tanimoto(pset, min_, max_, type_=None):
    def condition(height, depth):
        return depth == height

    if type_ is None:
        type_ = pset.ret

    expr = []
    lsTerm = pset.terminals[type_]
    lsPrim = pset.primitives[type_]

    expr.append(lsPrim[3])
    expr.append(lsTerm[0])
    expr.append(lsPrim[0])
    expr.append(lsTerm[0])
    expr.append(lsPrim[0])
    expr.append(lsTerm[1])
    expr.append(lsTerm[2])

    return expr

# def forbesStr():
#     return 'div(sub(mul(add(add(a, b), add(c, d)), a), mul(add(a, b), add(a, c)),sub(mul(add(add(a, b), add(c, d)), min(add(a, b), add(a, c)),mul(add(a, b), add(a, c)))'

# def forbes(pset, min_, max_, type_=None):
#     def condition(height, depth):
#         return depth == height

#     if type_ is None:
#         type_ = pset.ret

#     expr = []
#     lsTerm = pset.terminals[type_]
#     lsPrim = pset.primitives[type_]

#     expr.append(lsPrim[3])
#     expr.append(lsPrim[1])
#     expr.append(lsPrim[2])
#     expr.append(lsPrim[0])
#     expr.append(lsPrim[0])
#     expr.append(lsTerm[0])
#     expr.append(lsTerm[1])
#     expr.append(lsPrim[0])
#     expr.append(lsTerm[2])
#     expr.append(lsTerm[3])
#     expr.append(lsTerm[0])
#     expr.append(lsPrim[2])
#     expr.append(lsPrim[0])
#     expr.append(lsTerm[0])
#     expr.append(lsTerm[1])
#     expr.append(lsPrim[0])
#     expr.append(lsTerm[0])
#     expr.append(lsTerm[2])

#     expr.append(lsPrim[1])
#     expr.append(lsPrim[2])
#     expr.append(lsPrim[0])
#     expr.append(lsPrim[0])
#     expr.append(lsTerm[0])
#     expr.append(lsTerm[1])
#     expr.append(lsPrim[0])
#     expr.append(lsTerm[2])
#     expr.append(lsTerm[3])
#     expr.append(lsPrim[4])
#     expr.append(lsPrim[0])
#     expr.append(lsTerm[0])
#     expr.append(lsTerm[1])
#     expr.append(lsPrim[0])
#     expr.append(lsTerm[0])
#     expr.append(lsTerm[2])
#     expr.append(lsPrim[2])
#     expr.append(lsPrim[0])
#     expr.append(lsTerm[0])
#     expr.append(lsTerm[1])
#     expr.append(lsPrim[0])
#     expr.append(lsTerm[0])
#     expr.append(lsTerm[2])

#     return expr

def protectedDiv(left, right):
    with np.errstate(divide='ignore',invalid='ignore'):
        x = np.divide(left, right)
        if isinstance(x, np.ndarray):
            x[np.isinf(x)] = 1
            x[np.isnan(x)] = 1
        elif np.isinf(x) or np.isnan(x):
            x = 1
    return x

def pow(x):
    return np.power(x, 2)

def powhalf(x):
    return np.power(x, 0.5)

def loadData(datapath):
    data = np.loadtxt(datapath, delimiter=',')

    dataDict = defaultdict(list)
    for idx, datum in enumerate(data):
        classIdx = int(datum[0]) # the first element _must_ be classIdx
        dataDict[classIdx].append(idx) # contain only the idx
    assert (0 in dataDict), 'idx does not begin at 0'

    dataFeature = []
    for idx,x in enumerate(data):
        subdataFeature = []
        for idx2,x2 in enumerate(data):
            featureDict = {}
            featureDict['a'] = getFeatureA(x,x2)
            featureDict['b'] = getFeatureB(x,x2)
            featureDict['c'] = getFeatureC(x,x2)
            featureDict['d'] = getFeatureD(x,x2)
            subdataFeature.append(featureDict)
        dataFeature.append(subdataFeature)
    
    return (data,dataDict,dataFeature)

def getFeatureA(s1,s2):
    return np.inner(s1, s2)

def getFeatureB(s1,s2):
    return np.inner(s1, 1-s2)

def getFeatureC(s1,s2):
    return np.inner(1-s1, s2)

def getFeatureD(s1,s2):
    return np.inner(1-s1, 1-s2)

def isConverged(pop):
    maxFitnessVal = np.max([ind.fitness.values[0] for ind in pop])
    
    converged = False
    if maxFitnessVal > cfg.convergenceThreshold:
        converged = True

    return converged
