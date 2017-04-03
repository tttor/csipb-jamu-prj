import csv
import sys
import math
import time
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def main():
    if len(sys.argv)!=5:
        print "Usage: python combine_go_sim.py [BP] [MF] [CC] [Output]"

    CCDataDir = sys.argv[3]
    outDir = sys.argv[4]
    BPDataDir = sys.argv[1]
    MFDataDir = sys.argv[2]

    print "Parsing Data"
    BPSimMat,protMeta = fileToMatrix(BPDataDir)
    MFSimMat,_ = fileToMatrix(MFDataDir)
    CCSimMat,_ = fileToMatrix(CCDataDir)

    print "Combine Matrix"
    combGOSimMat = np.zeros((3334,3334),dtype=float)
    m,n = combGOSimMat.shape
    diagSim = []
    for i in range(m):
        for j in range(i,n):
            combGOSimMat[i][j] = (BPSimMat[i][j]+MFSimMat[i][j]+CCSimMat[i][j])/3
            if i==j:
                diagSim.append(combGOSimMat[i][j])

    print "Normalizing Value"
    # Based on stats.stackexchange.com/questions/23397/kernel-matrix-normalisation
    for i in range(m):
        for j in range(i,n):
            combGOSimMat[i][j] = (combGOSimMat[i][j]/math.sqrt(diagSim[i]))/math.sqrt(diagSim[j])
            combGOSimMat[j][i] = combGOSimMat[i][j]

    print "Writing file"
    with open(outDir,'w') as f:
        for i in range(m):
            for j in range(n):
                if j>0:
                    f.write(',')
                f.write(str(combGOSimMat[i][j]))
            f.write('\n')

    with open("meta_"+outDir,'w') as f:
        for prot in protMeta:
            f.write(prot)
            f.write('\n')

def fileToMatrix(directory):
    print "Parsing " + directory
    goSimMat = np.zeros((3334,3334),dtype=float)
    metaList = []
    with open(directory,'r') as f:
        fileContent = csv.reader(f,delimiter=',', quotechar='\"')
        for i,row in enumerate(fileContent):
            if i>0:
                for j,col in enumerate(row):
                    if j==0:
                        metaList.append(col)
                    else:
                        if col != "NA":
                            # print i,j
                            goSimMat[i-1][j-1] = float(col)
    return goSimMat,metaList

if __name__=='__main__':
    start_time = time.time()
    main()
    print "Program is running for "+str(time.time()-start_time)
