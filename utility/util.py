# util.py
import numpy as np
import sys

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
        pairList.append([tempC, tempP])
        nPair += 1
    return pairList
