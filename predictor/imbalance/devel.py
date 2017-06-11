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
from sklearn.metrics.pairwise import rbf_kernel
from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import SelectPercentile
from sklearn.feature_selection import chi2
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
    baseOutDir = sys.argv[3]; assert baseOutDir[-1]!='/',"should NOT be ended with '/'"

    clfParam = None
    method = cfg['method']
    if method=='esvm':
        from esvm_config import config as clfParam
    elif method=='psvm':
        from psvm_config import config as clfParam
    else:
        print 'FATAL: unknown method'
        return

    outDir = os.path.join(baseOutDir,'devel-'+os.path.basename(baseOutDir))
    if not(os.path.isdir(baseOutDir)): os.makedirs(baseOutDir)
    if not(os.path.isdir(outDir)): os.makedirs(outDir)

    ## Load data ###################################################################################
    dataLog = {}; dataLogFpath = os.path.join(outDir,'data_log_'+os.path.basename(baseOutDir)+'.json')
    dataset = clusterDir.split('/')[-2].split('-')[-1]; dataLog['dataset'] = dataset
    datasetParams = dataset.split('#')
    assert datasetParams[0]=='yamanishi'

    xyDevFpath = os.path.join(baseOutDir,'_'.join(['xdev','ydev','xrel','yrel']+datasetParams)+'.h5')
    if os.path.exists(xyDevFpath):
        print 'loading data from PREVIOUS...'

        with h5py.File(xyDevFpath,'r') as f:
            xdev = f['xdev'][:]
            ydev = f['ydev'][:]
            xrel = f['xrel'][:]
            yrel = f['yrel'][:]

        with open(dataLogFpath,'r') as f:
            dataLog = yaml.load(f)

    else:
        print 'loading data FRESHLY...'

        print 'loading cluster result...'
        nUnlabels = []
        statFnames = [i for i in os.listdir(clusterDir) if 'labels_stat.json' in i]
        for i in statFnames:
            with open(os.path.join(clusterDir,i),'r') as f: stat = yaml.load(f)
            nUnlabels.append(stat['0'])

        # use the cluster with minimum numbers of unlabeled samples
        metric = '_'.join(statFnames[ nUnlabels.index(min(nUnlabels)) ].split('_')[0:2])
        dataLog['metric'] = metric

        connFpath = os.path.join(clusterDir,metric+'_labels.pkl')
        with open(connFpath,'r') as f:
            data = pickle.load(f)

        ##
        print 'getting devel and release data...'
        xraw = []; yraw = []
        for k,v in data.iteritems():
            for vv in v:
                xraw.append(vv)
                yraw.append(k)

        devIdx = [i for i in range(len(xraw)) if yraw[i]!=0]
        xdev = [xraw[i] for i in devIdx]
        ydev = [yraw[i] for i in devIdx]

        relIdx = [i for i in range(len(xraw)) if yraw[i]==0]
        xrel = [xraw[i] for i in relIdx]
        yrel = [yraw[i] for i in relIdx]

        dataLog['nDevel'] = len(devIdx); dataLog['nData'] = len(yraw)
        dataLog['rDevel:Data'] = dataLog['nDevel']/float(dataLog['nData'])
        dataLog['nDevel(+)'] = len( [i for i in ydev if i==1] ); assert dataLog['nDevel(+)']!=0
        dataLog['nDevel(-)'] = len( [i for i in ydev if i==-1] ); assert dataLog['nDevel(-)']!=0
        dataLog['rDevel(+):Devel'] = float(dataLog['nDevel(+)'])/dataLog['nDevel']
        dataLog['rDevel(-):Devel'] = float(dataLog['nDevel(-)'])/dataLog['nDevel']
        dataLog['rDevel(+):(-)'] = float(dataLog['nDevel(+)'])/float(dataLog['nDevel(-)'])
        dataLog['nRelease'] = len(relIdx);
        dataLog['rRelease:Data'] = dataLog['nRelease']/float(dataLog['nData'])

        ##
        print 'loading com, pro feature...'
        krFpath = os.path.join(cfg['datasetDir'],datasetParams[0],'feature',
                               'klekotaroth','klekotaroth-'+datasetParams[1]+'.h5')
        aacFpath = os.path.join(cfg['datasetDir'],datasetParams[0],'feature',
                                'amino-acid-composition','amino-acid-composition-'+datasetParams[1]+'.h5')

        krDict = {}; aacDict = {}
        with h5py.File(krFpath, 'r') as f:
            for com in [str(i) for i in f.keys()]:
                krDict[com] = f[com][:]
        with h5py.File(aacFpath, 'r') as f:
            for pro in [str(i) for i in f.keys()]:
                aacDict[pro] = f[pro][:]
                # aacDict[pro] = list( fu.map(lambda x: float('%.2f'%(x)),f[pro][:]) ) # rounding

        comFeaLenOri = len(krDict.values()[0])
        proFeaLenOri = len(aacDict.values()[0])

        ##
        msg = 'extract (com,pro) feature... dims: '+str(comFeaLenOri)+','+str(proFeaLenOri)
        msg += ' of '+str(len(ydev))+' and '+str(len(yrel))
        print msg

        sh.setConst(krDict=krDict)
        sh.setConst(aacDict=aacDict)
        xdevf = list( fu.map(cutil.extractComProFea,xdev) )
        xrelf = list( fu.map(cutil.extractComProFea,xrel) )

        ##
        xyDevList = cutil.divideSamples(xdevf,ydev,cfg['smoteBatchSize'])
        if cfg['maxNumberOfSmoteBatch'] != 0:
            xyDevList = xyDevList[0:cfg['maxNumberOfSmoteBatch']]

        smoteSeed = util.seed(); dataLog['smoteSeed'] = smoteSeed
        sh.setConst(smoteSeed=smoteSeed)

        print 'resampling via Smote FRESHLY... '+str(len(xyDevList))+' smote(s)'+' on '+str(len(ydev))
        smoteTic = time.time()

        xdevfr = []; ydevr = []
        xydevfrList = list( fu.map(ensembleSmote,xyDevList) )
        for xdevfri,ydevri in xydevfrList:
            for x in xdevfri: xdevfr.append(x.tolist())
            for y in ydevri: ydevr.append(y)
        assert len(xdevfr)==len(ydevr),'len(xdevfr)!=len(ydevr)'

        dataLog['nSmote'] = len(xyDevList)
        dataLog['nDevelResampled'] = len(ydevr)
        dataLog['rDevelResampled:Data'] = dataLog['nDevelResampled']/float(dataLog['nData'])
        dataLog['nDevelResampled(+)'] = len( [i for i in ydevr if i==1] )
        dataLog['nDevelResampled(-)'] = len( [i for i in ydevr if i==-1] )
        dataLog['rDevelResampled(+):DevelResampled'] = dataLog['nDevelResampled(+)']/float(dataLog['nDevelResampled'])
        dataLog['rDevelResampled(-):DevelResampled'] = dataLog['nDevelResampled(-)']/float(dataLog['nDevelResampled'])
        dataLog['rDevelResampled(+):(-)'] = dataLog['nDevelResampled(+)']/float(dataLog['nDevelResampled(-)'])
        dataLog['timeSMOTE'] =  str(time.time()-smoteTic)

        ##
        print 'update xdev,ydev,xrel... '+str(np.asarray(xdevfr).shape)
        xrel = xrelf[:]
        xdev = xdevfr[:]
        ydev = ydevr[:]

        print 'writing updated xdev,ydev and xrel,yrel...'
        with h5py.File(xyDevFpath,'w') as f:
            f.create_dataset('xdev',data=xdev,dtype=np.float32)
            f.create_dataset('ydev',data=ydev,dtype=np.int8)
            f.create_dataset('xrel',data=xrel,dtype=np.float32)
            f.create_dataset('yrel',data=yrel,dtype=np.int8)

        print 'writing dataLog...'
        dataLog['nCom'] = len(krDict)
        dataLog['nPro'] = len(aacDict)
        with open(dataLogFpath,'w') as f:
            json.dump(dataLog,f,indent=2,sort_keys=True)

    ## TUNE+TRAIN+TEST #############################################################################
    devLog = {}
    devSeed = util.seed(); dataLog['devSeed'] = devSeed
    tag = '_'.join([method+'#'+cloneID,dataset,util.tag()])

    ## split devel dataset
    msg = ' '.join( ['devel',dataset,cloneID])
    xtr,xte,ytr,yte = tts(xdev,ydev,test_size=cfg['testSize'],
                          random_state=devSeed,stratify=ydev)

    if cfg['maxTestingSamples']>0:
        chosenIdx = np.random.randint(len(xte),size=cfg['maxTestingSamples'])
        xte = [xte[i] for i in chosenIdx]; yte = [yte[i] for i in chosenIdx]

    devLog['nTraining'] = len(xtr)
    devLog['nTraining(+)'] = len([i for i in ytr if i==1])
    devLog['nTraining(-)'] = len([i for i in ytr if i==-1])
    devLog['rTraining(+):(-)'] = devLog['nTraining(+)']/float(devLog['nTraining(-)'])
    devLog['rTraining:Devel'] = devLog['nTraining']/float(dataLog['nDevelResampled'])
    devLog['nTesting'] = len(xte)
    devLog['nTesting(+)'] = len([i for i in yte if i==1])
    devLog['nTesting(-)'] = len([i for i in yte if i==-1])
    devLog['rTesting(+):(-)'] = devLog['nTesting(+)']/float(devLog['nTesting(-)'])
    devLog['rTesting:Devel'] = devLog['nTesting']/float(dataLog['nDevelResampled'])

    ## tuning
    clf = None
    if method=='esvm':
        clf  = eSVM(simMat=None)
    elif method=='psvm':
        clf = svm.SVC(kernel=clfParam['kernel'],probability=True)

    ## training
    print msg+': fitting nTr= '+str(len(ytr))
    trTic = time.time()

    if method=='esvm':
        clf.fit(xtr,ytr)
        devLog['labels'] = clf.labels()
        devLog['nSVM'] = clf.nSVM()
        devLog['xtrDimAllBatches'] = clf.xtrDimAllBatches()
    elif method=='psvm':
        if cfg['method']['kernel']=='precomputed':
            assert False
            # simMatTr = cutil.makeComProKernelMatFromSimMat(xtr,xtr,simMat)
            # clf.fit(simMatTr,ytr)
        else:
            clf.fit(xtr,ytr)
        devLog['labels'] = clf.classes_.tolist()
    devLog['timeTraining'] = str(time.time()-trTic)

    ## testing
    print msg+': predicting nTe= '+str(len(yte))
    teTic = time.time()

    if method=='esvm':
        ypred,yscore = clf.predict(xte)
    elif method=='psvm':
        if cfg['method']['kernel']=='precomputed':
            assert False
            # simMatTe = cutil.makeComProKernelMatFromSimMat(xte,xtr,simMat)
            # ypred = clf.predict(simMatTe)
            # yscore = clf.predict_proba(simMatTe)
        else:
            ypred = clf.predict(xte)
            yscore = clf.predict_proba(xte)
            yscore = [max(i.tolist()) for i in yscore]
    devLog['timeTesting'] = str(time.time()-teTic)

    ## TEST RELEASE ################################################################################
    print msg+': predicting RELEASE n= '+str(len(yrel))
    relTic = time.time()

    if method=='esvm':
        yrel,yrelscore = clf.predict(xrel)
    elif method=='psvm':
        if cfg['method']['kernel']=='precomputed':
            assert False
            # simMatTe = cutil.makeComProKernelMatFromSimMat(xrel,xtr,simMat)
            # yrel = clf.predict(simMatTe)
            # yrelscore = clf.predict_proba(simMatTe)
        else:
            yrel = clf.predict(xrel)
            yrelscore = clf.predict_proba(xrel)
            yrelscore = [max(i.tolist()) for i in yrelscore]
    devLog['timeRelease'] = str(time.time()-relTic)

    ## WRITE RESULT ################################################################################
    result = {'yte':yte,'ypred':ypred,'yscore':yscore,'yrel':yrel,'yrelscore':yrelscore}

    print 'writing prediction...'
    with h5py.File(os.path.join(outDir,'result_'+tag+'.h5'),'w') as f:
        for k,v in result.iteritems():
            dt = np.int8
            if 'score' in k: dt = np.float32
            f.create_dataset(k,data=v,dtype=dt)

    ##
    print 'writing devLog...'
    devLog['clfParam'] = clfParam
    devLog['devParam'] = cfg
    with open(os.path.join(outDir,'devLog_'+tag+'.json'),'w') as f:
        json.dump(devLog,f,indent=2,sort_keys=True)

def ensembleSmote(xydev):
    xdevf,ydev = xydev
    sm = SMOTE(kind='svm',random_state=sh.getConst('smoteSeed'))
    xdevfr,ydevr = sm.fit_sample(xdevf,ydev)
    return (xdevfr,ydevr)

if __name__ == '__main__':
    tic = time.time()
    main()
    print "main took: "+str(time.time()-tic)+' seconds'
