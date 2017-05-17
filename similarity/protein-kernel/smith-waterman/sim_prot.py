import sys
import time
import csv
import math

import numpy as np
from Bio import SeqIO
from Bio.SubsMat.MatrixInfo import blosum62
from multiprocessing import Pool

def main():
    if len(sys.argv) !=5 or len(sys.argv) !=6:
        print "Usage: python sim_prot.py [numCore] [listDir] [fastaDir] [jobList] [lenBatch]"
        return

    core = int(sys.argv[1])
    listDir = sys.argv[2]
    fastaDir = sys.argv[3]
    jobListDir = sys.argv[4]
    if core > 1:
        poolNum = core
        step = int(sys.argv[5])

    # Open job list, Generate a job Queue
    print "Opening Job List"
    with open(jobListDir,'r') as jobListFile:
        csvcontent = csv.reader(jobListFile,delimiter=",",quotechar="\"")
        jobList = []
        for row in (csvcontent):
            jobList.append((int(row[0]),int(row[1])))

    print "Building Id List"
    with open(listDir,'r') as protFile:
        csvcontent = csv.reader(protFile,delimiter=",",quotechar="\"")
        uniprotIdList = []
        for it,row in enumerate(csvcontent):
            if (it > 0):
                uniprotIdList.append(row[2])
            else:
                it = 1

    print "Dumping sequance"
    seqList = []
    seqMeta = []
    nProt = len(uniprotIdList)
    for i,name in enumerate(uniprotIdList):
        ffDir = fastaDir + name + ".fasta"
        with open (ffDir) as handle:
            recTemp = SeqIO.read(handle, "fasta")
        recTempMeta = str(recTemp.id)
        recTempMeta = recTempMeta.split("|")
        if i in range(nProt):
            seqList.append(list(recTemp.seq))
            seqMeta.append(recTempMeta[1])

    sys.stderr.write("Cleaning Sequance\n")
    for i in range(nProt):
        for j in range(len(seqList[i])):
            if(seqList[i][j]=='U'):
                seqList[i][j]='C'
        seqList[i] = "".join(seqList[i])

    print "Calculate S-W score and output"
    if core == 1:
        singleProc(jobList,seqMeta,seqList)
    elif mode > 1:
        parallelProc(poolNum,step,jobList,seqMeta,seqList)

def singleProc(jobList,seqMeta,seqList):
    with open("simprot_list.csv"%time.time(),'w') as simFile:
        for idx,pairJob in enumerate(jobList):
            _,_,simScore = selfLocalAlign(seqMeta[pairJob[0]],seqMeta[pairJob[1]],seqList[pairJob[0]],seqList[pairJob[1]],blosum62,-1)
            simFile.write("%s,%s,%d\n"%(seqMeta[pairJob[0]],seqMeta[pairJob[1]],simScore))

def parallelProc(poolNum,step,jobList,seqMeta,seqList):
    pool = Pool(processes=poolNum)
    startBatch = 0
    step = step
    noBatch = 1
    fileName = "simprot_list_%d.csv"%time.time()
    while startBatch < len(jobList):
        if startBatch+step > len(jobList):
            batchLen = len(jobList) - startBatch
        else:
            batchLen = step
        print "%d of %d batch"%(noBatch,len(jobList)/step)
        listScore = [pool.apply_async(selfLocalAlign,(seqMeta[jobList[startBatch+b][0]],
                        seqMeta[jobList[startBatch+b][1]],seqList[jobList[startBatch+b][0]],
                        seqList[jobList[startBatch+b][1]],blosum62,-1,))
                        for b in range(batchLen)]

        with open(fileName,'a') as simFile:
            for listS in listScore:
                simFile.write("%s,%s,%d\n"%(listS.get()[0],listS.get()[1],listS.get()[2]))
        del listScore[:]
        startBatch += batchLen
        noBatch += 1

def selfLocalAlign(metaS1,metaS2,seq1,seq2,subMat,gap):
    sys.stderr.write("\rAligning %s and %s"%(metaS1,metaS2))
    sys.stderr.flush()
    m = len(seq1)
    n = len(seq2)
    dpTable = np.zeros((m+1,n+1))
    for i,c1 in enumerate(seq1):
        for j,c2 in enumerate(seq2):
            if (c1,c2) in subMat:
                diag = dpTable[i][j]+subMat[(c1,c2)]
            else:
                diag = dpTable[i][j]+subMat[(c2,c1)]
            down = dpTable[i][j+1]+gap
            right = dpTable[i+1][j]+gap

            dpTable[i+1][j+1]=max(0,diag,down,right)

    return metaS1,metaS2,np.max(dpTable)

if __name__ == '__main__':
    startTime=time.time()
    main()
    print "Program running for %s"%(time.time()-startTime)
