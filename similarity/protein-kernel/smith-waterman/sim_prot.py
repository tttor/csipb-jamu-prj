#!/usr/bin/python

import numpy as np
import time
import math
import csv
import sys

from Bio import SeqIO
from Bio import pairwise2
from Bio.SubsMat.MatrixInfo import blosum62
from multiprocessing import Pool

def main():
    if len(sys.argv)!=5:
        print "python sim_Prot.py [rowStart] [rowEnd] [columnBatch] [poolNum]"
    rowStart = int(sys.argv[1])
    rowEnd = int(sys.argv[2])
    step = int(sys.argv[3])
    poolNum = int(sys.argv[4])
    colStart = rowStart
    colEnd = 3334

    nProtCol = colEnd-colStart
    nProtRow = rowEnd-rowStart

    simMatProtNorm = np.zeros(nProtCol, dtype=float)
    simMatProt = np.zeros(nProtCol, dtype=float)
    fastaFileDir = "Fasta/"
    listDir = "protein.csv"
    OutDir = ""

    uniprotId = []
    colSeq = []
    colMeta = []
    rowSeq = []
    rowMeta = []
    # rowProtein = []
    # colProtein = []
    # rowIndex = []
    # colIndex = []

    ### MultiProcessing ###
    pool = Pool(processes=poolNum)
    ###################

    ###Parse uniprot ID from csv###
    sys.stderr.write("Parsing input\n")
    uniprotId = readProtList(listDir)

    ###############################

    ###Read file and parse (with library)###
    sys.stderr.write("Load fasta file\n")
    for i,name in enumerate(uniprotId):
        fastaDir = fastaFileDir + name + ".fasta"
        with open (fastaDir) as handle:
            recTemp = SeqIO.read(handle, "fasta")
        handle.close()
        recTempMeta = str(recTemp.id)
        recTempMeta = recTempMeta.split("|")
        if i in range(colStart, colEnd):
            colSeq.append(list(recTemp.seq))
            colMeta.append(recTempMeta[1])
        if i in range(rowStart,rowEnd):
            rowSeq.append(list(recTemp.seq))
            rowMeta.append(recTempMeta[1])
    ###Cleanning sequance###
    sys.stderr.write("Cleaning Sequance\n")
    for i in range(nProtRow):
        for j in range(len(rowSeq[i])):
            if(rowSeq[i][j]=='U'):
                rowSeq[i][j]='C'
        rowSeq[i] = "".join(rowSeq[i])
    for i in range(nProtCol):
        for j in range(len(colSeq[i])):
            if(colSeq[i][j]=='U'):
                colSeq[i][j]='C'
        colSeq[i] = "".join(colSeq[i])
    ########################################
    sys.stderr.write("Preparing output file\n")
    outMatDir = OutDir+"RealProtKernel"+str(rowStart)+"_"+str(rowEnd)+".txt"
    outMetaDir = OutDir+"MetaProtKernel"+str(rowStart)+"_"+str(rowEnd)+".txt"

    listScore = []
    simMatProt = [0.0 for k in range(colEnd)]
    # Open file after batch

    for i in range(nProtRow):
        ###Preparing data for parallel mapping###
        startBatch = colStart+i
        while startBatch < colEnd:
            if startBatch+step > colEnd:
                batchLen = 3334 - startBatch
            else:
                batchLen = step
            # for j in range(startBatch,startBatch+batchLen):
            #     rowProtein.append(rowSeq[i])
            #     rowIndex.append(i)
            #     colProtein.append(colSeq[j-colStart])
            #     colIndex.append(j)
            ### Calculation ###
            listScore = [pool.apply_async(alignprot,(rowSeq[i],
                            colSeq[j+startBatch-colStart], i, j+startBatch-colStart,))
                            for j in range(batchLen)]
            for listS in listScore:
                simMatProt[listS.get()[1]] = listS.get()[0]
            #Reset value
            # del rowProtein[:]
            # del rowIndex[:]
            # del colProtein[:]
            # del colIndex[:]
            del listScore[:]
            startBatch += batchLen
        sys.stderr.write("Writing output\n")
        with open(outMatDir, 'a') as matF, open(outMetaDir, 'ayy') as metaF:
            for j in range(colEnd):
                if j>0:
                    matF.write(",")
                matF.write(str(simMatProt[j]))
            matF.write("\n")
            metaF.write(rowMeta[i]+"\n")
        matF.close()
        metaF.close()
    sys.stderr.write("Closing file output\n")


    ##################

def alignprot(rowSeqProtein,colSeqProtein,rowIndex,colIndex):
    sys.stderr.write("\rAligning "+str(rowIndex)+" "+str(colIndex)+",")
    sys.stderr.flush()
    alignres = pairwise2.align.localds(rowSeqProtein,colSeqProtein, blosum62, -1,-1,force_generic = 0, score_only = 1)
    return [alignres, colIndex]

def readProtList(path):
    uniprotIdList = []
    with open(path,'r') as f:
        csvContent = csv.reader(f,  delimiter=',', quotechar='\"')
        for it,row in enumerate(csvContent):
            if (it > 0):
                uniprotIdList.append(row[2])
            else:
                it = 1
    f.close()
    return uniprotIdList


if __name__ == '__main__':
    start = time.time()
    main()
    #############Debugging section#############
    print "Runtime :"+ str(time.time()-start)
    ###########################################
