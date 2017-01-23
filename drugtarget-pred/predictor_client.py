#!/usr/bin/python
import random
import numpy as np
import sys
import time
import os
import socket

################################################################################
# This channel is not specified in a separate file because
# importing custom py causes error on .py executed from .php
predictor_channel = {}
predictor_channel['host'] = 'localhost'
predictor_channel['port'] = 5557
ch = predictor_channel
################################################################################

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
    addr = (ch['host'],ch['port'])
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
    resPred = [float(res.split(":")[1].split("=")[1]) for res in data.split(",")]


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
    sys.stderr.write ("Done...\n")
    #############Debugging section#############
    sys.stderr.write ("Runtime :"+ str(time.time()-start)+"\n")
    ###########################################
