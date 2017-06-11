# ensembled_svm.py
import os
import sys
import pickle
import json
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import KFold
from sklearn.decomposition import PCA, KernelPCA
from sklearn import svm
from scoop import futures as fu

sys.path.append('../../utility')
import classifier_util as cutil

from esvm_config import config as cfg

class EnsembledSVM:
    def __init__(self,simMat):
        self._kernel = cfg['kernel']
        self._mode = cfg['mode']
        self._boostrap = cfg['bootstrap']
        self._maxTrainingSamplesPerBatch = cfg['maxTrainingSamplesPerBatch']
        self._maxTestingSamplesPerBatch = cfg['maxTestingSamplesPerBatch']
        self._maxNumberOfTrainingBatches = cfg['maxNumberOfTrainingBatches']
        self._simMat = simMat
        self._svmList = []
        self._labels = []

    def writeSVM(self,outDir):
        fpath = os.path.join(outDir,'esvm.pkl')
        with open(fpath,'w') as f: pickle.dump(self._svmList,f)

    def labels(self):
        assert len(self._labels)!=0
        return self._labels

    def nSVM(self):
        return len(self._svmList)

    def xtrDimAllBatches(self):
        dims = []
        for _,xtr,_ in self._svmList:
            dims.append( np.asarray(xtr).shape )
        return dims

    ## Fit #########################################################################################
    def fit(self,ixtr,iytr):
        xyTrList = cutil.divideSamples(ixtr,iytr,self._maxTrainingSamplesPerBatch)
        if self._maxNumberOfTrainingBatches != 0:
            xyTrList = xyTrList[0:self._maxNumberOfTrainingBatches]

        self._svmList = list( fu.map(self._fit,
                                     [xytr[0] for xytr in xyTrList],
                                     [xytr[1] for xytr in xyTrList]) )
        assert len(self._svmList)!=0,'empty _svmList in fit()'

        self._labels = self._svmList[0][0].classes_.tolist()
        for svm in self._svmList: assert svm[0].classes_.tolist()==self._labels

    def _fit(self,xtr,ytr):
        ## dimred
        if cfg['dimred']=='pca':
            dimred = PCA(n_components=cfg['dimredNComponents'],svd_solver=cfg['dimredSolver'])
        elif cfg['dimred']=='kpca':
            dimred = KernelPCA(n_components=cfg['dimredNComponents'],kernel=cfg['kernel'],n_jobs=-1)
        elif clf['dimred'=='none']:
            dimred = None
        else:
            assert False,'FATAL: unknown dimred'

        if dimred is not None:
            dimred.fit(xtr)
            xtr = dimred.transform(np.asarray(xtr))

        ## tuning
        clf = svm.SVC(kernel=self._kernel,probability=True)

        ## train
        if self._kernel=='precomputed':
            assert self._simMat is not None
            simMatTr = cutil.makeComProKernelMatFromSimMat(xtr,xtr,self._simMat)
            clf.fit(simMatTr,ytr)
        else:
            clf.fit(xtr,ytr)

        return (clf,xtr,dimred)

    ## Predict #####################################################################################
    def predict(self,ixte):
        assert len(self._svmList)!=0,'empty _svmList in predict()'
        xyTeList = cutil.divideSamples(ixte,None,self._maxTestingSamplesPerBatch)
        xTeList = [i[0] for i in xyTeList]; n = len(xTeList)
        ypredList = list( fu.map(self._predict,
                                 xTeList,[self._mode]*n,[self._svmList]*n,[self._labels]*n) )

        ypredMerged = []; yscoreMerged = [];
        for i in ypredList:
            ypredMerged += [j[0] for j in i]
            yscoreMerged += [j[1] for j in i]
        assert len(ypredMerged)==len(ixte),str(len(ypredMerged))+'!='+str(len(ixte))
        return (ypredMerged,yscoreMerged)

    def _predict(self,xte,mode,svmList,labels):
        ypred2 = list( fu.map(self._predict2,
                              svmList,[xte]*len(svmList)) )

        ypred3 = [] # ypred merged from all classifiers
        for i in range(len(xte)):# for each member/sample of the vector xte
            ypred3i = [ypred2[j][i] for j in range(len(svmList))]# of each sample from all classifiers
            ypred3i = self._merge(ypred3i,mode,labels)
            ypred3.append(ypred3i)

        return ypred3

    def _predict2(self,iclf,xte):
        clf,xtr,dimred = iclf
        xte = dimred.transform(np.asarray(xte))

        if self._kernel=='precomputed':
            assert self._simMat is not None
            simMatTe = cutil.makeComProKernelMatFromSimMat(xte,xtr,self._simMat)
            ypred2iRaw = clf.predict(simMatTe) # remember: ypred2i is a vector
            ypredproba2iRaw = clf.predict_proba(simMatTe)
        else:
            ypred2iRaw = clf.predict(xte) # remember: ypred2i is a vector
            ypredproba2iRaw = clf.predict_proba(xte)

        ypred2i = zip(ypred2iRaw,ypredproba2iRaw)
        return ypred2i

    def _merge(self,yListRaw,mode,labels):
        y = None; yscore = None
        yList,yprobaList = zip(*yListRaw)

        if mode=='hard':
            counters = [0]*len(labels)
            for i in yList: counters[ labels.index(i) ] += 1
            assert sum(counters)==len(yList),'sum(counters)!=len(yList)'
            y = labels[ counters.index(max(counters)) ]
            yscore = max(counters)/float(sum(counters))
        elif mode=='soft':
            avgProbaList = [] # from all labels, averaged over all classifiers
            for i in range(len(labels)): avgProbaList.append(np.mean([ j[i] for j in yprobaList ]))
            yscore = max(avgProbaList)
            y = labels[ avgProbaList.index(yscore) ]
        else:
            assert False,'FATAL: unkown mode'

        return (y,yscore)
