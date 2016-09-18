'''
BLM Framework by Yamanishi and Beakley
'''

import numpy as np
from collections import defaultdict
from sklearn.cross_validation import KFold
from sklearn.cross_validation import StratifiedKFold
from sklearn import svm

class BLM:
    dataX = []
    dataY = []
    nData = 0
    proteinSimMat = None
    proteinSimMatMeta = None
    drugSimMat = None
    drugSimMatMeta = None

    def __init__(self, fpath, drugSimMatFpath, proteinSimMatFpath):
        self._loadBinding(fpath)
        self._loadSimMat(drugSimMatFpath, proteinSimMatFpath)

    def eval(self):
        # kf = KFold(self.nData, n_folds=self.nData) #equivalent to the Leave One Out strategy
        # kf = KFold(self.nData, n_folds=10, shuffle=True) 
        kf = StratifiedKFold(self.dataY, n_folds=10, shuffle=True)

        for trIdxList, testIdxList in kf:
            DtestX = [self.dataX[i] for i in testIdxList]
            DtestY = [self.dataY[i] for i in testIdxList]

            DtrX = [self.dataX[i] for i in trIdxList]
            DtrY = [self.dataY[i] for i in trIdxList]

            #
            DtrOfProteinSetX,DtrOfProteinSetY = self._makeDtrOfProteinSet(DtestX,DtrX,DtrY)
            DtrOfProteinSetX = [i[1] for i in DtrOfProteinSetX]
            DtestX = [i[1] for i in DtestX]
            
            #
            gramTr = self._makeGram(DtrOfProteinSetX, DtrOfProteinSetX, self.proteinSimMat, self.proteinSimMatMeta)
            gramTest = self._makeGram(DtestX,DtrOfProteinSetX, self.proteinSimMat, self.proteinSimMatMeta)

            clfOfProtein = svm.SVC(kernel='precomputed')
            clfOfProtein.fit(gramTr,DtrOfProteinSetY)
            
            DpredProteinY = clfOfProtein.predict(gramTest)

    def _makeDtrOfProteinSet(self, DtestX, DtrX, DtrY):
        DtrOfProteinSetX = []
        DtrOfProteinSetY = []

        testDrugList = [d[0] for d in DtestX]
        testDrugList = list(set(testDrugList))

        # enforce local training data
        for idx,d in enumerate(DtrX):
            if (d[0] in testDrugList):
                DtrOfProteinSetX.append(d)
                DtrOfProteinSetY.append( DtrY[idx] )

        return (DtrOfProteinSetX, DtrOfProteinSetY)

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
                
                gram[i][j] = self.proteinSimMat[ii][jj]

        return gram
