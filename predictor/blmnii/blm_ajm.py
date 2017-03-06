import numpy as np

import psycopg2
import blmnii
import sys
import time

sys.path.append('../../config')
from database_config import databaseConfig as dcfg
from predictor_config import blmniiConfig

sys.path.append('../../utility')
import util

class BLMNII:
    def __init__(self,params):
        self._name = params['name']
        self._nPair = params['maxTrainingDataSize']
        self._connDB = psycopg2.connect(database=dcfg['name'],user=dcfg['user'],password=dcfg['passwd'],
                                        host=dcfg['host'],port=dcfg['port'])
        self._cur = self._connDB.cursor()

    def predict(self,query):
        nQuery = len(query)
        # sys.stderr.write ("Processing Query.... \n")
        pairIdList = util.randData(query,self._nPair)

        # sys.stderr.write ("Making kernel....\n")
        compList = [i[0] for i in pairIdList]
        compMeta, compSimMat = self._makeKernel(compList,"com")
        protList = [i[1] for i in pairIdList]
        protMeta, protSimMat = self._makeKernel(protList,"pro")

        # sys.stderr.write ("Building connectivity data...\n")
        adjMat = self._makeAdjMat(compMeta,protMeta)
        pairIndexList = [[compMeta[i[0]],protMeta[i[1]]] for i in pairIdList]
        # sys.stderr.write ("Running BLM-NII...\n")
        # Running Batch
        comPred = self._predict(adjMat,compSimMat,protSimMat,pairIndexList,
                                nQuery,0)
        proPred = self._predict(adjMat,protSimMat,compSimMat,pairIndexList,
                                nQuery,1)

        mergePred = []
        for i in range(nQuery):
            mergePred.append(max(comPred[0][0],proPred[0][0]))
        return mergePred

    def close(self):
        self._connDB.close()

    def _makeAdjMat(self,compList,protList):
        adjMat = np.zeros((len(compList), len(protList)), dtype=int)

        query = "SELECT com_id, pro_id, weight FROM compound_vs_protein"
        queryC = " WHERE ("
        for i,j in enumerate(compList):
            if i>0:
                queryC += " OR "
            queryC += " com_id = " + "'"+j+"'"
        queryC += ")"
        queryP = " AND ("
        for i,j in enumerate(protList):
            if i>0:
                queryP += " OR "
            queryP += " pro_id = " + "'"+j+"'"
        queryP += ")"

        query += queryC + queryP
        self._cur.execute(query)
        rows = self._cur.fetchall()
        for row in rows:
            adjMat[compList[row[0]]][protList[row[1]]]=(row[2])
        return adjMat

    def _predict(self,adjMat,sourceSim,targetSim,pairIndexList,nQuery,mode):
        resPred = []
        if mode:
            adjMat = [[row[i] for row in adjMat] for i in range(len(adjMat[0]))]

        for i,pair in enumerate(pairIndexList):
            if i == nQuery:
                break
            train = [j for j in range(len(targetSim)) if j != i]
            test = [i]

            resPred.append(blmnii.BLM_NII(adjMat,sourceSim,targetSim,
                        (test,train),(pair[mode],pair[not(mode)])))

        return resPred

    def _makeKernel(self,dataList,mode):
        dataList = list(set(dataList))
        dataDict = {e:i for i,e in enumerate(dataList)}#for Index
        simMat = np.zeros((len(dataList),len(dataList)), dtype=float)
        if mode=="com":
            qParam = ["com_id","com_similarity_simcomp","compound"]
        elif mode=="pro":
            qParam = ["pro_id","pro_similarity_smithwaterman","protein"]

        query = "SELECT " + qParam[0] +", " + qParam[1]+ " FROM " + qParam[2]
        queryC = " WHERE "

        for i,d in enumerate(dataList):
            if i>0:
                queryC += " OR "
            queryC += (qParam[0] + " = " + "'" + d + "'")
        query += queryC
        self._cur.execute(query)
        dataRows = self._cur.fetchall()
        for i,row in enumerate(dataRows):
            if row[1] != None:
                temp = row[1].split(',')
                temp = [i.split('=') for i in temp]
                for j in temp:
                    if j[0].split(':')[0] in dataDict:
                        simMat[dataDict[row[0]]][dataDict[j[0].split(':')[0]]]=float(j[1])
        return dataDict, simMat

def test():
    pairQuery = [('COM00014256','PRO00001554')]
    predictorTest = BLMNII(blmniiConfig)
    testRes = predictorTest.predict(pairQuery)

if __name__=='__main__':
    startTime = time.time()
    test()
    print "Program is running for "+str(time.time()-startTime)+" seconds"
