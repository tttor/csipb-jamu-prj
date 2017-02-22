import numpy as np

import psycopg2
import blmnii
import sys

sys.path.append('../server')
from config import databaseConfig as dcfg
sys.path.append('../util')
import util

class BLMNII:
    def __init__(self):
        self.name = 'blmnii'
        self.connDB = psycopg2.connect(database=dcfg['name'],user=dcfg['user'],password=dcfg['passwd'],
                                        host=dcfg['host'],port=dcfg['port'])
        self.cur = self.connDB.cursor()

    def predict(self,query):
        nQuery = len(query)
        # sys.stderr.write ("Processing Query.... \n")
        pairIdList = util.randData(query,1000)

        # sys.stderr.write ("Making kernel....\n")
        compList = [i[0] for i in pairIdList]
        compMeta, compSimMat = self.makeKernel(compList,"com")
        protList = [i[1] for i in pairIdList]
        protMeta, protSimMat = self.makeKernel(protList,"pro")

        # sys.stderr.write ("Building connectivity data...\n")
        adjMat = self.makeAdjMat(compMeta,protMeta)

        pairIndexList = [[compMeta[i[0]],protMeta[i[1]]] for i in pairIdList]
        # sys.stderr.write ("Running BLM-NII...\n")
        # Running Batch
        resPred = []
        for i,pair in enumerate(pairIndexList):
            if i == nQuery:
                break
            resPred.append(blmnii.predict(adjMat,compSimMat,protSimMat,
                        pair[0],pair[1]))
        return resPred

    def makeAdjMat(self,compList,protList):
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
        self.cur.execute(query)
        rows = self.cur.fetchall()
        for row in rows:
            adjMat[compList[row[0]]][protList[row[1]]]=(row[2])
        return adjMat

    def makeKernel(self,dataList,mode):
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
        self.cur.execute(query)
        dataRows = self.cur.fetchall()
        for i,row in enumerate(dataRows):
            if row[1] != None:
                temp = row[1].split(',')
                temp = [i.split('=') for i in temp]
                for j in temp:
                    if j[0].split(':')[0] in dataDict:
                        simMat[dataDict[row[0]]][dataDict[j[0].split(':')[0]]]=float(j[1])
        return dataDict, simMat
