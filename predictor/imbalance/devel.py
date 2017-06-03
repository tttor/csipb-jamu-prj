# devel.py
import os
import sys
import yaml
import pickle
import json
import time
import shutil
import h5py
import numpy as np
from scoop import futures as fu
from scoop import shared as sh
from sklearn import svm
from sklearn.model_selection import train_test_split as tts
from ensembled_svm import EnsembledSVM as eSVM
from imblearn.over_sampling import SMOTE

sys.path.append('../../utility')
import util
import yamanishi_data_util as yam
import classifier_util as cutil

from devel_config import config as cfg

def main():
    if len(sys.argv)!=4:
        print 'USAGE:'
        print 'python -m scoop devel.py [cloneID] [clusterDir] [outputDir]'
        print 'see devel_config.py'
        return

    cloneID = sys.argv[1]
    clusterDir = sys.argv[2]; assert clusterDir[-1]=='/',"should be ended with '/'"
    baseOutDir = sys.argv[3]

    if not(os.path.isdir(baseOutDir)):
        os.makedirs(baseOutDir)

    method = cfg['method']['name']
    if method not in ['esvm','psvm']:
        print 'FATAL: unknown method'
        return
    print 'method: '+method

    # outDir = os.path.join(baseOutDir,'-'.join([method+'#'+cloneID,dataset,util.tag()]))
    # os.makedirs(outDir);

    ## Load data ###################################################################################
    dataLog = {}; dataLogFpath = os.path.join(baseOutDir,'data_log.json')
    dataset = clusterDir.split('/')[-2].split('-')[-1]; dataLog['dataset'] = dataset
    datasetParams = dataset.split('#')

    xyDevFpath = os.path.join(baseOutDir,'_'.join(['xdevf','ydev']+datasetParams)+'.h5')
    if os.path.exists(xyDevFpath):
        print 'loading data from previous...'
        with h5py.File(xyDevFpath,'r') as f:
            xdevf = f['xdevf'][:]
            ydev = f['ydev'][:]
        with open(dataLogFpath,'r') as f:
            dataLog = yaml.load(f)
    else:
        print 'loading data freshly...'
        if datasetParams[0]=='yamanishi':
            nUnlabels = []
            statFnames = [i for i in os.listdir(clusterDir) if 'labels_stat.json' in i]
            for i in statFnames:
                with open(os.path.join(clusterDir,i),'r') as f: stat = yaml.load(f)
                nUnlabels.append(stat['0'])
            metric = '_'.join(statFnames[ nUnlabels.index(min(nUnlabels)) ].split('_')[0:2])
            dataLog['metric'] = metric

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

        ##
        print 'loading com, pro feature...'
        krFpath = os.path.join(cfg['datasetDir'],datasetParams[0],'feature',
                               'klekotaroth','klekotaroth-'+datasetParams[1]+'.h5')
        aacFpath = os.path.join(cfg['datasetDir'],datasetParams[0],'feature',
                                'amino-acid-composition','amino-acid-composition-'+datasetParams[1]+'.h5')

        comList = list( set([i[0] for i in xdev]) )
        proList = list( set([i[1] for i in xdev]) )

        krDict = {}; aacDict = {}
        with h5py.File(krFpath, 'r') as f:
            for com in comList: krDict[com] = f[com][:]
        with h5py.File(aacFpath, 'r') as f:
            for pro in proList: aacDict[pro] = f[pro][:]

        ##
        print 'extract (com,pro) feature...'
        sh.setConst(krDict=krDict)
        sh.setConst(aacDict=aacDict)
        xdevf = list( fu.map(cutil.extractComProFea,xdev) )

        ##
        print 'writing...'
        shutil.copy2('devel_config.py',baseOutDir)

        with h5py.File(xyDevFpath,'w') as f:
            f.create_dataset('xdevf',data=xdevf,dtype=np.float32)
            f.create_dataset('ydev',data=ydev,dtype=np.int8)

        dataLog['nDevel'] = len(devIdx); dataLog['nData'] = len(yraw)
        dataLog['rDevel:Data'] = dataLog['nDevel']/float(dataLog['nData'])
        dataLog['nDevel(+)'] = len( [i for i in ydev if i==1] ); assert dataLog['nDevel(+)']!=0
        dataLog['nDevel(-)'] = len( [i for i in ydev if i==-1] ); assert dataLog['nDevel(-)']!=0
        dataLog['rDevel(+):Devel'] = float(dataLog['nDevel(+)'])/dataLog['nDevel']
        dataLog['rDevel(-):Devel'] = float(dataLog['nDevel(-)'])/dataLog['nDevel']
        dataLog['rDevel(+):(-)'] = float(dataLog['nDevel(+)'])/float(dataLog['nDevel(-)'])
        with open(dataLogFpath,'w') as f: json.dump(dataLog,f,indent=2,sort_keys=True)

    ##
    xyDevResFpath = os.path.join(baseOutDir,'_'.join(['xdevf','ydev','resampled']+datasetParams)+'.h5')
    if (os.path.exists(xyDevResFpath)):
        print ('ensembled smote from previous...')
        with h5py.File(xyDevResFpath,'r') as f:
            xdevfr = f['xdevfr'][:]
            ydevr = f['ydevr'][:]
        with open(dataLogFpath,'r') as f:
            dataLog = yaml.load(f)
    else:
        print ('ensembled smote freshly...')
        xyDevList = cutil.divideSamples(xdevf,ydev,cfg['smoteBatchSize'])
        smoteSeed = util.seed(); dataLog['smoteSeed'] = smoteSeed

        xdevfr = []; ydevr = []
        for xdevfi,ydevi in xyDevList:
            sm = SMOTE(kind='svm',random_state=smoteSeed)
            xdevfri,ydevri = sm.fit_sample(xdevfi,ydevi)
            for x in xdevfri: xdevfr.append(x.tolist())
            for y in ydevri: ydevr.append(y)
        assert len(xdevfr)==len(ydevr),'len(xdevfr)!=len(ydevr)'

        ##
        with h5py.File(xyDevResFpath,'w') as f:
            f.create_dataset('xdevfr',data=xdevfr,dtype=np.float32)
            f.create_dataset('ydevr',data=ydevr,dtype=np.int8)

        dataLog['nDevelResampled'] = len(ydevr)
        dataLog['rDevelResampled:Data'] = dataLog['nDevelResampled']/float(dataLog['nData'])
        dataLog['nDevelResampled(+)'] = len( [i for i in ydevr if i==1] )
        dataLog['nDevelResampled(-)'] = len( [i for i in ydevr if i==-1] )
        dataLog['rDevelResampled(+):DevelResampled'] = dataLog['nDevelResampled(+)']/float(dataLog['nDevelResampled'])
        dataLog['rDevelResampled(-):DevelResampled'] = dataLog['nDevelResampled(-)']/float(dataLog['nDevelResampled'])
        dataLog['rDevelResampled(+):(-)'] = dataLog['nDevelResampled(+)']/float(dataLog['nDevelResampled(-)'])
        with open(dataLogFpath,'w') as f: json.dump(dataLog,f,indent=2,sort_keys=True)

    return

    # ##
    # xdev = xdevfr
    # ydev = ydevr

    # ## TUNE+TRAIN+TEST #############################################################################
    # msg = 'devel '+dataset+' '+cloneID
    # xtr,xte,ytr,yte = tts(xdev,ydev,test_size=cfg['testSize'],
    #                       random_state=seed,stratify=ydev)

    # if cfg['maxTestingSamples']>0:
    #     chosenIdx = np.random.randint(len(xte),size=cfg['maxTestingSamples'])
    #     xte = [xte[i] for i in chosenIdx]; yte = [yte[i] for i in chosenIdx]

    # log['nTraining'] = len(xtr)
    # log['nTraining(+)'] = len([i for i in ytr if i==1])
    # log['nTraining(-)'] = len([i for i in ytr if i==-1])
    # log['rTraining(+):(-)'] = log['nTraining(+)']/float(log['nTraining(-)'])
    # log['rTraining:Devel'] = log['nTraining']/float(log['nDevel'])
    # log['nTesting'] = len(xte)
    # log['nTesting(+)'] = len([i for i in yte if i==1])
    # log['nTesting(-)'] = len([i for i in yte if i==-1])
    # log['rTesting(+):(-)'] = log['nTesting(+)']/float(log['nTesting(-)'])
    # log['rTesting:Devel'] = log['nTesting']/float(log['nDevel'])

    # ## tuning
    # clf = None
    # if method=='esvm':
    #     clf  = eSVM(cfg['method']['mode'],
    #                 cfg['method']['maxTrainingSamplesPerBatch'],
    #                 cfg['method']['maxTestingSamplesPerBatch'],
    #                 cfg['method']['bootstrap'],
    #                 {'com':comSimDict,'pro':proSimDict})
    # elif method=='psvm':
    #     # clf = svm.SVC(kernel='precomputed',probability=True)
    #     clf = svm.SVC(probability=True)

    # ## training
    # print msg+': fitting nTr= '+str(len(ytr))
    # if method=='esvm':
    #     clf.fit(xtr,ytr)
    #     clf.writeLabels(outDir)
    #     log['nSVM'] = clf.nSVM()
    # elif method=='psvm':
    #     # simMatTr = cutil.makeKernel(xtr,xtr,{'com':comSimDict,'pro':proSimDict})
    #     # clf.fit(simMatTr,ytr)
    #     clf.fit(xtr,ytr)
    #     log['labels'] = clf.classes_.tolist()

    # ## testing
    # print msg+': predicting nTe= '+str(len(yte))
    # if method=='esvm':
    #     ypred,yscore = clf.predict(xte)
    # elif method=='psvm':
    #     # simMatTe = cutil.makeKernel(xte,xtr,{'com':comSimDict,'pro':proSimDict})
    #     # ypred = clf.predict(simMatTe)
    #     # yscore = clf.predict_proba(simMatTe)
    #     ypred = clf.predict(xte)
    #     yscore = clf.predict_proba(xte)
    #     yscore = [max(i.tolist()) for i in yscore]

    # result = {'xtr':xtr,'xte':xte,'ytr':ytr,'yte':yte,'ypred':ypred,'yscore':yscore}
    # with open(os.path.join(outDir,"result.pkl"),'w') as f: pickle.dump(result,f)
    # with open(os.path.join(outDir,'log.json'),'w') as f: json.dump(log,f,indent=2,sort_keys=True)

if __name__ == '__main__':
    tic = time.time()
    main()
    print "main took: "+str(time.time()-tic)+' seconds'
