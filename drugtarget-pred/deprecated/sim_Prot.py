import numpy as np
import time
import math
import csv
import sys

from Bio import SeqIO
from Bio import pairwise2
from Bio.SubsMat.MatrixInfo import blosum62
from scoop import futures


#Parsing

def alignprot(rowSeqProtein,colSeqProtein,i,j):
    alignres = pairwise2.align.localds(rowSeqProtein,colSeqProtein, blosum62, -1,-1,force_generic = 0, score_only = 1)
    print str(i)+" "+str(j)
    return [alignres, j]


if __name__ == '__main__':
    start = time.time()

    rowStart = int(sys.argv[1])-1
    rowEnd = int(sys.argv[2])
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

    ###Parse uniprot ID from csv###
    with open(listDir,'r') as f:
        csvContent = csv.reader(f,  delimiter=',', quotechar='\"')
        for row in csvContent:
            if (it > 0):
                uniprotId.append(row[2])
            else:
                it = 1
    ###############################

    ###Read file and parse (with library)###
    for i in xrange(rowStart,rowEnd):
        fastaDir = fastaFileDir + uniprotId[i] + ".fasta"
        recTemp = SeqIO.read(fastaDir, "fasta")
        rowSeqProtein.append(list(recTemp.seq))
        recTemp = str(recTemp.id)
        recTemp = recTemp.split("|")
        rowMetaProtein.append(recTemp[1])

    for i in xrange(colStart,colEnd):
        fastaDir = fastaFileDir + uniprotId[i] + ".fasta"
        recTemp = SeqIO.read(fastaDir, "fasta")
        colSeqProtein.append(list(recTemp.seq))
        recTemp = str(recTemp.id)
        recTemp = recTemp.split("|")
        colMetaProtein.append(recTemp[1])

    ###Cleanning sequance###
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
    #sequance
    outMatDir = OutDir+"RealProtKernel"+str(rowStart+1)+"_"+str(rowEnd)+".txt"
    outMetaDir = OutDir+"MetaProtKernel"+str(rowStart+1)+"_"+str(rowEnd)+".txt"
    listScore = []
    with open(outMatDir, 'w') as matF, open(outMetaDir, 'w') as metaF:
        for i in range(nProtRow):
            ###Preparing data for parallel mapping###
            for j in xrange(rowStart+i,nProtCol):
                rowProtein.append(rowSeqProtein[i])
                colProtein.append(colSeqProtein[j])
                rowIndex.append(i)
                colIndex.append(j)
            ### Calculation ###
            listScore = list(futures.map(alignprot, rowProtein, colProtein, rowIndex, colIndex))
            ###Put into row
            for j in range(len(listScore)):
                simMatProt[listScore[j][1]] = listScore[j][0]

            ###Print Row
            for j in range(nProtCol):
                if j>0:
                    matF.write(",")
                matF.write(str(simMatProt[j]))
            matF.write("\n")
            metaF.write(rowMetaProtein[i]+"\n")
            #Reset value
            colIndex = []
            rowIndex = []
            rowProtein = []
            colProtein = []
            listScore = []
            simMatProt = [0.0 for i in range(nProtCol)]

    matF.close()
    metaF.close()
    ##################

    #############Debugging section#############
    print "Runtime :"+ str(time.time()-start)
    ###########################################
