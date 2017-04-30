# cluster.py
import os
import sys
import time
import json
import numpy as np
import sklearn.metrics as met
from scoop import futures as fu
from scoop import shared as sh

sys.path.append('../../utility')
import util
import yamanishi_data_util as yam

# np.random.seed(0)

def main():
    if len(sys.argv)!=6:
        print 'USAGE:'
        print 'python -m scoop cluster.py [method] [nIter] [dataset] [dataDir] [outDir]'
        return

    method = sys.argv[1]
    nIter = int(sys.argv[2])
    dataset = sys.argv[3]
    dataDir = sys.argv[4]
    outDir = os.path.join(sys.argv[5],'-'.join(['cluster',method,str(nIter),util.tag()]))
    os.makedirs(outDir)

    ##
    _,comList,proList = yam.loadComProConnMat(dataset,os.path.join(dataDir,'ground-truth'))
    kernelDict = yam.loadKernel(dataset,os.path.join(dataDir,'similarity-mat'))
    comSimMat,proSimMat = util.makeKernelMatrix(kernelDict,comList,proList)
    comDisMat,proDisMat = list(map(util.kernel2distanceMatrix,['naive']*2,[comSimMat,proSimMat]))

    ##
    print 'clustering...'
    paramSpace = {"eps": [0.0,1.0],"min_samples":[1,5]}
    paramList = _elaborateParamSpace(paramSpace,nIter,method)

    sh.setConst(method=method)
    sh.setConst(mat=comDisMat)

    comResList = list( fu.map(_cluster,paramList) )
    bestResIdxCal = _getBestResultIdx(comResList,'calinski_harabaz_score')
    bestResIdxSil = _getBestResultIdx(comResList,'silhouette_score')

    resDictCal = dict( zip(comList,comResList[bestResIdxCal][0]) )
    resDictSil = dict( zip(comList,comResList[bestResIdxSil][0]) )

    bestParamCal = dict(param=paramList[bestResIdxCal],
                        score=comResList[bestResIdxCal][1])
    bestParamSil = dict(param=paramList[bestResIdxSil],
                        score=comResList[bestResIdxSil][1])

    ##
    fname = method+"_"+'calinskiharabazscore'+"_clusterlabels.json"
    with open(os.path.join(outDir,fname),'w') as f:
        json.dump(resDictCal,f,indent=2,sort_keys=True)

    fname = method+"_"+'silhouettescore'+"_clusterlabels.json"
    with open(os.path.join(outDir,fname),'w') as f:
        json.dump(resDictSil,f,indent=2,sort_keys=True)

    fname = method+"_"+'calinskiharabazscore'+"_bestparam.json"
    with open(os.path.join(outDir,fname),'w') as f:
        json.dump(bestParamCal,f,indent=2,sort_keys=True)

    fname = method+"_"+'silhouettescore'+"_bestparam.json"
    with open(os.path.join(outDir,fname),'w') as f:
        json.dump(bestParamSil,f,indent=2,sort_keys=True)

def _cluster(params):
    cls = None
    method = sh.getConst('method')
    if method=='kmedoid':
        assert False
        # from kmedoid import kmedsoid
        # cls = kmedoid
    elif method=='dbscan':
        from sklearn.cluster import DBSCAN
        cls = DBSCAN(eps=params['eps'],min_samples=params['min_samples'],
                     metric='precomputed')
    else:
        assert False, 'FATAL: unknown cluster method'

    ##
    mat = sh.getConst('mat')
    labels = cls.fit_predict(mat)
    nLabels = len(set(labels))

    ##
    sil = None; cal = None
    if (nLabels >= 2)and(nLabels <= len(labels)-1):
        sil = met.silhouette_score(mat,labels,'precomputed')
        cal = met.calinski_harabaz_score(mat,labels)
    perf = dict(silhouette_score=sil,calinski_harabaz_score=cal)

    return (labels,perf)

def _elaborateParamSpace(paramSpace,nIter,method):
    paramList = []
    for i in range(nIter):
        if method=='dbscan':
            epsMin,epsMax = paramSpace['eps']
            nMin,nMax = paramSpace['min_samples']

            eps = np.random.uniform(epsMin,epsMax,1)[0]
            n = np.random.randint(nMin,nMax,1)[0]
            param = dict(eps=eps,min_samples=n)
            paramList.append(param)
        else:
            assert False
    return paramList

def _getBestResultIdx(resList,metric):
    mets = [i[1][metric] for i in resList]
    return mets.index(max(mets))

if __name__ == '__main__':
    tic = time.time()
    main()
    print "main took: "+str(time.time()-tic)+' seconds'
