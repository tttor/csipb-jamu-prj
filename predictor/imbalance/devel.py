# deploy.py
import os
import sys
import yaml
import pickle
import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split as tts
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score

sys.path.append('../../utility')
import util
import yamanishi_data_util as yam

XPRMT_DIR = '../../xprmt'
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
    nClone = 3
    for i in range(nClone):
        xtr,xte,ytr,yte = tts(xdev,ydev,test_size=0.20,random_state=42)

        ## tuning
        clf = svm.SVC(kernel='precomputed')

        ## train
        comList = list(set([i[0] for i in xtr]))
        comSimMatTr,_ = util.makeKernelMatrix(comSimDict,comList)
        proSimMatTr = None
        phaSimMatTr = None
        simMatTr = _mergeKernel(comSimMatTr,proSimMatTr,phaSimMatTr)

        print len(xtr)
        print simMatTr.shape

        n = 40000
        mat = np.zeros((n,n))
        print mat.shape
        # clf.fit(simMatTr,ytr)

        # ## test
        # ypred = clf.predict(xte)
        # cokaScore = cohen_kappa_score(yte, ypred)

        # ## test eval
        # print 'calculating aupr...'
        # precision, recall, _ = precision_recall_curve(yte,ypred)
        # aupr = average_precision_score(yte,ypred,average='micro')
        # print aupr

        return

    ## devel perf

def _mergeKernel(comSimMatTr,proSimMatTr,phaSimMatTr):
    return comSimMatTr

def _tune():
    pass

if __name__ == '__main__':
    main()
