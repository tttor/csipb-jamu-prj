#!/usr/bin/python
import signal
import socket
import time
import sys
import threading
import psycopg2

import numpy as np
from datetime import datetime

from predictor_server_thread import PredictorServerThread as PST
from config import database as db
import blmnii
import util

connDB = psycopg2.connect(database=db['name'],user=db['user'],password=db['passwd'],
                      host=db['host'],port=db['port'])

def main():
    if len(sys.argv)!=6:
        print 'USAGE: phyton prediction_server.py [host] [portLo] [portHi] [maxElapsedTime] [serverId]'
        return

    global maxElapsedTime
    global upAt
    host = sys.argv[1]
    portLo = int(sys.argv[2])
    portHi = int(sys.argv[3])
    maxElapsedTime = float(sys.argv[4])
    serverId = sys.argv[5]
    upAt = datetime.now().strftime("%Y:%m:%d %H:%M:%S")

    print >> sys.stderr, '******************************************************'
    print >> sys.stderr,"Ijah predictor server :)"
    print >> sys.stderr,"[id= "+serverId+"]"
    print >> sys.stderr,"[ports= "+str(portLo)+" to "+str(portHi)+"]"
    print >> sys.stderr,"[maxElapsedTimePerQuery= "+str(maxElapsedTime)+" seconds]"
    print >> sys.stderr,"[upFrom= "+upAt+"]"

    threadList = [PST(i,"server-"+str(i), host, port) for i,port in enumerate(range(portLo, portHi+1))]
    signal.signal(signal.SIGINT, signalHandler)
    for t in threadList:
        t.daemon=True
        t.start()

    while True:
        pass

    connDB.close()

def signalHandler(signal, frame):
    sys.stderr.write("Closing thread, socket, and database ...\n")
    connDB.close()
    sys.exit(0)

def makeKernel(dataList,mode,cur):
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

def predict(queryString,cur):
    maxIter = None
    pairIdList = None
    pairQueryList = None

    compList = None
    compMeta = None
    compSimMat = None
    protList = None
    protMeta = None
    protSimMat = None
    adjMat = None

    query = ""
    queryC = ""
    queryP = ""
    rows = None

    resPred = None
    sendRes = ""
    timeEx = time.time()

    sys.stderr.write ("Processing Query.... \n")
    pairQuery = [queryString.split(":")]

    ##Parsing to pair id list
    pairIdList = util.randData(pairQuery,1000)

    ############# Make simMat and dict #############
    sys.stderr.write ("Making kernel....\n")
    compList = [i[0] for i in pairIdList]
    compMeta, compSimMat = makeKernel(compList,"com",cur)

    protList = [i[1] for i in pairIdList]
    protMeta, protSimMat = makeKernel(protList,"pro",cur)

    ############# Make adjacency list #############
    sys.stderr.write ("Building connectivity data...\n")
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

    ########### Prediction ###################
    sys.stderr.write ("Running BLM-NII...\n")
    #Transform from PairId to PairIndex
    pairIndexList = [[compMeta[i[0]],protMeta[i[1]]] for i in pairIdList]

    resPred = blmnii.predict(adjMat,compSimMat,protSimMat,pairIndexList[0][0],pairIndexList[0][1])
    sendRes += pairIdList[0][0]+'|'+pairIdList[0][1]+'|'+str(resPred)
    sendRes += "|blm-nii-svm|"+'%s.%04f' % (time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(int(timeEx))), timeEx-int(timeEx))

    ############## push to DB ##################
    query = ""
    query1 = ""
    query2 = ""
    query3 = ""
    queryCheck = ""
    #
    sys.stderr.write ("Push data to DB...\n")
    ## Check row in the table ##
    queryCheck = "SELECT * FROM compound_vs_protein WHERE "
    queryCheck += "com_id='"+pairIdList[0][0]+"' AND pro_id='"+pairIdList[0][1]+"'"
    queryCheck += " AND source = 'blm-nii-svm'"
    cur.execute(queryCheck)
    dataRows = cur.fetchall()
    # ## Update row if data is already exsist on table ##
    if len(dataRows)>0:
        query1 = "UPDATE compound_vs_protein "
        query2 = "SET source='blm-nii-svm', weight="+ str(resPred)+", time_stamp=now() "
        query3 = "WHERE com_id='" + pairIdList[0][0] + "'AND pro_id='" + pairIdList[0][1]+"'"

    # ## Insert if no record found ##
    else:
        #May use INSERT INTO .. VALUE ... ON DUPLICATE KEY UPDATE
        query1 = "INSERT INTO compound_vs_protein (com_id, pro_id, source, weight) "
        query2 = "VALUES ( "+ "'" + pairIdList[0][0] + "', "+ "'" + pairIdList[0][1]
        query3 = "', " + "'blm-nii-svm', "+ str(resPred)+" )"

    query = query1 + query2 + query3
    cur.execute(query)
    connDB.commit()

    return sendRes

def predictDummy(query):
    comId,proId = query.split(":")
    weight = 0
    source = 'null'
    timestamp = 'null'
    predictionStrList = [comId,proId,str(weight),source,timestamp]
    predictionStr = '|'.join(predictionStrList)
    return predictionStr

if __name__ == '__main__':
    funcPointer = {'blm-nii':predict} # Add future predict function here
    main()
