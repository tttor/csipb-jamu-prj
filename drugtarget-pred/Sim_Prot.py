import numpy as np
import time
import math
from Bio import SeqIO
from Bio import pairwise2
from Bio.SubsMat.MatrixInfo import blosum62

#S-W Alignment

#Parsing

if __name__ == '__main__':

    start = time.time()
    fastaFileDir = "Fasta/";
    listDir = "protein.csv"
    uniprotId = []
    nProt = len(uniprotId)
    seqProtein = []
    metaProtein = []
    simMatProt = np.zeros((len(uniprotId),len(uniprotId)), dtype=float)
    simMatProtNorm = np.zeros((len(uniprotId),len(uniprotId)), dtype=float)
    it = 0
    ###Parse uniprot ID from csv###
    with open(listDir,'r') as f:
        csvContent = csv.reader(f,  delimiter=',', quotechar='\"')
        for row in csvContent:
            if (it > 0):
                uniProtId.append(row[2])
            else:
                it = 1
    ###############################

    ###Read file and parse (with library)###
    for i in range(nProt):
        fastaDir = fastaFileDir + uniprotId[i] + ".fasta"
        recTemp = SeqIO.read(fastaDir, "fasta")
        seqProtein.append((recTemp.seq))
        metaProtein.append(recTemp.id)

    ###Baca an parse (own function) later###

    ########################################

    ### Calculation ###
    #Align all string using waterman with affine gap penalty -1 and extend gap penalty -1
    for i in xrange(nProt):
        for j in xrange(i,nProt):
            simMatProt[i][j] = pairwise2.align.localds(seqProtein[i],seqProtein[j], blosum62, -1,-1,force_generic = 0, score_only = 1)

    #Normalisasi
    for i in xrange(nProt):
        for j in xrange(i,nProt):
            simMatProtNorm[i][j] = simMatProt[i][j]/(math.sqrt(simMatProt[i][i])*math.sqrt(simMatProt[j][j]))

    for i in xrange(nProt):
        for j in xrange(i+1,len(seqProtein)):
            simMatProtNorm[j][i] = simMatProtNorm[i][j]
    ##################

    ###write as txt file###
    outDir = "hasil/ProtKernel.txt"
    with open(outDir,'w') as f:
        for i in range(nProt):
            for j in range(nProt):
                if j>0:
                    f.write(",")
                f.write(str(simMatProtNorm[i][j]))
            f.write("\n")
    f.close()
    outMetaDir = "hasil/MetaProtKernel.txt"
    with open(outMetaDir,'w') as f:
        for i in range(nProt):
            f.write(uniprotId[i]+"\n")
    f.close()
    #######################

    #############Debugging section#############
    # print metaProtein
    print time.time()-start
    ###########################################
