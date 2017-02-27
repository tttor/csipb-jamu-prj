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
    colStart = 0
    colEnd = 3334

    nProtCol = colEnd-colStart
    nProtRow = rowEnd-rowStart

    simMatProtNorm = np.zeros(nProtCol, dtype=float)
    simMatProt = np.zeros(nProtCol, dtype=float)
    fastaFileDir = "Fasta/"
    listDir = "protein.csv"
    OutDir = ""

    uniprotId = []
    colSeqProtein = []
    colMetaProtein = []
    rowSeqProtein = []
    rowMetaProtein = []
    rowProtein = []
    colProtein = []
    rowIndex = []
    colIndex = []

    it = 0
    ### MultiProcessing ###
    pool = Pool(processes=poolNum)
    ###################

    ###Parse uniprot ID from csv###
    sys.stderr.write("Parsing input\n")
    with open(listDir,'r') as f:
        csvContent = csv.reader(f,  delimiter=',', quotechar='\"')
        for row in csvContent:
            if (it > 0):
                uniprotId.append(row[2])
            else:
                it = 1
    f.close()
    ###############################

    ###Read file and parse (with library)###

    sys.stderr.write("Load fasta file\n")
    for i in range(len(uniprotId)):
        fastaDir = fastaFileDir + uniprotId[i] + ".fasta"
        with open (fastaDir) as handle:
            recTemp = SeqIO.read(handle, "fasta")
        handle.close()
        recTempMeta = str(recTemp.id)
        recTempMeta = recTempMeta.split("|")
        if i in range(colStart, colEnd):
            colSeqProtein.append(list(recTemp.seq))
            colMetaProtein.append(recTempMeta[1])
        if i in range(rowStart,rowEnd):
            rowSeqProtein.append(list(recTemp.seq))
            rowMetaProtein.append(recTempMeta[1])

    ###Cleanning sequance###
    sys.stderr.write("Cleaning Sequance\n")
    for i in range(nProtRow):
        for j in range(len(rowSeqProtein[i])):
            if(rowSeqProtein[i][j]=='U'):
                rowSeqProtein[i][j]='C'
        rowSeqProtein[i] = "".join(rowSeqProtein[i])

    for i in range(nProtCol):
        for j in range(len(colSeqProtein[i])):
            if(colSeqProtein[i][j]=='U'):
                colSeqProtein[i][j]='C'
        colSeqProtein[i] = "".join(colSeqProtein[i])
    ########################################
    sys.stderr.write("Preparing output file\n")
    outMatDir = OutDir+"RealProtKernel"+str(rowStart)+"_"+str(rowEnd)+".txt"
    outMetaDir = OutDir+"MetaProtKernel"+str(rowStart)+"_"+str(rowEnd)+".txt"
    listScore = []
    with open(outMatDir, 'w') as matF, open(outMetaDir, 'w') as metaF:
        for i in range(nProtRow):
            ###Preparing data for parallel mapping###
            columnCursor = rowStart+i
            while columnCursor < nProtCol:
                if columnCursor+step > colEnd:
                    batchLen = 3334-columnCursor
                else:
                    batchLen = step
                for j in range(columnCursor,columnCursor+batchLen):
                    rowProtein.append(rowSeqProtein[i])
                    rowIndex.append(i)
                    colProtein.append(colSeqProtein[j])
                    colIndex.append(j)
                ### Calculation ###
                listScore = [pool.apply_async(alignprot,(rowProtein[j], colProtein[j], rowIndex[j], colIndex[j],)) for j in range(batchLen)] ###Put into row
                for listS in listScore:
                    simMatProt[listS.get()[1]] = listS.get()[0]
                #Reset value
                colIndex = []
                rowIndex = []
                rowProtein = []
                colProtein = []
                columnCursor += batchLen
                listScore = []

            sys.stderr.write("Writing output\n")
            for j in range(nProtCol):
                if j>0:
                    matF.write(",")
                matF.write(str(simMatProt[j]))
            matF.write("\n")
            metaF.write(rowMetaProtein[i]+"\n")
            simMatProt = [0.0 for k in range(nProtCol)]
    sys.stderr.write("Closing file output\n")
    matF.close()
    metaF.close()

    ##################

def alignprot(rowSeqProtein,colSeqProtein,rowIndex,colIndex):
    sys.stderr.write("\rAligning "+str(rowIndex)+" "+str(colIndex)+",")
    sys.stderr.flush()
    alignres = pairwise2.align.localds(rowSeqProtein,colSeqProtein, blosum62, -1,-1,force_generic = 0, score_only = 1)
    return [alignres, colIndex]


if __name__ == '__main__':
    start = time.time()
    main()
    #############Debugging section#############
    print "Runtime :"+ str(time.time()-start)
    ###########################################
