import util
import numpy
import scipy.stats as stats
from collections import defaultdict
from operator import itemgetter

import config as cfg

def compute(pop,data):
    valid = False; recallFitnessList = None
    for i in range(cfg.maxKendallTrial):
        valid,recallFitnessList = testKendal(pop, data)
        if valid:
            break

    fitnessList = []
    if valid:
        inRangeFitnessList = getInRangeFitness(pop,data)
        assert len(recallFitnessList)==len(inRangeFitnessList)

        for i in range(len(pop)):
            fitness = recallFitnessList[i] + inRangeFitnessList[i]
            fitnessList.append(fitness)

    return (valid,fitnessList)

def getInRangeFitness(pop,data):
    data2 = []
    for classIdx, classData in data.iteritems():
        data2 = data2 + classData

    inRangeFitnessDict = {}
    for individualIdx,individual in enumerate(pop):
        for i,sx in enumerate(data2):
            for j,sy in enumerate(data2[i:]):
                a = util.getFeatureA(sx,sy)
                b = util.getFeatureB(sx,sy)
                c = util.getFeatureC(sx,sy)
                d = util.getFeatureD(sx,sy)
                simScore = individual(a,b,c,d); 

                inRangeFitness = 0.0
                if not(util.inRange(simScore)):
                    inRangeFitness = cfg.nIndividual
                inRangeFitnessDict[individualIdx] = inRangeFitness

    inRangeFitnessList = []
    for i in range(cfg.nIndividual):
        inRangeFitnessList.append( inRangeFitnessDict[i] )

    return inRangeFitnessList

def testKendal(pop, data):
    # Get refERENCE and remAINING idx
    refAndRemIdxDict = defaultdict(tuple)
    for classIdx,classData in data.iteritems():
        nSample = len(classData)
        nRef = int( cfg.nRefPerClassInPercentage/100.0 * nSample )
        refIdxList = numpy.random.randint(0,nSample, size=nRef)
        remIdxList = [idx for idx in range(nSample) if idx not in refIdxList]

        refAndRemIdxDict[classIdx] = (refIdxList,remIdxList)

    # Get Recall Matrix along with some other fitness
    nIndividual = len(pop); nClass = len(data)
    medianRecallMat = numpy.zeros( (nIndividual,nClass) )

    for individualIdx,individual in enumerate(pop):
        for classIdx, classData in data.iteritems():
            refIdxList = refAndRemIdxDict[classIdx][0]
            nRecallList = [] # from all refIdx of this class

            for refIdx in refIdxList:
                refString = classData[refIdx]

                # Compute simScore for each pair of (ref, rem)
                simScoreList = [] # each element contains 3-tuple of (simScore, refClassLabel, remClassLabel)
                for remClassIdx, refAndRemIdx in refAndRemIdxDict.iteritems():
                    remIdxList = refAndRemIdx[1]
                    for remIdx in remIdxList:
                        remString = data[remClassIdx][remIdx]
                        a = util.getFeatureA(refString, remString)
                        b = util.getFeatureB(refString, remString)
                        c = util.getFeatureC(refString, remString)
                        d = util.getFeatureD(refString, remString)
                        simScore = individual(a,b,c,d); 
                        simScoreList.append( (simScore,classIdx,remClassIdx) )

                # Sort simScoreList based descending order of SimScore
                sortedIdx = sorted(range(len(simScoreList)), key=lambda k: simScoreList[k][0])

                nTop = int(cfg.nTopInPercentage/100.0 * len(sortedIdx))
                sortedIdx = sortedIdx[0:nTop]

                # Get the number of recall/tp
                nRecall = 0
                for i in sortedIdx:
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
        medianRecallPerClass = medianRecallMat[:,i] # from all individuals
        sortedIdx = sorted(range(nIndividual), key=lambda k: medianRecallPerClass[k])

        rankList = []
        for j in range(nIndividual):
            rank = sortedIdx.index(j)
            rankList.append(rank)
        medianRecallRankMat[:,i] = rankList

    recallFitnessList = []
    for i in range(nIndividual):
        recallFitness = numpy.average(medianRecallRankMat[i,:])
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
