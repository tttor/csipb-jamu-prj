#!/usr/bin/python

import numpy as np
import json
import time
import sys
from multiprocessing import Pool

import matplotlib.pyplot as plt
from blm_ajm import BLMNII

from sklearn import svm
from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold

from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score
from sklearn.preprocessing import MinMaxScaler

sys.path.append('../../utility')
import yamanishi_data_util as yam

sys.path.append('../../config')
from predictor_config import blmniiConfig

def main():
    global classParam,comSimMat,proSimMat,connMat,comNetSim,proNetSim
    classParam = blmniiConfig
    classParam["proba"] = False
    if len(sys.argv)!=6:
        print "python devel.py [numCore] [DataSetCode] [evalMode] [dataPath] [outPath]"
        return

    core = int(sys.argv[1])
    dataset = sys.argv[2]
    evalMode = sys.argv[3]
    dataPath = sys.argv[4]
    outPath = sys.argv[5]

    print "Building Data"
    connMat,comList,proList = yam.loadComProConnMat(dataset,dataPath+"/Adjacency")
    kernel = yam.loadKernel(dataset,dataPath)

    proListIdx = [i for i,_ in enumerate(proList)]
    comListIdx = [i for i,_ in enumerate(comList)]

    nComp = len(comList)
    nProtein = len(proList)

    comSimMat = np.zeros((nComp,nComp), dtype=float)
    proSimMat = np.zeros((nProtein,nProtein), dtype=float)
    for row,i in enumerate(comList):
        for col,j in enumerate(comList):
            comSimMat[row][col] = (kernel[(i,j)]+kernel[(j,i)])/2

    for row,i in enumerate(proList):
        for col,j in enumerate(proList):
            proSimMat[row][col] = (kernel[(i,j)]+kernel[(j,i)])/2


    comSimMat = regularizationKernel(comSimMat)
    proSimMat = regularizationKernel(proSimMat)

    pairData = []
    connList = []
    print "Split Dataset..."
    if evalMode == "loocv":
        nFold = len(comListIdx)
        kSplit = KFold(n_splits=nFold,shuffle=True)
        comSplit = kSplit.split(comListIdx)

        nFold = len(proListIdx)
        kSplit = KFold(n_splits=nFold,shuffle=True)
        proSplit = kSplit.split(proListIdx)

    elif evalMode == "kfold":
        nFold = 10
        kSplit = KFold(n_splits=nFold, shuffle=True)
        comSplit = kSplit.split(comListIdx)
        proSplit = kSplit.split(proListIdx)

    else:
        assert(False)

    predictedData = np.zeros((len(comList),len(proList)),dtype=float)
    splitPred = []
    proTestList = []
    proTrainList = []
    comTestList = []
    comTrainList = []

    for trainIndex, testIndex in proSplit:
        proTestList.append([i for i in testIndex])
        proTrainList.append([i for i in trainIndex])
    for trainIndex, testIndex in comSplit:
        comTestList.append([i for i in testIndex])
        comTrainList.append([i for i in trainIndex])


    if core == 1:
        predRes,testData = singleProc(comTrainList,proTrainList,comTestList,proTestList)
    elif core > 1:
        tempMat = [[row[i] for row in connMat] for i in range(len(connMat[0]))]
        tempPred = BLMNII(classParam)
        tempPred.modParameter(proSimMat=proSimMat,comSimMat=comSimMat,
                                connMat=connMat,netSim=[None,None])
        comNetSim = tempPred._makeNetSim("com",comSimMat,classParam["gamma"],
                                        classParam["alpha"])
        proNetSim = tempPred._makeNetSim("pro",proSimMat,classParam["gamma"],
                                        classParam["alpha"])
        predRes,testData = parallelProc(core,comTrainList,proTrainList,comTestList,proTestList)
    else:
        print "Error: Invalid core processor number"
#####################################################################

    print "\nCalculate Performance"
    key = 'BLM-NII'
    precision, recall, _ = precision_recall_curve(testData, predRes)
    prAUC = average_precision_score(testData, predRes, average='micro')

    print "Visualiation"
    lineType = 'k-.'

    perf = {'precision': precision, 'recall': recall, 'prAUC': prAUC,
                 'lineType': lineType}
    perf2 = {'prAUC': prAUC, 'nTest': nComp*nProtein}

    with open(outPath+'perf_blmnii_'+evalMode+'_'+dataset+'_perf.json', 'w') as fp:
        json.dump(perf2, fp, indent=2, sort_keys=True)

    plt.clf()
    plt.figure()
    plt.plot(perf['recall'], perf['precision'], perf['lineType'], label= key+' (area = %0.2f)' % perf['prAUC'], lw=2)
    plt.ylim([-0.05, 1.05])
    plt.xlim([-0.05, 1.05])
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curve')
    plt.legend(loc="lower left")
    plt.savefig(outPath+'/'+ dataset +'_'+evalMode+'_pr_curve_'+str(time.time())+'.png', bbox_inches='tight')

def singleProc(comTrainList,proTrainList,comTestList,proTestList):
    print "Predicting..."
    testData = []
    predRes = []
    predictor = BLMNII(classParam)
    predictor.modParameter(proSimMat=proSimMat,comSimMat=comSimMat,
                            connMat=connMat,develMode=True)
    for ii,i in enumerate(comTestList):
        for jj,j in enumerate(proTestList):
            sys.stderr.write("\r%d/%d||%d/%d"%(ii,len(comTestList),jj,len(proTestList)))
            sys.stderr.flush()
            predictor.modParameter(trainList=[comTrainList[ii],proTrainList[jj]],
                                    testList=[i,j])
            for comp in i:
                for prot in j:
                    predRes.append(predictor.predict([(comp,prot)]))
                    testData.append(connMat[comp][prot])
    return predRes,testData

def parallelProc(core,comTrainList,proTrainList,comTestList,proTestList):
    print "Building Job List... "
    # We still Have to precomput
    # Parallel This

    predJob = []
    for ii,i in enumerate(comTestList):
        for jj,j in enumerate(proTestList):
            for comp in i:
                for prot in j:
                    predJob.append(((comp,prot),comTrainList[ii],proTrainList[jj],[i,j]))
                    # testData.append(connMat[comp][prot])
    pool = Pool(processes=core)
    print "Run Prediction in parallel..."
    testData = []
    predRes = []
    predParallel = pool.map(parallelWorkArround,predJob)
    # print predParallel
    for pred in predParallel:
        predRes.append(pred[0][0])
        testData.append(connMat[pred[1][0][0]][pred[1][1][0]])
    return predRes,testData

def parallelWorkArround(job):
    predictor = BLMNII(classParam)
    predictor.modParameter(connMat=connMat, comSimMat=comSimMat, proSimMat=proSimMat,
                    trainList=[job[1],job[2]],testList=job[3],
                    netSim=(comNetSim,proNetSim),develMode=True)
    predictionResult = predictor.predict([job[0]])
    return [predictionResult,job[3]]

# http://stackoverflow.com/questions/29644180/gram-matrix-kernel-in-svms-not-positive-semi-definite?rq=1
def regularizationKernel(mat):
    eps = 0.1
    m,n = mat.shape
    assert(m==n)
    while isPSDKernel(mat) == False:
        for i in range(m):
            mat[i][i] = mat[i][i] + eps
    return mat

def isPSDKernel(mat,eps = 1e-8):
  E,V = np.linalg.eigh(mat)
  return np.all(E > -eps) and np.all(np.isreal(E))


if __name__ == '__main__':
    startTime = time.time()
    main()
    print "Program is running for %f seconds"%(time.time()-startTime)
