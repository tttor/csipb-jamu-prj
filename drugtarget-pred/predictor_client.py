#!/usr/bin/python
import psycopg2
import random
import numpy as np
import sys
import time
import os
import socket

conn = psycopg2.connect(database="ijah", user="ijah", password="123", host= "127.0.0.1", port = "5432")
cur = conn.cursor()

if __name__ == "__main__":

    #init Variables

    start = time.time()

    sys.stderr.write("Initialization...\n")
    #Catch Argument sent from php...
    compList = [c for c in sys.argv[1].split(',')]
    protList = [p for p in sys.argv[2].split(',')]
    assert len(compList) == len(protList)

    ############# Build to be predicted data as Pair #############
    sys.stderr.write ("Preparing to be predicted data...\n")
    pairIdList = [[compList[i], protList[i]] for i in range(len(compList))]

    ############## Prepare Query Data ##############
    queryString = ""
    for i,pair in enumerate(pairIdList):
        if i >0:
            queryString += ","
        queryString += pair[0]+":"+pair[1]

    ##### Send Data to server
    addr = ('localhost',5557)
    data = ""
    dataTemp = ""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(addr)
    sys.stderr.write("Connecting to server...\n")
    try:
        sock.sendall(queryString+"|end")
        sys.stderr.write("Sending Data...\n")
        sys.stderr.write(str(queryString)+"...\n")
        lenDataRecv = 0
        lenDataExpected = len(queryString)+(4*len(pairIdList))

        while lenDataRecv < lenDataExpected:
            dataTemp = sock.recv(1024)
            lenDataRecv += len(dataTemp)
            data += dataTemp
    finally:
        sys.stderr.write("Closing connection...\n")
        sock.close()

    timeEx = time.time()
    metaPred = [[pair.split(":")[0], pair.split(":")[1].split("=")[0]] for pair in data.split(",")]
    resPred = [ 0.65*float(res.split(":")[1].split("=")[1]) for res in data.split(",")]


    strOut = ''
    for i,pair in enumerate(metaPred):
        if i>0:
            strOut += ','
        strOut += pair[0]
    strOut += '|'

    for i,pair in enumerate(metaPred):
        if i>0:
            strOut += ','
        strOut += pair[1]
    strOut += '|'

    for i,res in enumerate(resPred):
        if i>0:
            strOut += ','
        strOut += str(res)
    strOut += '|'

    for i,res in enumerate(resPred):
        if i>0:
            strOut += ','
        strOut += "blm-nii-svm"
    strOut += '|'

    for i,res in enumerate(resPred):
        if i>0:
            strOut += ','
        strOut += '%s.%04f' % (time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(int(timeEx))), timeEx-int(timeEx))
    strOut += '|'


    print strOut
    ############## Update database ##############
    query = ""
    query1 = ""
    query2 = ""
    query3 = ""
    queryCheck = ""

    sys.stderr.write ("Push data to DB...\n")
    for i in range(len(compList)):
        ## Check row in the table ##
        queryCheck = "SELECT * FROM compound_vs_protein WHERE "
        queryCheck += "com_id='"+pairIdList[i][0]+"' AND pro_id='"+pairIdList[i][1]+"'"
        queryCheck += " AND source = 'blm-nii-svm'"
        cur.execute(queryCheck)
        dataRows = cur.fetchall()
        # ## Update row if data is already exsist on table ##
        if len(dataRows)>0:
            query1 = "UPDATE compound_vs_protein "
            query2 = "SET source='blm-nii-svm', weight="+ str(resPred[i])+", time_stamp=now() "
            query3 = "WHERE com_id='" + pairIdList[i][0] + "'AND pro_id='" + pairIdList[i][1]+"'"

        # ## Insert if no record found ##
        else:
            #May use INSERT INTO .. VALUE ... ON DUPLICATE KEY UPDATE
            query1 = "INSERT INTO compound_vs_protein (com_id, pro_id, source, weight) "
            query2 = "VALUES ( "+ "'" + pairIdList[i][0] + "', "+ "'" + pairIdList[i][1]
            query3 = "', " + "'blm-nii-svm', "+ str(resPred[i])+" )"

        query = query1 + query2 + query3
        # print query
        cur.execute(query)

    conn.commit()

    conn.close()
    sys.stderr.write ("Done...\n")

    #############Debugging section#############
    sys.stderr.write ("Runtime :"+ str(time.time()-start)+"\n")
    ###########################################
