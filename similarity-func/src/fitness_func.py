import util
import numpy
import scipy.stats as stats
from collections import defaultdict
from operator import itemgetter

import config as cfg

def testKendal(toolbox, pop, data):
    # Get ref idx
    refRemIdxListDict = defaultdict(tuple)
    for classIdx,dataPerClass in data.iteritems():
        nSample = len(dataPerClass)
        nRef = int( cfg.nRefPerClassInPercentage/100.0 * nSample )
        refIdxList = numpy.random.randint(0,nSample, size=nRef)
        remIdxList = [idx for idx in range(nSample) if idx not in refIdxList]

        refRemIdxListDict[classIdx] = (refIdxList,remIdxList)

    # Get Recall Matrix
    nIndividual = len(pop); nClass = len(data)
    medianRecallMat = numpy.zeros( (nIndividual,nClass) )
    for individualIdx,individual in enumerate(pop):
        simFunc = toolbox.compile(expr=individual)
        medianPerClass = []

        for classIdx, classData in data.iteritems():
            nRecallList = [] # from all refIdx of this class
            refIdxList = refRemIdxListDict[classIdx][0]
            for refIdx in refIdxList:
                refString = classData[refIdx]
                simScoreList = [] # each element contains 3-tuple of (simScore, refClassLabel, remClassLabel)


                # Compute simScore for each pair of (ref, rem)
                for remClassIdx, refRemIdxListTuple in refRemIdxListDict.iteritems():
                    remIdxList = refRemIdxListTuple[1]
                    for remIdx in remIdxList:
                        remString = data[remClassIdx][remIdx]
                        a = util.getFeatureA(refString, remString)
                        b = util.getFeatureB(refString, remString)
                        c = util.getFeatureC(refString, remString)
                        d = util.getFeatureD(refString, remString)
                        simScore = simFunc(a,b,c,d)
                        simScoreList.append( (simScore,classIdx,remClassIdx) )

                # Sort simScoreList based descending order of SimScore
                sortedIdx = sorted(range(len(simScoreList)), key=lambda k: simScoreList[k][0])
                #   print "len sortedIdx : ", len(sortedIdx)
                #  Must check again, because remaining data should be 72-length but it's given 78-length

                nTop = cfg.nTopInPercentage/100.0 * len(sortedIdx)
                sortedIdx = sortedIdx[0:int(nTop)]

                # Get the number of recall/tp
                nRecall = 0
                for i in sortedIdx:
                    refClass = simScoreList[i][1]
                    remClass = simScoreList[i][2]

                    if (refClass==remClass):
                        nRecall += 1

                nRecallList.append(nRecall) # Add true positive value for current class.

            median = numpy.median(nRecallList) # Calculate median of true positive value current class
            medianRecallMat[individualIdx][classIdx] = median

    # Get median recall Ranking Matrix
    medianRecallRankMat = numpy.zeros( (nIndividual, nClass) )
    for i in range(nClass):
        medianRecallListPerClass = medianRecallMat[:,i]
        sortedIdx = sorted(range(len(medianRecallListPerClass)), key=lambda k: medianRecallListPerClass[k])

        rankList = []
        for j in range(nIndividual):
            rank = sortedIdx.index(j)
            rankList.append(rank)
        medianRecallRankMat[:,i] = rankList

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
    pValueAvg = numpy.average(pValueList)
    if pValueAvg <= cfg.pValueAcceptance:
        independent = True

    return independent, medianRecallRankMat
