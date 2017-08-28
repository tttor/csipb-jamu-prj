#!/usr/bin/python

import numpy as np
import json
import time
import sys

import matplotlib.pyplot as plt

from sklearn import svm
from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold

from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score
from sklearn.preprocessing import MinMaxScaler

sys.path.append('../../utility')
import yamanishi_data_util as yam

sys.path.append('../cluster/kmedoid')
import kmedoid

from generateNegativeData import genNegativeData
from selfblm import SELFBLM

def main():
    if len(sys.argv)!=5:
        print ("python blmniisvm_experiment.py [DataSetCode] [evalMode]"
                " [dataPath] [outPath]")
        return
    classParam = dict(name='blmnii',proba=True)

    dataset = sys.argv[1]
    evalMode = sys.argv[2]
    dataPath = sys.argv[3]
    outPath = sys.argv[4]

    print "Building Data"
    connMat,comList,proList = yam.loadComProConnMat(dataset,dataPath+"/Adjacency")
    kernel = yam.loadKernel(dataset,dataPath)

    comListIdx = [i for i,_ in enumerate(comList)]
    proListIdx = [i for i,_ in enumerate(proList)]

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

    print "Clustering"
    comDisMat = kmedoid.simToDis(comSimMat)
    proDisMat = kmedoid.simToDis(proSimMat)

    _,proClust = kmedoid.kMedoids(len(proList)/2, proDisMat)
    _,comClust = kmedoid.kMedoids(len(comList)/2, comDisMat)

    print "Generate Negative Data"
    connMat = genNegativeData(connMat,proClust,comClust)
    # PLACEHOLDER

    # Split Data
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

    predRes = []
    testData = []

    print "Predicting..."
    for ii,i in enumerate(comTestList):
        for jj,j in enumerate(proTestList):
            sys.stdout.write("\r%03d of %03d||%03d of %03d" %
                                (jj+1, len(proTestList), ii+1,len(comTestList),))
            sys.stdout.flush()

            predictor = SELFBLM(classParam, connMat, comSimMat, proSimMat,
                            [comTrainList[ii],proTrainList[jj]],[i,j])
            for comp in i:
                for prot in j:
                    predRes.append(predictor.predict([(comp,prot)]))
                    if connMat[comp][prot] == 1:
                        testData.append(1)
                    else:
                        testData.append(-1)

    # run core selfBLM
    # Evaluate prediction
    print "\nCalculate Performance"
    key = 'PredictionUsingSelfBLM'
    precision, recall, _ = precision_recall_curve(testData, predRes)
    prAUC = average_precision_score(testData, predRes, average='micro')

    print "Visualiation"
    lineType = 'k-.'

    perf = {'precision': precision, 'recall': recall, 'prAUC': prAUC,
                 'lineType': lineType}
    perf2 = {'prAUC': prAUC, 'nTest': nComp*nProtein}

    with open(outPath+'perf_selfblm_'+evalMode+'_'+dataset+'_perf.json', 'w') as fp:
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
    plt.savefig(outPath+'/pr_curve_'+ dataset +'_'+evalMode+'_selfblm.png', bbox_inches='tight')

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
    start_time = time.time()
    main()
    print "Program is running for :"+str(time.time()-start_time)
