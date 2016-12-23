import numpy as np
import time
import math
import csv
import sys

from Bio import SeqIO
from Bio import pairwise2
from Bio.SubsMat.MatrixInfo import blosum62
from scoop import futures
#S-W Alignment

#Parsing
def alignprot(rowSeqProtein,colSeqProtein,i,j):
    alignres = pairwise2.align.localds(rowSeqProtein,colSeqProtein, blosum62, -1,-1,force_generic = 0, score_only = 1)
    return [alignres, i, j]

if __name__ == '__main__':
    start = time.time()

    rowStart = int(sys.argv[1])-1
    rowEnd = int(sys.argv[2])
    colStart = int(sys.argv[3])-1
    colEnd = int(sys.argv[4])

    nProtCol = colEnd-colStart
    nProtRow = rowEnd-rowStart

    simMatProtNorm = np.zeros((nProtRow,nProtCol), dtype=float)
    simMatProt = np.zeros((nProtRow,nProtCol), dtype=float)
    selfSimScoreCol = np.zeros((nProtCol), dtype=float)
    selfSimScoreRow =  np.zeros((nProtRow), dtype=float)
    fastaFileDir = "Fasta/"
    listDir = "protein.csv"
    outDir = "hasil/"

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
        rowMetaProtein.append(recTemp.id)

    for i in xrange(colStart,colEnd):
        fastaDir = fastaFileDir + uniprotId[i] + ".fasta"
        recTemp = SeqIO.read(fastaDir, "fasta")
        colSeqProtein.append(list(recTemp.seq))
        colMetaProtein.append(recTemp.id)

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

    ###Preparing data for parallel mapping###
    #sequance
    for i in range(nProtRow):
        for j in xrange(nProtCol):
            rowProtein.append(rowSeqProtein[i])

    for i in range(nProtRow):
        for j in xrange(nProtCol):
            colProtein.append(colSeqProtein[j])

    #index
    for i in range(nProtRow):
        for j in xrange(nProtCol):
            rowIndex.append(i)

    for i in range(nProtRow):
        for j in xrange(nProtCol):
            colIndex.append(j)

    ########################################
    ### Calculation ###
    #Align all string using waterman with affine gap penalty -1 and extend gap penalty -1
    selfSimRow = list(futures.map(alignprot, rowSeqProtein, rowSeqProtein, [i for i in range(nProtRow)], [i for i in range(nProtRow)]))
    selfSimCol = list(futures.map(alignprot, colSeqProtein, colSeqProtein, [i for i in range(nProtCol)], [i for i in range(nProtCol)]))
    listScore = list(futures.map(alignprot, rowProtein, colProtein, rowIndex, colIndex))

    for i in range(nProtRow):
        selfSimScoreRow[selfSimRow[i][1]] = selfSimRow[i][0]

    for i in range(nProtCol):
        selfSimScoreCol[selfSimCol[i][1]] = selfSimCol[i][0]

    for i in range(len(listScore)):
        simMatProt[listScore[i][1]][listScore[i][2]] = listScore[i][0]

    #Normalisasi
    for i in range(nProtRow):
        for j in range(nProtCol):
            simMatProtNorm[i][j] = simMatProt[i][j]/(math.sqrt(selfSimScoreRow[i])*math.sqrt(selfSimScoreCol[j]))

    #Mirror Result
    # for i in xrange(nProtrow):
    #     for j in xrange(i+1,nProtCol):
    #         simMatProtNorm[j][i] = simMatProtNorm[i][j]
    ##################

    ###write as txt file###
    outMatDir = outDir+"NormProtKernel.txt"
    with open(outMatDir,'w') as f:
        for i in range(nProtRow):
            for j in range(nProtCol):
                if j>0:
                    f.write(",")
                f.write(str(simMatProtNorm[i][j]))
            f.write("\n")
    f.close()

    outMatDir = outDir+"RealProtKernel.txt"
    with open(outMatDir,'w') as f:
        for i in range(nProtRow):
            for j in range(nProtCol):
                if j>0:
                    f.write(",")
                f.write(str(simMatProt[i][j]))
            f.write("\n")
    f.close()

    outMetaDir = outDir+"MetaProtKernel.txt"
    with open(outMetaDir,'w') as f:
        f.write("\t")
        for i in range(nProtCol):
            f.write(colMetaProtein[i]+" ")
        f.write("\n")
        for i in range(nProtRow):
            f.write(rowMetaProtein[i]+"\n")

    f.close()
    #######################

    #############Debugging section#############
    print "Runtime :"+ str(time.time()-start)
    ###########################################
