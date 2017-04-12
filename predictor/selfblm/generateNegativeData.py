import csv
import sys
import json
import time
import numpy as np

sys.path.append('../../utility')
import yamanishi_data_util as yam

sys.path.append('../cluster/kmedoid')
import kmedoid as kmed

def main():
    if len(sys.argv)!=6:
        print ("python blmniisvm_experiment.py [e|ic|gpcr|nr] [clustMethod] "
                "[dataPath] [clusterPath] [outPath]")
        return

    dataset = sys.argv[1]
    method = sys.argv[2]
    dataPath = sys.argv[3]
    clusterPath = sys.argv[4]
    outPath = sys.argv[5]

    print "Loading Adjacency"
    connMat,comList,proList = yam.loadComProConnMat(dataset,dataPath+"/Adjacency")
    nComp = len(comList)
    nProtein = len(proList)

    print "Loading Cluster"
    comClust = loadCluster(clusterPath+"/cluster_"+method+"_com_"+dataset+".json",comList)
    proClust = loadCluster(clusterPath+"/cluster_"+method+"_pro_"+dataset+".json",proList)

    print "Generate Negative Data"
    connMat = genNegativeData(connMat,proClust,comClust)

    print "Writing Output To "+outPath
    connMat = [[row[i] for row in connMat] for i in range(len(connMat[0]))]
    with open(outPath+"/admat_dgc_"+dataset+"_negative.txt",'w') as f:
        for i,c in enumerate(comList):
            if i>0:
                f.write(" ")
            f.write(str(c))
        f.write("\n")
        for i,r in enumerate(connMat):
            f.write(proList[i].ljust(7))
            for j,c in enumerate(r):
                f.write(" ")
                f.write(str(c))
            f.write("\n")

    print "Stats: "
    unlabeled = 0
    negative = 0
    positive = 0
    total = nComp*nProtein

    for i in connMat:
        for j in i:
            if j == 0:
                unlabeled += 1
            elif j == -1:
                negative += 1
            elif j == 1:
                positive += 1

    print "Total Data: "+str(total)
    print "Positive Data: "+str(positive)
    print "Unlabeled Data: "+str(unlabeled)
    print "Negative Data: "+str(negative)




def loadCluster(clusterPath,metaList):
    with open(clusterPath,'r') as f:
        data = json.load(f)

    for lab,clust in data.items():
        for i,member in enumerate(clust):
            data[lab][i] = metaList.index(member)

    return data

def genNegativeData(adjMat, proClust,comClust):
    # Change every 0 value to Negative
    m, n = adjMat.shape

    for i in range(m):
        for j in range(n):
            if adjMat[i][j] == 0:
                adjMat[i][j] = -1


                # Check interaction of both cluster
    for cLab,cClust in comClust.items():
        for pLab,pClust in proClust.items():
            intFlag = -1
            pairList = []
            for p in pClust:
                for c in cClust:
                    pairList.append([c,p])
                    if adjMat[c][p] == 1:
                        intFlag = 0
            if intFlag == 0:
                for pair in pairList:
                    if adjMat[pair[0]][pair[1]] == -1:
                        adjMat[pair[0]][pair[1]] = 0

    return adjMat


if __name__ == '__main__':
    start_time = time.time()
    main()
    print "Program is running for :"+str(time.time()-start_time)
