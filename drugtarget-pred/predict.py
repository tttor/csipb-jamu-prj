import psycopg2
import random
import numpy as np
import sys
import time
from blm import predictBLMNII

conn = psycopg2.connect(database="ijah", user="ijah", password="ijahdb", host= "127.0.0.1", port = "5432")
cur = conn.cursor()

def MakeKernel(dataList,mode):
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
    cur.execute(query)
    dataRows = cur.fetchall()
    for i,row in enumerate(dataRows):
        if row[1] != None:
            temp = row[1].split(',')
            temp = [i.split('=') for i in temp]
            for j in temp:
                if j[0].split(':')[0] in dataDict:
                    simMat[dataDict[row[0]]][dataDict[j[0].split(':')[0] ]]=float(j[1])

    return dataDict, simMat


if __name__ == "__main__":
    #init Variables
    start = time.time()
    print "Initialization..."
    #Catch Argument sent from php...
    compList = [c for c in sys.argv[1].split(',')]
    protList = [p for p in sys.argv[2].split(',')]
    assert len(compList) == len(protList)

    ############# Build to be predicted data as Pair #############
    print "Preparing to be predicted data..."
    pairIdList = [[compList[i], protList[i]] for i in range(len(compList))]
    maxIter = len(pairIdList)
    nPair = len(pairIdList)
    # pairSet = set(pairIdList)

    ############# Generate random ID #############
    print "Generating addtional random data..."
    temp1 = None
    tempC = None
    tempP = None
    idP = None
    idC = None

    while nPair < 1000:
        temp1 = np.random.randint(1,3334*17277)
        if temp1%3334 == 0:
            idP = 3334
            idC = temp1/3334
        else:
            idP = temp1%3334
            idC = (temp1/3334)+1
        tempC = "COM"+str(idC).zfill(8)

        tempP = "PRO"+str(idP).zfill(8)
        # if ([temp1,temp2] in pairSet):
        #     continue
        # pairSet |= [temp1, temp2]
        pairIdList.append([tempC, tempP])
        nPair += 1

    ############# Make simMat and dict #############
    print "Making kernel...."
    compList = [i[0] for i in pairIdList]
    compMeta, compSimMat = MakeKernel(compList,"com")

    protList = [i[1] for i in pairIdList]
    protMeta, protSimMat = MakeKernel(protList,"pro")

    ############# Make adjacency list #############
    print "Building connectivity data"
    adjMat = np.zeros((len(compMeta), len(protMeta)), dtype=int)

    query = "SELECT com_id, pro_id, weight FROM compound_vs_protein"
    queryC = " WHERE ("
    for i,j in enumerate(compMeta):
        if i>0:
            queryC += " OR "
        queryC += " com_id = " + "'"+j+"'"
    queryC += ")"
    queryP = " AND ("
    for i,j in enumerate(protMeta):
        if i>0:
            queryP += " OR "
        queryP += " pro_id = " + "'"+j+"'"
    queryP += ")"

    query += queryC + queryP
    cur.execute(query)

    rows = cur.fetchall()
    for row in rows:
        adjMat[compMeta[row[0]]][protMeta[row[1]]]=(row[2])

    ############## Predict ##############
    print "Predicting..."
    #Transform from PairId to PairIndex
    pairIndexList = [[compMeta[i[0]],protMeta[i[1]]] for i in pairIdList]
    resPred = np.zeros((len(pairIndexList)),dtype=float)
    for i,pair in enumerate(pairIndexList):
        if i == maxIter:
            break
        #PredictEveryPair
        resPred[i] = predictBLMNII(adjMat,compSimMat,protSimMat,pair[0],pair[1])

    ############## Update database ##############
    print "Push data to DB"
    for i in range(maxIter):
        query1 = "INSERT INTO compound_vs_protein (com_id, pro_id, source, weight) "
        query2 = "VALUES ( "+ "'" + pairIdList[i][0] + "', "+ "'" + pairIdList[i][1]
        query3 = "', " + "'blm-nii-svm', "+ str(resPred[i]*0.65)+" )"

        query = query1 + query2 + query3
        cur.execute(query)

    conn.commit()

    conn.close()
    print "Done..."

    
    #############Debugging section#############
    print "Runtime :"+ str(time.time()-start)
    ###########################################
