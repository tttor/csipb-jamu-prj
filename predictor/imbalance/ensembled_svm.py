# ensembled_svm.py
import os
import pickle
import json
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import KFold
from sklearn import svm
from scoop import futures as fu

class EnsembledSVM:
    def __init__(self,imaxTrSamples,imaxTeSamples,ibootstrap,isimDict):
        self._maxTrainingSamples = imaxTrSamples
        self._maxTestingSamples = imaxTeSamples
        self._boostrap = ibootstrap
        self._simDict = isimDict
        self._svmList = []
        self._labels = []

    def writeSVM(self,outDir):
        fpath = os.path.join(outDir,'esvm.pkl')
        with open(fpath,'w') as f: pickle.dump(self._svmList,f)

    def writeLabels(self,outDir):
        assert len(self._labels)!=0
        fpath = os.path.join(outDir,'esvm_labels.json')
        with open(fpath,'w') as f: json.dump(self._labels,f)

    def nSVM(self):
        return len(self._svmList)

    def fit(self,ixtr,iytr):
        xyTrList = self._divideSamples(ixtr,iytr,self._maxTrainingSamples)
        self._svmList = list( fu.map(self._fit2,
                                     [xytr[0] for xytr in xyTrList],
                                     [xytr[1] for xytr in xyTrList]) )
        assert len(self._svmList)!=0,'empty _svmList in fit()'

        self._labels = self._svmList[0][0].classes_.tolist()
        for svm in self._svmList: assert svm[0].classes_.tolist()==self._labels

    def predict(self,ixte,mode):
        assert len(self._svmList)!=0,'empty _svmList in predict()'
        xyTeList = self._divideSamples(ixte,None,self._maxTestingSamples)
        xTeList = [i[0] for i in xyTeList]; n = len(xTeList)
        ypredList = list( fu.map(self._predict2,
                                 xTeList,[mode]*n,[self._svmList]*n,[self._labels]*n) )

        ypredMerged = []; yscoreMerged = [];
        for i in ypredList:
            ypredMerged += [j[0] for j in i]
            yscoreMerged += [j[1] for j in i]
        assert len(ypredMerged)==len(ixte),str(len(ypredMerged))+'!='+str(len(ixte))
        return (ypredMerged,yscoreMerged)

    def _predict2(self,xte,mode,svmList,labels):
        ypred2 = list( fu.map(self._predict3,
                              svmList,[xte]*len(svmList)) )

        ypred3 = [] # ypred merged from all classifiers
        for i in range(len(xte)):# for each member/sample of the vector xte
            ypred3i = [ypred2[j][i] for j in range(len(svmList))]# of each sample from all classifiers
            ypred3i = self._merge(ypred3i,mode,labels)
            ypred3.append(ypred3i)

        return ypred3

    def _predict3(self,iclf,xte):
        clf,xtr = iclf
        simMatTe = self._makeKernel(xte,xtr)

        ypred2iRaw = clf.predict(simMatTe) # remember: ypred2i is a vector
        ypredproba2iRaw = clf.predict_proba(simMatTe)
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

    def _fit2(self,xtr,ytr):
        ## tuning
        clf = svm.SVC(kernel='precomputed',probability=True)

        ## train
        simMatTr = self._makeKernel(xtr,xtr)
        clf.fit(simMatTr,ytr)

        return (clf,xtr)

    def _divideSamples(self,x,y,maxSamples):
        nSplits = int(len(x)/maxSamples) + 1
        if nSplits==1:# take all
            idxesList = [range(len(x))]
        else:# abusely use StratifiedKFold, taking only the testIdx
            if y is None:
                cv = KFold(n_splits=nSplits)
                idxesList = [testIdx for  _, testIdx in cv.split(x) ]
            else:
                cv = StratifiedKFold(n_splits=nSplits,shuffle=True)
                idxesList = [testIdx for  _, testIdx in cv.split(x,y) ]

        ##
        xyList = []
        for idxes in idxesList:
            xList = [x[i] for i in idxes]
            if y is None:
                xyList.append( (xList,None))
            else:
                yList = [y[i] for i in idxes]
                xyList.append( (xList,yList) )

        return xyList

    def _makeKernel(self,xtr1,xtr2):
        mat = np.zeros( (len(xtr1),len(xtr2)) )
        for i in range(mat.shape[0]):
            for j in range(mat.shape[1]):
                mat[i][j] = self._getCompoundProteinSim(xtr1[i],xtr2[j])

        return mat

    def _getCompoundProteinSim(self,i,j):
        comSim = self._getCompoundSim(i[0],j[0])
        proSim = self._getProteinSim(i[1],j[1])

        alpha = 0.5
        sim = alpha*comSim + (1.0-alpha)*proSim

        return sim

    def _getCompoundSim(self,i,j):
        return self._simDict['com'][(i,j)]

    def _getProteinSim(self,i,j):
        return self._simDict['pro'][(i,j)]
