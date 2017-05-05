# deploy.py
import os
import sys
import yaml
import pickle
import json
import numpy as np
from collections import defaultdict
from sklearn import svm
from sklearn.model_selection import train_test_split as tts
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score

sys.path.append('../../utility')
import util
import yamanishi_data_util as yam

XPRMT_DIR = '../../xprmt/imbalance'
DATASET_DIR = '../../dataset/connectivity/compound_vs_protein'

def main():
    if len(sys.argv)!=5:
        print 'USAGE:'
        print 'python -m scoop devel.py [method] [nClone] [dataset#x] [clusterDir]'
        return

    method = sys.argv[1]
    nClone = int(sys.argv[2])
    dataset = sys.argv[3]
    clusterDir = sys.argv[4]

    outDir = os.path.join(XPRMT_DIR,
                          '-'.join(['imbalance',method+'#'+str(nClone),dataset,
                                    util.tag()]))
    os.makedirs(outDir)

    ## Load data
    print 'loading data...'
    dParam = dataset.split('#')
    disMat = None; iList = None
    if dParam[0]=='yamanishi':
        connFpath = os.path.join(clusterDir,'calinskiharabaz_connDict.pkl')
        with open(connFpath,'r') as f:
            data = pickle.load(f)

        simDir = os.path.join(DATASET_DIR,dParam[0],'similarity-mat')
        comSimDict = yam.loadKernel2('compound',dParam[1],simDir)
        proSimDict = yam.loadKernel2('protein',dParam[1],simDir)
    else:
        assert False,'FATAL: unknown dataset'

    print 'getting devel data...'
    xraw = []; yraw = []
    for k,v in data.iteritems():
        for vv in v:
            xraw.append(vv)
            yraw.append(k)

    devIdx = [i for i in range(len(xraw)) if yraw[i]!=0]
    xdev = [xraw[i] for i in devIdx]
    ydev = [yraw[i] for i in devIdx]

    ## DEVEL
    def _makeKernel(xtr1,xtr2):
        mat = np.zeros( (len(xtr1),len(xtr2)) )
        for i in range(mat.shape[0]):
            for j in range(mat.shape[1]):
                mat[i][j] = _getCompoundProteinSim(xtr1[i],xtr2[j])

        return mat

    def _getCompoundProteinSim(i,j):
        comSim = _getCompoundSim(i[0],j[0])
        proSim = _getProteinSim(i[1],j[1])

        alpha = 0.5
        sim = alpha*comSim + (1.0-alpha)*proSim

        return sim

    def _getCompoundSim(i,j):
        return comSimDict[(i,j)]

    def _getProteinSim(i,j):
        return proSimDict[(i,j)]

    results = []
    for i in range(nClone):
        print 'devel clone= '+str(i+1)+'/'+str(nClone)
        xtr,xte,ytr,yte = tts(xdev,ydev,
                              test_size=0.20,random_state=None,stratify=None)

        nTr = 1000
        chosenIdx = np.random.randint(len(xtr),size=nTr)
        xtr = [xtr[i] for i in chosenIdx]
        ytr = [ytr[i] for i in chosenIdx]

        ## tuning
        clf = svm.SVC(kernel='precomputed')

        ## train
        simMatTr = _makeKernel(xtr,xtr)
        clf.fit(simMatTr,ytr)

        ## test
        simMatTe = _makeKernel(xte,xtr)
        ypred = clf.predict(simMatTe)

        _ = {'xtr':xtr,'xte':xte,'ytr':ytr,'yte':yte,'ypred':ypred}
        results.append(_)

    # devel perf
    perfs = defaultdict(list)
    for r in results:
        coka = cohen_kappa_score(r['yte'],r['ypred'])
        aupr = average_precision_score(r['yte'],r['ypred'],average='micro')
        perfs['cohen_kappa_score'].append(coka)
        perfs['average_precision_score'].append(aupr)

    fpath = os.path.join(outDir,'perfs.json')
    with open(fpath,'w') as f: json.dump(perfs,f,indent=2,sort_keys=True)

if __name__ == '__main__':
    main()
