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
    if len(sys.argv)!=3:
        print 'USAGE:'
        print 'python -m scoop devel.py [clusterDir] [cloneID]'
        print 'see devel_config.py'
        return

    clusterDir = sys.argv[1]# assume: ended with '/'
    cloneID = sys.argv[2]

    dataset = clusterDir.split('/')[-2].split('-')[-1]
    outDir = os.path.join('./output',
                          '-'.join([cfg['method']+'#'+cloneID,dataset,util.tag()]))
    os.makedirs(outDir)
    shutil.copy2('devel_config.py',outDir)
    log = {}

    ## Load data
    print 'loading data...'
    datasetParams = dataset.split('#')
    if datasetParams[0]=='yamanishi':
        nUnlabels = []
        statFnames = [i for i in os.listdir(clusterDir) if 'labels_stat.json' in i]
        for i in statFnames:
            with open(os.path.join(clusterDir,i),'r') as f: stat = yaml.load(f)
            nUnlabels.append(stat['0'])
        metric = '_'.join(statFnames[ nUnlabels.index(min(nUnlabels)) ].split('_')[0:2])
        log['metric'] = metric

        connFpath = os.path.join(clusterDir,metric+'_labels.pkl')
        with open(connFpath,'r') as f: data = pickle.load(f)
        simDir = os.path.join(cfg['datasetDir'],datasetParams[0],'similarity-mat')
        comSimDict = yam.loadKernel2('compound',datasetParams[1],simDir)
        proSimDict = yam.loadKernel2('protein',datasetParams[1],simDir)
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

    log['nDevel(+)'] = len( [i for i in ydev if i==1] )
    log['nDevel(-)'] = len( [i for i in ydev if i==-1] )
    log['nDevel'] = len(devIdx); log['nData'] = len(yraw)
    log['rDevel'] = float(len(devIdx))/len(yraw)
    log['rDevel(+)'] = float(log['nDevel(+)'])/log['nDevel']
    log['rDevel(-)'] = float(log['nDevel(-)'])/log['nDevel']
    print 'nDevel: '+str(log['nDevel'])+'/'+str(log['nData'])+' = '+str(log['rDevel'])
    with open(os.path.join(outDir,'log.json'),'w') as f: json.dump(log,f,indent=2,sort_keys=True)

    ## DEVEL
    msg = 'devel '+dataset+' '+cloneID
    xtr,xte,ytr,yte = tts(xdev,ydev,test_size=cfg['testSize'],
                          random_state=None,stratify=ydev)

    esvm = eSVM(cfg['maxTrainingSamplesPerBatch'],
                cfg['maxTestingSamplesPerBatch'],
                cfg['bootstrap'],
                {'com':comSimDict,'pro':proSimDict})

    ##
    print msg+': fitting nTr= '+str(len(ytr))
    esvm.fit(xtr,ytr)

    ##
    if cfg['maxTestingSamples']>0:
        chosenIdx = np.random.randint(len(xte),size=cfg['maxTestingSamples'])
        xte = [xte[i] for i in chosenIdx]; yte = [yte[i] for i in chosenIdx]

    print msg+': predicting nTe= '+str(len(yte))
    ypred = esvm.predict(xte,cfg['mode'])

    result = {'xtr':xtr,'xte':xte,'ytr':ytr,'yte':yte,'ypred':ypred}
    with open(os.path.join(outDir,"result.pkl"),'w') as f: pickle.dump(result,f)

    ##
    print msg+': getting perf...'
    perf = {}
    coka = cohen_kappa_score(result['yte'],result['ypred'])
    aupr = average_precision_score(result['yte'],result['ypred'],average='micro')
    perf['cohen_kappa_score'] = coka
    perf['average_precision_score'] = aupr

    fpath = os.path.join(outDir,'perf.json')
    with open(fpath,'w') as f: json.dump(perf,f,indent=2,sort_keys=True)

if __name__ == '__main__':
    tic = time.time()
    main()
    print "main took: "+str(time.time()-tic)+' seconds'
