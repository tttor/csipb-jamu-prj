'''
BLM Framework by Yamanishi and Beakley
'''

import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from sklearn.cross_validation import KFold
from sklearn.cross_validation import StratifiedKFold
from sklearn import svm
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import average_precision_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score

class BLM:
    dataX = []; dataY = []; nData = 0
    proteinSimMat = None; proteinSimMatMeta = None
    drugSimMat = None; drugSimMatMeta = None

    def __init__(self, fpath, drugSimMatFpath, proteinSimMatFpath):
        self._loadBinding(fpath)
        self._loadSimMat(drugSimMatFpath, proteinSimMatFpath)

    def eval(self, outDir):
        # kfList = KFold(self.nData, n_folds=self.nData) #equivalent to the Leave One Out strategy
        # kfList = KFold(self.nData, n_folds=10, shuffle=True) 
        kfList = StratifiedKFold(self.dataY, n_folds=10, shuffle=True)

        for idx, kf in enumerate(kfList):
            trIdxList, testIdxList = kf

            xTest = [self.dataX[i] for i in testIdxList]
            yTest = [self.dataY[i] for i in testIdxList]

            xTr = [self.dataX[i] for i in trIdxList]
            yTr = [self.dataY[i] for i in trIdxList]

            #
            yPredOfProteinSet = self._predict('usingProteinSet', xTest, xTr, yTr)
            yPredOfDrugSet = self._predict('usingDrugSet', xTest, xTr, yTr)
            assert(len(yPredOfDrugSet)==len(yPredOfProteinSet))

            #
            yPred = []
            for i in range(len(yPredOfDrugSet)):
                yPred.append( max(yPredOfDrugSet[i],yPredOfProteinSet[i]) )

            #
            self._computePrecisionRecall(yTest, yPred, outDir+'/pr_curve_fold_'+str(idx+1)+'.png')
            self._computeROC(yTest, yPred, outDir+'/roc_curve_fold_'+str(idx+1)+'.png')
            # accuracy = accuracy_score(yTest, yPred)
            # precision = precision_score(yTest, yPred)
            # recall = recall_score(yTest, yPred)
            
            break

    def _predict(self, type, xTest, xTr, yTr):
        # get _local_ (w.r.t. testData) training data
        xTrLocal = []
        yTrLocal = []

        simMat = None
        simMatMeta = None
        
        refIdx = None
        if type=='usingDrugSet':
            refIdx = 1 # ref is protein in xTest
            simMat = self.drugSimMat
            simMatMeta = self.drugSimMatMeta
        elif type=='usingProteinSet':
            refIdx = 0 # ref is drug in xTest
            simMat = self.proteinSimMat
            simMatMeta = self.proteinSimMatMeta
        else:
            assert(False)

        refList = [d[refIdx] for d in xTest] 
        for idx,d in enumerate(xTr):
            if (d[refIdx] in refList):
                xTrLocal.append(d)
                yTrLocal.append( yTr[idx] )

        # Use only either drug or protein of X
        xTrLocal = [i[int(not refIdx)] for i in xTrLocal]
        xTestLocal = [i[int(not refIdx)] for i in xTest]

        #
        gramTr = self._makeGram(xTrLocal, xTrLocal, simMat, simMatMeta)
        gramTest = self._makeGram(xTestLocal,xTrLocal, simMat, simMatMeta)

        #
        clf = svm.SVC(kernel='precomputed')
        clf.fit(gramTr,yTrLocal)

        yPred = clf.predict(gramTest)
        return yPred

    def _loadBinding(self, fpath):
        content = []
        with open(fpath) as f:
            content = f.readlines()

        drugList = []
        proteinList = []
        drugProteinDict = defaultdict(list)
        for c in content:
            tmp = [i.strip() for i in c.split()]
            
            proteinList.append(tmp[0])
            drugList.append(tmp[1])

            drugProteinDict[tmp[1]].append( tmp[0] )

        drugList = list(set(drugList))
        proteinList = list(set(proteinList))
        assert(len(drugList)==len(drugProteinDict))

        self.dataX = [(i,j) for i in drugList for j in proteinList]
        for x in self.dataX:
            targetProteinList = drugProteinDict[ x[0] ]
            self.dataY.append(int( x[1] in targetProteinList ))

        assert(len(self.dataX)==len(self.dataY))
        self.nData = len(self.dataX)

    def _loadSimMat(self, drugSimMatFpath, proteinSimMatFpath):
        self.proteinSimMatMeta, self.proteinSimMat = self._readSimMat(proteinSimMatFpath)
        self.drugSimMatMeta, self.drugSimMat = self._readSimMat(drugSimMatFpath)
        
    def _readSimMat(self, fpath):
        with open(fpath) as f:
            content = f.readlines()

        simMatMeta = []
        simMat = None
        for idx,c in enumerate(content):
            if idx==0:
                simMatMeta = [i.strip() for i in c.split()]
                n = len(simMatMeta)
                simMat = np.zeros((n,n),dtype=float)
            else:
                valStr = [i.strip() for i in c.split()]
                assert(valStr[0]==simMatMeta[idx-1])
                del valStr[0]
                i = idx - 1
                for j,v in enumerate(valStr):
                    simMat[i][j] = float(v)

        return (simMatMeta, simMat)

    def _makeGram(self, X1, X2, simMat, meta):
        shape = (len(X1),len(X2))
        gram = np.zeros(shape)

        for i, x1 in enumerate(X1):
            for j, x2 in enumerate(X2):
                x1 = x1.replace(':','')
                x2 = x2.replace(':','')
                
                ii = meta.index(x1)
                jj = meta.index(x2)
                
                gram[i][j] = simMat[ii][jj]

        return gram

    def _computePrecisionRecall(self, yTrue, yPred, curveFpath):
        precision, recall, thresholds = precision_recall_curve(yTrue, yPred)
        averagePrecision = average_precision_score(yTrue, yPred, average='micro')

        plt.clf()
        plt.plot(recall, precision, label='Precision-Recall curve')
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.ylim([0.0, 1.05])
        plt.xlim([0.0, 1.0])
        plt.title('Precision-Recall example: AUC={0:0.2f}'.format(averagePrecision))
        plt.legend(loc="lower left")
        plt.savefig(curveFpath, bbox_inches='tight')

    def _computeROC(self, yTrue, yPred, curveFpath):
        fpr, tpr, _ = roc_curve(yTrue, yPred)
        roc_auc = auc(fpr, tpr)

        plt.figure()
        plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
        plt.plot([0, 1], [0, 1], 'k--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver operating characteristic example')
        plt.legend(loc="lower right")
        plt.savefig(curveFpath, bbox_inches='tight')


