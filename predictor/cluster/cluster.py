# cluster.py
import os
import sys
import time
import json
import sklearn.metrics as met
from sklearn.model_selection import RandomizedSearchCV as rscv

sys.path.append('../../utility')
import util
import yamanishi_data_util as yam

def main():
    if len(sys.argv)!=5:
        print 'USAGE:'
        print 'python cluster.py [method] [dataset] [dataDir] [outDir]'
        return

    method = sys.argv[1]
    dataset = sys.argv[2]
    dataDir = sys.argv[3]
    outDir = sys.argv[4]

    ##
    cls = None
    if method=='kmedoid':
        from kmedoid import kmedoid
        cls = kmedoid
    elif method=='dbscan':
        from sklearn.cluster import DBSCAN
        cls = DBSCAN(eps=0.75,min_samples=1,metric='precomputed')
    else:
        assert False, 'FATAL: unknown cluster method'

    ##
    _,comList,proList = yam.loadComProConnMat(dataset,os.path.join(dataDir,'ground-truth'))
    kernelDict = yam.loadKernel(dataset,os.path.join(dataDir,'similarity-mat'))
    comSimMat,proSimMat = util.makeKernelMatrix(kernelDict,comList,proList)
    comDisMat,proDisMat = list(map(util.kernel2distanceMatrix,['naive']*2,[comSimMat,proSimMat]))

    ##
    random_search = rscv(cls, param_distributions=param_dist,
                                        n_iter=n_iter_search)

start = time()
random_search.fit(X, y)
print("RandomizedSearchCV took %.2f seconds for %d candidates"
      " parameter settings." % ((time() - start), n_iter_search))
report(random_search.cv_results_)

    ##
    print 'clustering...'
    comLabels,proLabels = list( map(cls.fit_predict,[comDisMat,proDisMat]) )
    comLabels = comLabels.tolist(); proLabels = proLabels.tolist()

    ##
    print 'eval...'
    comSil,proSil = list(map(met.silhouette_score,
                            [comDisMat,proDisMat],[comLabels,proLabels],
                            ['precomputed']*2))
    comCal,proCal = list(map(met.calinski_harabaz_score,
                            [comDisMat,proDisMat],[comLabels,proLabels]))

    perf = dict(comCluster={'silhouette_score':comSil,'calinski_harabaz_score':comCal},
                proCluster={'silhouette_score':proSil,'calinski_harabaz_score':proCal})

    with open(os.path.join(outDir+"perf.json"),'w') as f:
        json.dump(perf,f,indent=2,sort_keys=True)

if __name__ == '__main__':
    tic = time.time()
    main()
    print "main: "+str(time.time()-tic)+' seconds'
