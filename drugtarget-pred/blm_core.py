'''
BLM Framework by Yamanishi and Beakley
'''

import numpy as np
import matplotlib.pyplot as plt
import json
from collections import defaultdict
from sklearn.cross_validation import KFold
from sklearn.cross_validation import StratifiedKFold
from sklearn import svm
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import average_precision_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.preprocessing import MinMaxScaler
from scipy import interp
from scoop import futures as fu

class BLM:
    dataX = []; dataY = []; nData = 0
    drugSimMat = None; proteinSimMat = None
    drugList = []; proteinList = []
    adjMat = None

    def __init__(self, fpath, drugSimMatFpath, proteinSimMatFpath):
        self._loadInteraction(fpath)
        self._loadSimMat(drugSimMatFpath, proteinSimMatFpath)

    def eval(self, type, outDir):
        nFolds = None
        kfList = None
        if type=='loocv':
            nFolds = self.nData
            kfList = KFold(self.nData, n_folds=nFolds, shuffle=True) 
        elif type=='kfcv':
            nFolds = 10
            kfList = StratifiedKFold(self.dataY, n_folds=nFolds, shuffle=True)
        else:
            assert(False)

        #
        xTestList = []; yTestList = []
        xTrList = []; yTrList = []
        for trIdxList, testIdxList in kfList:
            xTestList.append( [self.dataX[i] for i in testIdxList] )
            yTestList.append( [self.dataY[i] for i in testIdxList] )

            xTrList.append( [self.dataX[i] for i in trIdxList] )
            yTrList.append( [self.dataY[i] for i in trIdxList] )

        kfResult = fu.map(self._evalPerFold, xTestList, yTestList, xTrList, yTrList,
                          [self.drugList]*nFolds, [self.proteinList]*nFolds)# TODO not to pass these lists?

        # Combine the results from across all folds
        predResults = defaultdict(list)
        for result in kfResult:
            yPredD, yPredP, yTest = result
            yPredD, yPredDNII = yPredD
            yPredP, yPredPNII = yPredP

            for i, y in enumerate(yTest):
                yd = yPredD[i]; ydnii = yPredDNII[i]
                yp = yPredP[i]; ypnii = yPredPNII[i]

                #
                if yd!=None:
                    predResults['usingDrugSet'].append((yd,y))

                if yp!=None:
                    predResults['usingProteinSet'].append((yp,y))

                if yd!=None and yp!=None:
                    predResults['usingDrugAndProteinSet'].append( (max(yd,yp),y) )
                
                #
                ynii = max(yd,yp,ydnii,ypnii); assert ynii!=None
                predResults['usingDrugAndProteinSetNII'].append( (ynii,y) )

        # Compute ROC curve and PR curve
        perf = dict.fromkeys(predResults.keys())
        perf2 = dict.fromkeys(predResults.keys())

        for key, value in predResults.iteritems():
            yPred = [v[0] for v in value]
            yTest = [v[1] for v in value]

            fpr, tpr, _ = roc_curve(yTest, yPred)
            rocAUC = roc_auc_score(yTest, yPred)

            precision, recall, _ = precision_recall_curve(yTest, yPred)
            prAUC = average_precision_score(yTest, yPred, average='micro')

            lineType = None
            if key=='usingDrugSet':
                lineType = 'r-'
            elif key=='usingProteinSet':
                lineType = 'b--'
            elif key=='usingDrugAndProteinSet':
                lineType = 'g:'
            elif key=='usingDrugAndProteinSetNII':
                lineType = 'k-.'

            perf[key] = {'fpr': fpr, 'tpr': tpr, 'rocAUC': rocAUC,
                         'precision': precision, 'recall': recall, 'prAUC': prAUC,
                         'lineType': lineType}
            perf2[key] = {'rocAUC': rocAUC,'prAUC': prAUC, 'nTest': len(yTest)}

        with open(outDir+'/perf.json', 'w') as fp:
            json.dump(perf2, fp, indent=2, sort_keys=True)

        plt.clf()
        plt.figure()
        for key, locPerf in perf.iteritems():
            plt.plot(locPerf['fpr'], locPerf['tpr'], locPerf['lineType'],
                    label=key+' (area = %0.2f)' % locPerf['rocAUC'], lw=2)
        plt.xlim([-0.05, 1.05])
        plt.ylim([-0.05, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver operating characteristic (ROC) Curve')
        plt.legend(loc="lower right")
        plt.savefig(outDir+'/roc_curve.png', bbox_inches='tight')

        plt.clf()
        plt.figure()
        for key, locPerf in perf.iteritems():
            plt.plot(locPerf['recall'], locPerf['precision'], locPerf['lineType'],
                    label= key+' (area = %0.2f)' % locPerf['prAUC'], lw=2)
        plt.ylim([-0.05, 1.05])
        plt.xlim([-0.05, 1.05])
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title('Precision-Recall Curve')
        plt.legend(loc="lower left")
        plt.savefig(outDir+'/pr_curve.png', bbox_inches='tight')

    def _evalPerFold(self, xTest, yTest, xTr, yTr, drugList, proteinList):
        yPredUsingDrugSet = self._predict('usingDrugSetAsTrainingData', xTest, xTr, yTr, 
                                        drugList, proteinList)
        yPredUsingProteinSet = self._predict('usingProteinSetAsTrainingData', xTest, xTr, yTr,
                                           drugList, proteinList)

        assert(len(yPredUsingDrugSet[0])==len(yPredUsingProteinSet[0])==len(yTest))
        return (yPredUsingDrugSet, yPredUsingProteinSet, yTest)

    def _predict(self, type, xTest, xTr, yTr, drugList, proteinList):
        # set based on 2 possible types,i.e
        # a) 'usingDrugSetAsTrainingData':# =local model of a protein
        # b) 'usingProteinSetAsTrainingData':# =local model of a drug
        simMatT = (self.drugSimMat, self.proteinSimMat)
        metaT = (drugList, proteinList)

        refIdx = None # either drug(=0) or protein(=1) of a tuple xTest(drug,protein)
        if type=='usingProteinSetAsTrainingData':# =local model of a drug
            refIdx = 0 
        elif type=='usingDrugSetAsTrainingData':# =local model of a protein
            refIdx = 1 
        else:
            assert False

        # get _local_ training data (w.r.t. xTest)
        xTrLocal = []; yTrLocal = []
        refList = [ dp[refIdx] for dp in xTest ] # of those we build the local model
        refList = list(set(refList)) # to avoid duplicate on (xTrLocal and yTrLocal)
        for idx,dp in enumerate(xTr):# impose locality constraints in the xTr
            if (dp[refIdx] in refList):
                xTrLocal.append(dp)
                yTrLocal.append( yTr[idx] )

        # if a drug or a protein is new, it has _no_ known connection,
        # then, we follow the NII procedure by Mei, 2012
        yTrLocalNII = []
        if (len(set(yTrLocal))==1): # set(yTrLocal) = {0} (unknown interaction)
            for idx, y in enumerate(yTrLocal):
                x = xTrLocal[idx]
                neighbors = [i for i in metaT[refIdx] if i != x[refIdx]]

                ip = 0.0 # interaction profile from all neighbors
                for n in neighbors:
                    idx1 = metaT[refIdx].index(n)
                    idx2 = metaT[refIdx].index( x[refIdx] )
                    simScore = simMatT[refIdx][idx1][idx2]

                    nt = [None]*2 
                    nt[refIdx] = n
                    nt[not(refIdx)] = x[not(refIdx)]

                    drugIdx = drugList.index(nt[0])
                    proteinIdx = proteinList.index(nt[1])
                    interaction = self.adjMat[drugIdx][proteinIdx]

                    ip += (interaction*simScore)
                yTrLocalNII.append(ip)
            
            #normalize such that each element of yTrLocalNII in [0,1]
            assert len(yTrLocalNII)==len(yTrLocal)

            mms = MinMaxScaler((0,1))
            yTrLocalNIIArr = np.asarray(yTrLocalNII)
            yTrLocalNIIArr = yTrLocalNIIArr.reshape(-1,1)
            yTrLocalNIIArr = mms.fit_transform(yTrLocalNIIArr)
            yTrLocalNIIArr = [i[0] for i in yTrLocalNIIArr.tolist()]
            yTrLocalNII = [int(i>=0.5) for i in yTrLocalNIIArr]

        # Make gram mat
        # Use only either drug or protein only from x(drug,protein)
        xTrLocal = [i[int(not(refIdx))] for i in xTrLocal]
        xTestLocal = [i[int(not(refIdx))] for i in xTest]

        gramTr = self._makeGram(xTrLocal, xTrLocal, 
                                simMatT[not(refIdx)], metaT[not(refIdx)])
        gramTest = self._makeGram(xTestLocal,xTrLocal, 
                                  simMatT[not(refIdx)], metaT[not(refIdx)])

        # Predict
        yPred = None; yPredNII = None
        clf = svm.SVC(kernel='precomputed')
        if (len(set(yTrLocal))==2): # as for binary clf where nClass=2
            clf.fit(gramTr,yTrLocal)

            yPred = clf.predict(gramTest)
            yPredNII = [None]*len(xTest)
        else:
            clf.fit(gramTr,yTrLocalNII)

            yPred = [None]*len(xTest)
            yPredNII = clf.predict(gramTest)
            
        return (yPred, yPredNII)

    def _loadInteraction(self, fpath):
        lines = []
        with open(fpath) as f:
            lines = f.readlines()

        self.drugList = [i.strip() for i in lines[0].split()]
        del lines[0]
        
        nDrugs = len(self.drugList); nProteins = len(lines)
        self.adjMat = np.zeros( (nDrugs,nProteins) )
        for i,line in enumerate(lines):
            cols = [c.strip() for c in line.split()]
            
            self.proteinList.append(cols[0])
            del cols[0]

            for j,c in enumerate(cols):
                self.adjMat[j][i] = int(c)

        # Make data
        self.dataX = [(i,j) for i in self.drugList for j in self.proteinList]
        for x in self.dataX:
            i = self.drugList.index(x[0])
            j = self.proteinList.index(x[1])

            self.dataY.append( self.adjMat[i][j])
        
        assert(len(self.dataX)==len(self.dataY))
        self.nData = len(self.dataX)

    def _loadSimMat(self, drugSimMatFpath, proteinSimMatFpath):
        meta, self.proteinSimMat = self._readSimMat(proteinSimMatFpath)
        assert meta==self.proteinList

        meta, self.drugSimMat = self._readSimMat(drugSimMatFpath)
        assert meta==self.drugList
        
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
                assert(gram[i][j] >= 0)

        return gram
