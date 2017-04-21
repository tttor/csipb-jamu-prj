import sys
import time
import numpy as np
import psycopg2

from sklearn import svm
from sklearn.preprocessing import MinMaxScaler

sys.path.append('../../config')
from database_config import databaseConfig as dcfg
from predictor_config import blmniiConfig

sys.path.append('../../utility')
import util

class SELFBLM:
    def __init__(self,params,connMat=None,comSimMat=None,proSimMat=None,
                    trainList=None,testList=None):

        self._name = params['name']
        self._proba = params['proba']
        self._connDB = psycopg2.connect(database=dcfg['name'],user=dcfg['user'],password=dcfg['passwd'],
                                        host=dcfg['host'],port=dcfg['port'])
        self._cur = self._connDB.cursor()

        if connMat is not None:
            self._comSimMat = comSimMat
            self._proSimMat = proSimMat
            self._connMat = connMat
            self._develMode = True
            self._trainList = trainList
            self._testList = testList

    def predict(self, query):


        if self._develMode:
            queryIdx = [[i[0],i[1]] for i in query]

            comTrain = self._trainList[0]
            comTest = self._testList[0]

            proTrain = self._trainList[1]
            proTest = self._testList[1]

        mergePred = []
        for i in queryIdx:
            comPred = self._predict(self._connMat,self._comSimMat,self._proSimMat,
                                    [proTest,proTrain],(i[0],i[1]),0)
            proPred = self._predict(self._connMat,self._proSimMat,self._comSimMat,
                                    [comTest,comTrain],(i[1],i[0]),1)
            mergePred.append(max(comPred,proPred))
        # print "This section is running for "+str(time.time()-timer)+" seconds"
        return mergePred

    def close():
        pass

    def _predict(self,adjMatrix, sourceSim, targetSim, dataSplit, dataQuery,mode):

        if mode:
            adjMatrix = [[row[i] for row in adjMatrix] for i in range(len(adjMatrix[0]))]

        testIndex = dataSplit[0]
        trainIndex = dataSplit[1]
        sourceIndex = dataQuery[0]
        targetIndex = dataQuery[1]

        nTrain = len(trainIndex)
        nTest = len(testIndex)
        nSource = len(sourceSim)

        gramTest = targetSim[targetIndex]
        gramTrain = targetSim
        for i in reversed(sorted(testIndex)):
            gramTest = np.delete(gramTest,i, 0)
            gramTrain = np.delete(gramTrain,i, 0)
            gramTrain = np.delete(gramTrain,i, 1)

        intVector = np.array([i for r,i in enumerate(adjMatrix[sourceIndex]) if r != targetIndex ])

        if len(set(intVector)) == 1 or np.all(intVector != 1):
            return -1
        elif np.all(intVector != -1):
            intVector = np.array([i if i==1 else -1 for i in intVector])

        else:
            while np.any(intVector == 0):
                labInt = [i for i in intVector if i!=0]

                labIdx = [v for v,i in enumerate(intVector) if i!=0]
                ulabIdx = [v for v,i in enumerate(intVector) if i == 0]
                uTrain = np.zeros((len(labIdx),len(labIdx)),dtype=float)
                uTest = np.zeros((len(ulabIdx),len(labIdx)),dtype=float)

                for r,i in enumerate(labIdx):
                    for c,j in enumerate(labIdx):
                        uTrain[r][c] = gramTrain[i][j]

                for r,i in enumerate(ulabIdx):
                    for c,j in enumerate(labIdx):
                        uTest[r][c] = gramTrain[i][j]

                model = svm.SVC(kernel='precomputed')
                model.fit(uTrain, labInt)
                uPred = model.predict(uTest)
                uDist = model.decision_function(uTest)
                # print ulabIdx,uDist
                for r,i in enumerate(uPred):
                    if abs(uDist[r])>0:
                        intVector[ulabIdx[r]] = i

        model = svm.SVC(kernel='precomputed')
        model.fit(gramTrain, intVector)
        pred = model.predict(gramTest.reshape(1,-1))
        return pred


    def _makeKernel():
        pass

    def _makeAdjMat():
        pass

def test():
    pass

if __name__ == '__main__':
    pass
