import random
import csv
import sys
import time
import json

import numpy as np
import sklearn.metrics as met
sys.path.append('../../../utility')
import yamanishi_data_util as yam

def main():
    if len(sys.argv)!=4:
        print "Usage: python kmedoid.py [e|ic|gpcr|nr] [dataDir] [outputDir]"
        return

    dataPath = sys.argv[1]
    dataset = sys.argv[2]
    outPath = sys.argv[3]

    # Load file
    print "Preparing data"
    _,comList,proList = yam.loadComProConnMat(dataset,dataPath+"/Adjacency")
    kernel = yam.loadKernel(dataset,dataPath)

    nComp = len(comList)
    nProtein = len(proList)

    comSimMat = np.zeros((nComp,nComp), dtype=float)
    proSimMat = np.zeros((nProtein,nProtein), dtype=float)

    for row,i in enumerate(comList):
        for col,j in enumerate(comList):
            comSimMat[row][col] = kernel[(i,j)]

    for row,i in enumerate(proList):
        for col,j in enumerate(proList):
            proSimMat[row][col] = kernel[(i,j)]

    # convert similarity matrix to distance Matrix
    proDisMat = simToDis(proSimMat)
    comDisMat = simToDis(comSimMat)

    print "Clustering"
    proMedoid,proClust = kMedoids(len(proList)/2, proDisMat)
    comMedoid,comClust = kMedoids(len(comList)/2, comDisMat)
    # Take each label for each sample
    comLabelList = np.zeros((nComp))
    proLabelList = np.zeros((nProtein))
    proMetaClust = dict()
    comMetaClust = dict()

    for lab in proClust:
        meta = []
        for idx in proClust[lab]:
            meta.append(proList[idx])
            proLabelList[idx] = lab
        proMetaClust[lab] = meta


    for lab in comClust:
        meta = []
        for idx in comClust[lab]:
            meta.append(comList[idx])
            comLabelList[idx] = lab
        comMetaClust[lab] = meta

    print "Evaluation"

    comSilhouette = met.silhouette_score(comDisMat,comLabelList,metric="precomputed")
    proSilhouette = met.silhouette_score(proDisMat,proLabelList,metric="precomputed")

    comCalinskiHarabaz = met.calinski_harabaz_score(comDisMat,comLabelList)
    proCalinskiHarabaz = met.calinski_harabaz_score(proDisMat,proLabelList)

    print ("Silhouette score :\nCompound cluster = "+str(comSilhouette)+
            ",Protein cluster = "+str(proSilhouette))

    print ("Calinski Harabaz score :\nCompound cluster = "+str(comCalinskiHarabaz)+
            ", Protein cluster = "+str(proCalinskiHarabaz))

    print "Writing Output"

    perf = {'silhouette_score_':{'compound':comSilhouette,'protein':proSilhouette},
            'calinski_harabaz_score':{'compound':comCalinskiHarabaz,'protein':
            proCalinskiHarabaz}}

    with open(outPath+"/perf_medoid_"+dataset+".json",'w') as f:
        json.dump(perf,f, indent=2, sort_keys=True)

    with open(outPath+"/cluster_medoid_com_"+dataset+".json",'w') as f:
        json.dump(comMetaClust,f, indent=2, sort_keys=True)

    with open(outPath+"/cluster_medoid_pro_"+dataset+".json",'w') as f:
        json.dump(proMetaClust,f, indent=2, sort_keys=True)

def simToDis(simMat):
    m,n = simMat.shape
    disMat = np.zeros((m,n),dtype=float)
    for i in range(m):
        for j in range(n):
            disMat[i][j] = 1.0000000 - simMat[i][j]
    return disMat

# TAKEN FROM https://github.com/letiantian/kmedoids
# Citation Bauckhage C. Numpy/scipy Recipes for Data Science: k-Medoids Clustering[R]. Technical Report, University of Bonn, 2015.
# Still possible to raise an error on random chance
def kMedoids(k,D, tmax=100):
    # determine dimensions of distance matrix D
    m, n = D.shape

    if k > n:
        raise Exception('too many medoids')
    # randomly initialize an array of k medoid indices
    M = np.arange(n)
    np.random.shuffle(M)
    M = np.sort(M[:k])

    # create a copy of the array of medoid indices
    Mnew = np.copy(M)

    # initialize a dictionary to represent clusters
    C = {}
    for t in xrange(tmax):
        # determine clusters, i. e. arrays of data indices
        J = np.argmin(D[:,M], axis=1)
        for kappa in range(k):
            C[kappa] = np.where(J==kappa)[0]

        # update cluster medoids
        for kappa in range(k):
            # ---------------------------------
                # if there is a cluster with no member Re-do clustering

            if D[np.ix_(C[kappa],C[kappa])].size == 0:
                med,clust = kMedoids(k,D)
                return med,clust
            J = np.mean(D[np.ix_(C[kappa],C[kappa])],axis=1)
            j = np.argmin(J)
            # ---------------------------------
            Mnew[kappa] = C[kappa][j]
        np.sort(Mnew)
        # check for convergence
        if np.array_equal(M, Mnew):
            break
        M = np.copy(Mnew)
    else:
        # final update of cluster memberships
        J = np.argmin(D[:,M], axis=1)
        for kappa in range(k):
            C[kappa] = np.where(J==kappa)[0]

    # return results
    return M, C

if __name__ == "__main__":
    start_time = time.time()
    main()
    print "Program is running for "+str(time.time()-start_time)
