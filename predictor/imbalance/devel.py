# devel.py
import os
import sys
import yaml
import pickle
import json
import time
import shutil
import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split as tts
from ensembled_svm import EnsembledSVM as eSVM

sys.path.append('../../utility')
import util
import yamanishi_data_util as yam
import classifier_util as cutil

from devel_config import config as cfg

def main():
    if len(sys.argv)!=3:
        print 'USAGE:'
        print 'python -m scoop devel.py [clusterDir] [cloneID]'
        print 'see devel_config.py'
        return

    clusterDir = sys.argv[1]# assume: ended with '/'
    cloneID = sys.argv[2]

    method = cfg['method']['name']
    if method not in ['esvm','psvm']:
        print 'FATAL: unknown method'
        return
    print 'method: '+method

    log = {}
    seed = util.seed(); log['seed'] = seed
    np.random.seed(seed)

    dataset = clusterDir.split('/')[-2].split('-')[-1]; log['dataset'] = dataset
    outDir = os.path.join('./output',
                          '-'.join([method+'#'+cloneID,dataset,util.tag()]))
    os.makedirs(outDir)
    shutil.copy2('devel_config.py',outDir)

    ## Load data ###################################################################################
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

    log['nDevel'] = len(devIdx); log['nData'] = len(yraw)
    log['rDevel:Data'] = log['nDevel']/float(log['nData'])
    log['nDevel(+)'] = len( [i for i in ydev if i==1] ); assert log['nDevel(+)']!=0
    log['nDevel(-)'] = len( [i for i in ydev if i==-1] ); assert log['nDevel(-)']!=0
    log['rDevel(+):Devel'] = float(log['nDevel(+)'])/log['nDevel']
    log['rDevel(-):Devel'] = float(log['nDevel(-)'])/log['nDevel']
    log['rDevel(+):(-)'] = float(log['nDevel(+)'])/float(log['nDevel(-)'])
    print 'nDevel: '+str(log['nDevel'])+'/'+str(log['nData'])+' = '+str(log['rDevel:Data'])

    ## DEVEL #######################################################################################
    msg = 'devel '+dataset+' '+cloneID
    xtr,xte,ytr,yte = tts(xdev,ydev,test_size=cfg['testSize'],
                          random_state=seed,stratify=ydev)

    if cfg['maxTestingSamples']>0:
        chosenIdx = np.random.randint(len(xte),size=cfg['maxTestingSamples'])
        xte = [xte[i] for i in chosenIdx]; yte = [yte[i] for i in chosenIdx]

    log['nTraining'] = len(xtr)
    log['nTraining(+)'] = len([i for i in ytr if i==1])
    log['nTraining(-)'] = len([i for i in ytr if i==-1])
    log['rTraining(+):(-)'] = log['nTraining(+)']/float(log['nTraining(-)'])
    log['rTraining:Devel'] = log['nTraining']/float(log['nDevel'])

    log['nTesting'] = len(xte)
    log['nTesting(+)'] = len([i for i in yte if i==1])
    log['nTesting(-)'] = len([i for i in yte if i==-1])
    log['rTesting(+):(-)'] = log['nTesting(+)']/float(log['nTesting(-)'])
    log['rTesting:Devel'] = log['nTesting']/float(log['nDevel'])

    ##
    clf = None
    if method=='esvm':
        clf  = eSVM(cfg['method']['mode'],
                    cfg['method']['maxTrainingSamplesPerBatch'],
                    cfg['method']['maxTestingSamplesPerBatch'],
                    cfg['method']['bootstrap'],
                    {'com':comSimDict,'pro':proSimDict})
    elif method=='psvm':
        clf = svm.SVC(kernel='precomputed',probability=True)

    ##
    print msg+': fitting nTr= '+str(len(ytr))
    if method=='esvm':
        clf.fit(xtr,ytr)
        clf.writeLabels(outDir)
        log['nSVM'] = clf.nSVM()
    elif method=='psvm':
        simMatTr = cutil.makeKernel(xtr,xtr,{'com':comSimDict,'pro':proSimDict})
        clf.fit(simMatTr,ytr)

    ##
    print msg+': predicting nTe= '+str(len(yte))
    if method=='esvm':
        ypred,yscore = clf.predict(xte)
    elif method=='psvm':
        simMatTe = cutil.makeKernel(xte,xtr,{'com':comSimDict,'pro':proSimDict})
        ypred = clf.predict(simMatTe)
        yscore = clf.predict_proba(simMatTe)

    result = {'xtr':xtr,'xte':xte,'ytr':ytr,'yte':yte,'ypred':ypred,'yscore':yscore}
    with open(os.path.join(outDir,"result.pkl"),'w') as f: pickle.dump(result,f)
    with open(os.path.join(outDir,'log.json'),'w') as f: json.dump(log,f,indent=2,sort_keys=True)

if __name__ == '__main__':
    tic = time.time()
    main()
    print "main took: "+str(time.time()-tic)+' seconds'
