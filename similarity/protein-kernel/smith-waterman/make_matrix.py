import numpy as np
import csv
import time
import math
import sys
# This script is about make kernel from file output produced by ****_sim_prot.py

def main():
    if len(sys.argv)!= 4:
        print "Usage: python make_matrix.py [listDir] [fileDir] [outputDir]"
        return

    protFile = sys.argv[1]
    listFileDir = sys.argv[2]
    outputDir = sys.argv[3]

    print "Opening uniprot ID list"
    with open(listDir,'r') as protFile:
        content = csv.reader(protFile,delimiter=",",quotechar="\"")
        uIdList = []
        for it,row in enumerate(content):
            if (it > 0):
                u.append(row[2])
            else:
                it = 1

    realSimMat = np.zeros((len(uIdList),len(uIdList)))
    normSimMat = np.zeros((len(uIdList),len(uIdList)))

    print "Make real matrix"
    with open(listFileDir,'r') as listFile:
        content = csv.reader(listFile,delimiter=",",quotechar="\"")
        for row in content:
            realSimMat[uIdList.index(row[0])][uIdList.index(row[1])] = int(row[3])

    print "Normalization"
    for i in range(uIdList):
        for j in range(i+1,uIdList):
            normSimMat[i][j] = realSimMat[i][j]/(math.sqrt(realSimMat[i][i])*math.sqrt(realSimMat[j][j]))

    for i in range(uIdList):
        normSimMat[i][i] = realSimMat[i][i]/(math.sqrt(realSimMat[i][i])*math.sqrt(realSimMat[i][i]))

    print "Writing Output"
    with open(outputDir+"sim_prot.csv",',w') as outMat:
        for i in range(len(uniprotIdList)):
            for j in range(len(uniprotIdList)):
                if (j>startIdx):
                    outMat.write(",")
                outMat.write(str(simMatProt[i][j]))
            outMat.write("\n")
    outMat.close()

    with open(outputDir+"meta_sim_prot.csv",'w') as metaF:
        for i in range(len(uniprotIdList)):
            metaF.write(uniprotIdList[i]+"\n")
    metaF.close()


if __name__ == '__main__':
    startTime = time.time()
    main()
    print "Program Running for: %s"%startTime-time.time()
