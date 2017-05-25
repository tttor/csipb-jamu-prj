# devel.py
import os
import sys
import yaml
import pickle
import json
import time
import shutil
import numpy as np
from collections import defaultdict
from sklearn.model_selection import train_test_split as tts
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score

from ensembled_svm import EnsembledSVM as eSVM

sys.path.append('../../utility')
import util
import yamanishi_data_util as yam

from devel_config import config as cfg

def main():
    if len(sys.argv)!=1:
        print 'USAGE:'
        print 'python -m scoop devel.py'
        print 'see devel_config.py'
        return

    dataset = cfg['clusterDir'].split('/')[-1].split('-')[-1]
    outDir = os.path.join('./output',
                          '-'.join(['imbalance',
                                    cfg['method']+'#'+str(cfg['nClone']),
                                    dataset,cfg['clusterMetric'],util.tag()]))
    os.makedirs(outDir)
    shutil.copy2('devel_config.py',outDir)

    ## Load data
    print 'loading data...'
    dParam = dataset.split('#')
    disMat = None; iList = None
    if dParam[0]=='yamanishi':
        connFpath = os.path.join(cfg['clusterDir'],cfg['clusterMetric']+'_labels.pkl')
        with open(connFpath,'r') as f:
            data = pickle.load(f)

        simDir = os.path.join(cfg['datasetDir'],dParam[0],'similarity-mat')
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
    print 'nDevel: '+str(len(devIdx))+'/'+str(len(yraw))+' = '+str(float(len(devIdx))/len(yraw))

    ## DEVEL
    results = []
    for i in range(cfg['nClone']):
        msg = 'devel clone: '+str(i+1)+'/'+str(cfg['nClone'])
        print msg
        xtr,xte,ytr,yte = tts(xdev,ydev,test_size=cfg['testSize'],
                              random_state=None,stratify=ydev)

        esvm = eSVM(cfg['maxTrainingSamplesPerBatch'],
                    cfg['maxTestingSamplesPerBatch'],
                    cfg['bootstrap'],
                    {'com':comSimDict,'pro':proSimDict},msg)

        ##
        print msg+': fitting nTr= '+str(len(ytr))
        esvm.fit(xtr,ytr)

        ##
        if cfg['maxTestingSamples']>0:
            chosenIdx = np.random.randint(len(xte),size=cfg['maxTestingSamples'])
            xte = [xte[i] for i in chosenIdx]; yte = [yte[i] for i in chosenIdx]

        print msg+': predicting nTe= '+str(len(yte))
        ypred = esvm.predict(xte,cfg['mode'])

        results.append( {'xtr':xtr,'xte':xte,'ytr':ytr,'yte':yte,'ypred':ypred} )
        with open(os.path.join(outDir,"results.pkl"),'w') as f: pickle.dump(results,f)

    # devel perf
    print 'getting perf...'
    perf = defaultdict(list)
    for r in results:
        coka = cohen_kappa_score(r['yte'],r['ypred'])
        aupr = average_precision_score(r['yte'],r['ypred'],average='micro')
        perf['cohen_kappa_score'].append(coka)
        perf['average_precision_score'].append(aupr)

    fpath = os.path.join(outDir,'perf.json')
    with open(fpath,'w') as f: json.dump(perf,f,indent=2,sort_keys=True)

    perfAvg = {}; fpath = os.path.join(outDir,'perf_avg.json')
    for k,v in perf.iteritems(): perfAvg[k] = [np.mean(v),np.std(v)]
    with open(fpath,'w') as f: json.dump(perfAvg,f,indent=2,sort_keys=True)

if __name__ == '__main__':
    tic = time.time()
    main()
    print "main took: "+str(time.time()-tic)+' seconds'
