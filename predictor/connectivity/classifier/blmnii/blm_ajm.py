import sys
import time
import yaml

import psycopg2
import numpy as np
from numpy import linalg as LA
from sklearn import svm
from sklearn.preprocessing import MinMaxScaler
from sklearn.externals import joblib

with open("../config_predictor.json") as f:
    config = yaml.load(f)
    blmniiConfig = config["blmnii"]

with open("../config_database.json") as f:
    dcfg = yaml.load(f)

sys.path.append('../../../../utility')
import util

# NOTES query batch from predictor server must be 1 only
class BLMNII:
    def __init__(self,params):

        self._alpha = params['alpha']
        self._gamma0 = params['gamma']
        self._name = params['name']
        self._proba = params['proba']
        self._nPair = params['maxTrainingDataSize']
        self._kernel = params['kernel']
        self._connDB = psycopg2.connect(database=dcfg['database'],user=dcfg['user']
                        ,password=dcfg['password'],host=dcfg['host'],port=dcfg['port'])
        self._cur = self._connDB.cursor()
        self._data = params['data']
        self._ret = params['retValue']
        self._comSimMat = dict()
        self._proSimMat = dict()
        self._connMat = None

        self._trainList = None
        self._testList = None

    def predict(self,query):
        nQuery = len(query)

        if self._data=="precomputed":#
            queryIdx = [(i[0],i[1]) for i in query]
            comTrain = self._trainList[0]
            comTest = self._testList[0]
            proTrain = self._trainList[1]
            proTest = self._testList[1]

        else:
            comMeta, self._comSimMat[self._kernel[0]] = self._makeKernel(query,"com")
            comTest = comMeta[query[0][0]]
            comTrain = [idx for idx,i in enumerate(comMeta) if idx!=comTest]

            proMeta, self._proSimMat[self._kernel[0]] = self._makeKernel(query,"pro")
            proTest = proMeta[query[0][1]]
            proTrain = [idx for idx,i in enumerate(proMeta) if idx!=proTest]
            queryIdx = [(comTest,proTest)]

            self._connMat = self._makeAdjMat(comMeta,proMeta)

        mergePred = []
        for i in queryIdx:
            comPred = self._predict(self._comSimMat[self._kernel[0]],self._proSimMat,
                                    [[proTest],proTrain],(i[0],i[1]),"pro")
            proPred = self._predict(self._proSimMat[self._kernel[0]],self._comSimMat,
                                    [[comTest],comTrain],(i[1],i[0]),"com")

            if abs(comPred["score"])>abs(proPred["score"]):
                mergePred.append(comPred[self._ret])
            else:
                mergePred.append(proPred[self._ret])
        return mergePred

    def close(self):
        self._connDB.close()

    def _predict(self,sourceSim,targetSim,dataSplit,dataQuery,mode):
        if mode == "com":
            adjMatrix = np.transpose(self._connMat)
        elif mode == "pro":
            adjMatrix = self._connMat

        testIndex = dataSplit[0]
        trainIndex = dataSplit[1]
        sourceIndex = dataQuery[0]
        targetIndex = dataQuery[1]

        nTrain = len(trainIndex)
        nTest = len(testIndex)
        nSource = len(sourceSim)
        nTarget = len(targetSim)

        intProfile = np.zeros(nTrain,dtype=float)
        neighbors = [j for i,j in enumerate(adjMatrix[sourceIndex]) if i in trainIndex]
        isNewData = len(set(neighbors))==1

        if isNewData:
            for i in range(nSource):
                for jj,j in enumerate(trainIndex):
                    intProfile[jj] += sourceSim[sourceIndex][i] * adjMatrix[i][j]
            scale = MinMaxScaler((0,1))
            intProfile = intProfile.reshape(-1,1)
            intProfile = scale.fit_transform(intProfile)
            intProfile = [i[0] for i in intProfile.tolist()]
            threshold = 0.5
            intProfile = [int(i>=threshold) for i in intProfile]
        else:
            for ii,i in enumerate(trainIndex):
                intProfile[ii] = adjMatrix[sourceIndex][i]

        cantPredict = len(set(intProfile))==1
        if cantPredict:
            return {"class":0,"score":0,"probability":0}
        else:
            if (not isNewData) and ("rbf" in targetSim):
                gramTrain = targetSim["rbf"]
                gramTest = targetSim["rbf"][targetIndex]
            elif (not isNewData) and ("rbf" in self._kernel):
                gramTrain = self.makeNetSim(mode)
                gramTest = gramTrain[targetIndex]
            else:
                gramTest = targetSim[self._kernel[0]][targetIndex]
                gramTrain = targetSim[self._kernel[0]]

            for i in reversed(sorted(testIndex)):
                gramTest = np.delete(gramTest,i, 0)
                gramTrain = np.delete(gramTrain,i, 0)
                gramTrain = np.delete(gramTrain,i, 1)
            model = svm.SVC(kernel='precomputed', probability=True)
            model.fit(gramTrain, intProfile)

            probability = model.predict_proba(gramTest.reshape(1,-1))
            score = model.decision_function(gramTest.reshape(1,-1))
            prediction = model.predict(gramTest.reshape(1,-1))
            return {"class":prediction[0],"score":score[0],"proba":probability[0][0]}

    def setAttr(self,proSimMat=None,comSimMat=None,connMat=None,
                        trainList=None,testList=None,netSim=None):
        if comSimMat is not None:
            self._comSimMat = comSimMat
        if proSimMat is not None:
            self._proSimMat = proSimMat
        if connMat is not None:
            self._connMat = connMat
        if trainList is not None:
            self._trainList = trainList
        if testList is not None:
            self._testList = testList

    def makeNetSim(self,mode):
        # makeNetSim already combined 2 similarity Measurement
        if mode == "com":
            targetSim = self._comSimMat[self._kernel[0]]
            adjMatrix = self._connMat
        elif mode == "pro":
            targetSim = self._proSimMat[self._kernel[0]]
            adjMatrix = np.transpose(self._connMat)

        gamma0 = self._gamma0
        alpha = self._alpha
        nTarget = len(targetSim)
        netSim = np.zeros((targetSim.shape),dtype=float)
        for i in range(nTarget):
            intpro1 = adjMatrix[i]
            gamma = sum(intpro1**2)*gamma0/nTarget
            if gamma==0:
                gamma = gamma0
            for j in range(i,nTarget):
                intpro2 = adjMatrix[j]
                netSim[j][i] = self.computeNetSim(intpro1,intpro2,gamma)
                netSim[i][j] = (alpha*targetSim[j][i] + (1-alpha)*netSim[j][i])
        for i in range(nTarget):
            for j in range(i+1,nTarget):
                netSim[j][i] = netSim[j][i]/(np.sqrt(netSim[i][i])*np.sqrt(netSim[j][j]))
                netSim[i][j] = netSim[j][i]
        for i in range(nTarget):
            netSim[i][i] = netSim[i][i]/(np.sqrt(netSim[i][i])*np.sqrt(netSim[i][i]))
        return netSim

    def computeNetSim(self,profile1,profile2,gamma):
        norm = LA.norm(profile1-profile2)
        value = np.exp(-((norm**2)/gamma))
        return float(value)

    def _makeKernel(self,query_in,mode):
        simMat = np.zeros((self._nPair,self._nPair), dtype=float)+10e-8
        if mode=="com":
            with open("similarity-pickle/meta_com.pkl","rb") as fp:
                metaCom = joblib.load(fp)
            dataListId = np.random.choice(17277,self._nPair-1,replace=False)
            metaSim = []
            metaSim = {metaCom[i]:idx+1 for idx,i in enumerate(dataListId)}
            metaSim[query_in[0][0]] = 0

            qParam = ["com_id","com_similarity_simcomp","compound"]
            query = "SELECT " +qParam[0]+","+ qParam[1]+ " FROM " + qParam[2]
            queryC = " WHERE "
            for i,d in enumerate(metaSim):
                if i>0:
                    queryC += " OR "
                queryC += (qParam[0] + " = " + "'" + d + "'")
            query += queryC
            self._cur.execute(query)
            dataRows = self._cur.fetchall()

            for i,row in enumerate(dataRows):
                if row[1] != None:
                    temp = row[1].split(',')
                    for j in temp:
                        if j.split(':')[0] in metaSim:
                            simMat[metaSim[row[0]]][metaSim[j.split(':')[0]]]=float(j.split('=')[1])

        elif mode=="pro":
            with open("similarity-pickle/sim_pro.pkl","rb") as fp:
                allSimMat = joblib.load(fp)
            with open("similarity-pickle/meta_pro.pkl","rb") as fp:
                metaProt = joblib.load(fp)

            if query_in[0][1] in set(metaProt):
                idx = metaProt.index(query_in[0][1])
                temp = []
                for i,v in enumerate(allSimMat[idx]):
                    temp.append([v,i])
                temp.sort(reverse=True)
                metaIdx = [idx]
            else:
                dataListId = np.random.choice(len(metaProt),self._nPair-1,replace=False)
                temp = [[1,-1]]+[[0,i] for i in dataListId]
                metaIdx = [-1]

            metaSim={query_in[0][1]:0}
            for i in range(1,self._nPair):
                metaIdx.append(temp[i][1])
                metaSim[metaProt[temp[i][1]]]=i
            for i in range(self._nPair):
                for j in range(i,self._nPair):
                    if (metaIdx[i]>=0 and metaIdx[j]>=0) :
                        simMat[i][j] = allSimMat[metaIdx[i]][metaIdx[j]]
                    else:
                        simMat[i][j] = 0
                    simMat[j][i] = simMat[i][j]

        return metaSim, simMat

    def _makeAdjMat(self,comList,proList):
        adjMat = np.zeros((len(comList), len(proList)), dtype=int)

        query = "SELECT com_id, pro_id, weight FROM compound_vs_protein"
        queryC = " WHERE ("
        for i,j in enumerate(comList):
            if i>0:
                queryC += " OR "
            queryC += " com_id = " + "'"+j+"'"
        queryC += ")"
        queryP = " AND ("
        for i,j in enumerate(proList):
            if i>0:
                queryP += " OR "
            queryP += " pro_id = " + "'"+j+"'"
        queryP += ")"

        query += queryC + queryP
        self._cur.execute(query)
        rows = self._cur.fetchall()
        for row in rows:
            adjMat[comList[row[0]]][proList[row[1]]]=(row[2])
        return adjMat

def unitTest():
    # print "init"
    pairQuery = [('COM00000020','PRO00001846')]
    # print "load class"
    predictorTest = BLMNII(blmniiConfig)
    testRes = predictorTest.predict(pairQuery)
    print "Interaction Probability: ",testRes
    predictorTest.close()

if __name__=='__main__':
    startTime = time.time()
    unitTest()
    print "Program is running for "+str(time.time()-startTime)+" seconds"
