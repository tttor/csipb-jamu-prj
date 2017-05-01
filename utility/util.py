# util.py
import numpy as np
import sys
import socket
import datetime

def tag():
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    hostname = socket.gethostname()
    return hostname+'-'+timestamp

def kernel2distanceMatrix(method,simMat):
    # https://rdrr.io/cran/mmpp/man/k2d.html
    m,n = simMat.shape
    disMat = np.ones((m,n),dtype=float)

    if method=='naive':
        for i in range(m):
            for j in range(n):
                # d_n(x,y) = 1 - k(x,y)/sqrt{ k(x,x)k(y,y)},
                disMat[i][j] = (1.0 - simMat[i][j])/np.sqrt(simMat[i][i]*simMat[j][j])
    else:
        assert False, 'FATAL: unkown method'

    return disMat

def makeKernelMatrix(kernelDict,iList=list()):
    if len(iList)==0:
        iList = list(set([i[0] for i in kernelDict.keys()]))

    n = len(iList)
    simMat = np.zeros((n,n),dtype=float)

    for row,i in enumerate(iList):
        for col,j in enumerate(iList):
            simMat[row][col] = kernelDict[(i,j)]

    return (simMat,iList)

def getType(idStr):
    prefix1 = idStr[0:1]
    prefix1 = prefix1.upper()

    prefix3 = idStr[0:3]
    prefix3 = prefix3.upper()

    name = None
    if prefix3=='COM' or prefix1=='D':
        name = 'compound'
    elif prefix3=='PRO' or prefix3=='HSA':
        name = 'protein'
    else:
        assert False, 'Unknown idStr'

    return name

def randData(pairList,limit):
############# Generate random ID #############
    # sys.stderr.write ("Generating additional random data...\n")
    temp1 = None
    tempC = None
    tempP = None
    idP = None
    idC = None

    nPair = len(pairList)
    while nPair < limit:
        temp1 = np.random.randint(1,3334*17277)
        if temp1%3334 == 0:
            idP = 3334
            idC = temp1/3334
        else:
            idP = temp1%3334
            idC = (temp1/3334)+1
        tempC = "COM"+str(idC).zfill(8)

        tempP = "PRO"+str(idP).zfill(8)
        pairList.append([tempC, tempP])
        nPair += 1
    return pairList
