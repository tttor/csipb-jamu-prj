import util
import numpy
import scipy.stats as stats
from collections import defaultdict
from operator import itemgetter

import config as cfg

def compute(individual, data):
    inRangeFitness = getInRangeFitness(individual,data)

    return (inRangeFitness,)

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

def getRecallFitness(pop, data, dataDict):
    # Get refERENCE and remAINING idx
    refAndRemIdxDict = defaultdict(tuple)
    for classIdx,classData in dataDict.iteritems():
        nSample = len(classData)
        nRef = int( cfg.nRefPerClassInPercentage/100.0 * nSample )
        refIdxList = numpy.random.randint(0,nSample, size=nRef)
        remIdxList = [idx for idx in range(nSample) if idx not in refIdxList]

        refAndRemIdxDict[classIdx] = (refIdxList,remIdxList)

    # Get Recall Matrix along with some other fitness
    nIndividual = len(pop); nClass = len(dataDict)
    medianRecallMat = numpy.zeros( (nIndividual,nClass) )

    for individualIdx,individual in enumerate(pop):
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

                        simScore = util.getSimScore(refString,remString,individual)
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

            median = numpy.median(nRecallList) # Calculate median of nRecall of this class from all refIdx
            medianRecallMat[individualIdx][classIdx] = median

    # Get median recall Ranking Matrix and recallFitness (agnostic to iid)
    medianRecallRankMat = numpy.zeros( (nIndividual, nClass) )
    for i in range(nClass):
        medRecall = medianRecallMat[:,i] # from all individuals of this class
        sortedMedRecallIdx = sorted(range(nIndividual), key=lambda k: medRecall[k],reverse=True)# descending

        rankList = []
        for j in range(nIndividual):
            rank = sortedMedRecallIdx.index(j)
            rankList.append(rank)

        medianRecallRankMat[:,i] = rankList

    recallFitnessList = []
    for i in range(nIndividual):
        recallFitness = numpy.average(medianRecallRankMat[i,:]) * -1.0 # inversed as we maximize the Fitness
        recallFitnessList.append(recallFitness)

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
    if numpy.average(pValueList) <= cfg.pValueAcceptance:
        independent = True

    return (independent, recallFitnessList)
