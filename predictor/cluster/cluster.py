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

DATASET_DIR = '../../dataset/connectivity/compound_vs_protein'
XPRMT_DIR = '../../xprmt/cluster'

def main():
    if len(sys.argv)!=5:
        print 'USAGE:'
        print 'python -m scoop cluster.py [method] [nIter] [dataset] [compound/protein]'
        return

    method = sys.argv[1]
    nIter = int(sys.argv[2])
    dataset = sys.argv[3]
    mode = sys.argv[4]

    outDir = os.path.join(XPRMT_DIR,
                          '-'.join(['cluster',method+'#'+str(nIter),dataset,mode,
                                    util.tag()]))
    os.makedirs(outDir)

    ##
    print 'loading data...'
    dParam = dataset.split('#')
    disMat = None; iList = None
    if dParam[0]=='yamanishi':
        dataDir = os.path.join(DATASET_DIR,dParam[0])
        simDict = yam.loadKernel2(mode,dParam[1],os.path.join(dataDir,'similarity-mat'))
        simMat,iList = util.makeKernelMatrix(simDict)
        disMat = util.kernel2distanceMatrix('naive',simMat)
    else:
        assert False,'FATAL: unknown dataset'

    ##
    print 'clustering...'
    paramSpace = {"eps": [0.0,1.0],"min_samples":[1,5]}
    paramList = _elaborateParamSpace(paramSpace,nIter,method)

    sh.setConst(method=method)
    sh.setConst(mat=disMat)

    resList = list( fu.map(_cluster,paramList) )
    bestResIdxCal = _getBestResultIdx(resList,'calinski_harabaz_score')
    bestResIdxSil = _getBestResultIdx(resList,'silhouette_score')

    resDictCal = dict( zip(iList,resList[bestResIdxCal][0]) )
    resDictSil = dict( zip(iList,resList[bestResIdxSil][0]) )

    bestParamCal = dict(param=paramList[bestResIdxCal],
                        score=resList[bestResIdxCal][1])
    bestParamSil = dict(param=paramList[bestResIdxSil],
                        score=resList[bestResIdxSil][1])

    ##
    print 'writing result...'
    def _writeLabelAndParam(metric,resDict,paramDict):
        fname = '_'.join(['cluster',mode,metric])
        with open(os.path.join(outDir,fname+"_bestlabels.json"),'w') as f:
            json.dump(resDict,f,indent=2,sort_keys=True)
        with open(os.path.join(outDir,fname+"_bestparams.json"),'w') as f:
            json.dump(paramDict,f,indent=2,sort_keys=True)

    _writeLabelAndParam('calinskiharabaz',resDictCal,bestParamCal)
    _writeLabelAndParam('silhouette',resDictSil,bestParamSil)

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
