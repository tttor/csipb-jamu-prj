#!/usr/bin/python

import json
import time
import sys
from multiprocessing import Pool

import yaml
import numpy as np
import matplotlib.pyplot as plt
from blm_ajm import BLMNII

from sklearn import svm
from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold

from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score
from sklearn.preprocessing import MinMaxScaler

sys.path.append('../../../../utility')
import yamanishi_data_util as yam

with open("../config_predictor.json") as f:
    config = yaml.load(f)
    blmniiConfig = config["blmnii"]


def main():
    if sys.argv[1]=="time":
        timeTest()
    elif sys.argv[1]=="aupr":
        auprTest()
    else:
        print "Usage: python devel.py [time|aupr] ..."
        return

def auprTest():
    global classParam,comSimMat,proSimMat,connMat,comNetSim,proNetSim
    classParam = blmniiConfig
    classParam["proba"] = False
    classParam["data"] = "precomputed"
    classParam["kernel"] = ["precomputed","rbf"]
    classParam["retValue"] = "score"
    if len(sys.argv)!=7:
        print "Usage: python devel.py aupr [numCore] [DataSetCode] [evalMode] [dataPath] [outPath]"
        return

    core = int(sys.argv[2])
    dataset = sys.argv[3]
    evalMode = sys.argv[4]
    dataPath = sys.argv[5]
    outPath = sys.argv[6]
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


    comSimMat = {"precomputed":regularizationKernel(comSimMat)}
    proSimMat = {"precomputed":regularizationKernel(proSimMat)}

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
        tempPred = BLMNII(classParam)
        tempPred.setAttr(connMat=connMat,comSimMat=comSimMat,proSimMat=proSimMat)

        comSimMat["rbf"] = regularizationKernel(tempPred.makeNetSim("com"))
        proSimMat["rbf"] = regularizationKernel(tempPred.makeNetSim("pro"))
        tempPred.setAttr(comSimMat=comSimMat,proSimMat=proSimMat)

        predRes,testData = parallelProc(core,comTrainList,proTrainList,comTestList,proTestList)
    else:
        print "Error: Invalid core processor number"
        return
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

    with open(outPath+'perf_blmnii_'+dataset +'_'+evalMode+'_'+str(classParam["alpha"])+'_'+str(classParam["gamma"])+'_perf.json', 'w') as fp:
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
    plt.savefig(outPath+'/'+ dataset +'_'+evalMode+'_'+str(classParam["alpha"])+'_'+str(classParam["gamma"])+'_pr_curve_.png', bbox_inches='tight')

def singleProc(comTrainList,proTrainList,comTestList,proTestList):
    print "Predicting..."
    testData = []
    predRes = []

    predictor = BLMNII(classParam)
    predictor.setAttr(proSimMat=proSimMat,comSimMat=comSimMat,connMat=connMat)
    comSimMat["rbf"] = regularizationKernel(predictor.makeNetSim("com"))
    proSimMat["rbf"] = regularizationKernel(predictor.makeNetSim("pro"))
    predictor.setAttr(comSimMat=comSimMat,proSimMat=proSimMat)
    for ii,i in enumerate(comTestList):
        for jj,j in enumerate(proTestList):
            sys.stderr.write("\r%d/%d||%d/%d"%(ii,len(comTestList),jj,len(proTestList)))
            sys.stderr.flush()
            predictor.setAttr(trainList=[comTrainList[ii],proTrainList[jj]],
                                    testList=[i,j])
            for comp in i:
                for prot in j:
                    predRes.append(predictor.predict([(comp,prot)]))
                    testData.append(connMat[comp][prot])
    return predRes,testData

def parallelProc(core,comTrainList,proTrainList,comTestList,proTestList):
    print "Building Job List... "
    predJob = []
    for ii,i in enumerate(comTestList):
        for jj,j in enumerate(proTestList):
            for comp in i:
                for prot in j:
                    predJob.append(((comp,prot),comTrainList[ii],proTrainList[jj],[i,j]))
    pool = Pool(processes=core)
    print "Run Prediction in parallel..."
    testData = []
    predRes = []
    predParallel = pool.map(parallelWorkArround,predJob)
    for pred in predParallel:
        predRes.append(pred[0][0])
        testData.append(connMat[pred[1][0]][pred[1][1]])
    return predRes,testData

def parallelWorkArround(job):

    predictor = BLMNII(classParam)
    predictor.setAttr(connMat=connMat,comSimMat=comSimMat,proSimMat=proSimMat,
                    trainList=[job[1],job[2]],testList=job[3])
    predictionResult = predictor.predict([job[0]])
    return predictionResult,job[0]

# http://stackoverflow.com/questions/29644180/gram-matrix-kernel-in-svms-not-positive-semi-definite?rq=1
def regularizationKernel(mat):
    eps = 0.01
    m,n = mat.shape
    assert(m==n)
    while isPSDKernel(mat) == False:
        for i in range(m):
            mat[i][i] = mat[i][i] + eps
    return mat

def isPSDKernel(mat,eps = 1e-8):
  E,V = np.linalg.eigh(mat)
  return np.all(E > -eps) and np.all(np.isreal(E))

def timeTest():
    runTimeData = []
    numList = [5,10,15,20]
    for i in numList:
        runTimeData.append(fullTest(i))
    makeGraph(numList,runTimeData)
    with open("execution_time.csv","w") as f:
        f.write("Jumlah Query,Jumlah Data Training,Total Eksekusi,Nilai Rata-Rata\n")
        for r,i in enumerate(nQuery):
            for k,j in enumerate(wut[r]):
                k+=100
                f.write("%d,%d,%f,%f\n"%(i,k,j,j/i))

def fullTest(n):
    with open("meta_prot.pkl","rb") as fp:
        metaProt = joblib.load(fp)
    with open("meta_com.pkl","rb") as fp:
        metaCom = joblib.load(fp)
    proteinIdxQuery = np.random.choice(3333,n,replace=False)
    compoundIdxQuery = np.random.choice(17277,n,replace=False)

    query = zip([metaCom[i] for i in compoundIdxQuery],[metaProt[i] for i in proteinIdxQuery])
    totalTime = []

    for i in range(101,301):
        print "\rRunning %d query with %d data training"%(n,i),
        sys.stdout.flush()
        blmniiConfig["maxTrainingDataSize"] = i
        predictorTest = BLMNII(blmniiConfig)
        prediction = []
        queryTime = []
        for j in query:
            timeStamp = time.time()
            prediction.append(predictorTest.predict(j))
            queryTime.append(time.time()-timeStamp)
        totalTime.append(queryTime)
    ret = []
    for j,i in enumerate(totalTime):
        ret.append(sum(i))

    predictorTest.close()
    return ret

def makeGraph(n,data):
    lineType = ["C0","C1","C2","C3","C4"]
    plt.clf()
    plt.figure()
    for i,d in enumerate(data):
        plt.plot(range(101,301), d, lineType[i], label= "%d Kueri"%n[i], lw=2)
    plt.grid(True)
    plt.ylabel('Total Waktu Eksekusi (s)')
    plt.xlabel('Ukuran Data Latih')
    plt.title('Grafik Perbandingan Waktu Eksekusi dengan Ukuran Data Latih')
    plt.legend(loc="upper left")
    plt.savefig('time_size.png', bbox_inches='tight')

if __name__ == '__main__':
    startTime = time.time()
    main()
    print "Program is running for %f seconds"%(time.time()-startTime)
