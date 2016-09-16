'''
BLM Framework by Yamanishi and Beakley
'''

import numpy as np
from collections import defaultdict
from sklearn.cross_validation import KFold
from sklearn import svm

class BLM:
    dataX = []
    dataY = []
    nData = 0
    proteinKernel = None
    proteinKernelMeta = None
    drugKernel = None
    drugKernelMeta = None

    def __init__(self, fpath, drugKernelFpath, proteinKernelFpath):
        self._loadBinding(fpath)
        self._loadKernel(drugKernelFpath, proteinKernelFpath)

    def eval(self):
        # kf = KFold(self.nData, n_folds=self.nData) #equivalent to the Leave One Out strategy
        kf = KFold(self.nData, n_folds=10) 

        for trIdxList, testIdxList in kf:
            DtestX = [self.dataX[i] for i in testIdxList]
            DtestY = [self.dataY[i] for i in testIdxList]

            DtrX = [self.dataX[i] for i in trIdxList]
            DtrY = [self.dataY[i] for i in trIdxList]

            DtrProteinX,DtrProteinY = self._makeDtrOfProtein(DtestX,DtrX,DtrY)

            print( len(DtrProteinX) )
            print( len(DtrProteinY) )
            # clfOfProtein = svm.SVC(kernel='precomputed') 
            # clfOfProtein.fit(gramTr,DtrProteinY)

            # DpredProteinY = clfOfProtein.predict(gramTest)
            break

    def _makeDtrOfProtein(self, DtestX, DtrX, DtrY):
        DtrProteinX = []
        DtrProteinY = []
        testDrugList = [d[0] for d in DtestX]

        for idx,d in enumerate(DtrX):
            if (d[0] in testDrugList):
                DtrProteinX.append(d)
                DtrProteinY.append( DtrY[idx] )

        return (DtrProteinX, DtrProteinY)

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

        self.dataX = [(i,j) for i in range(len(drugList)) for j in range(len(proteinList))]
        for x in self.dataX:
            targetProteinList = drugProteinDict[ drugList[x[0]] ]
            self.dataY.append(int( proteinList[x[1]] in targetProteinList ))

        assert(len(self.dataX)==len(self.dataY))
        self.nData = len(self.dataX)

    def _loadKernel(self, drugKernelFpath, proteinKernelFpath):
        self.proteinKernelMeta, self.proteinKernel = self._readKernelFile(proteinKernelFpath)
        self.drugKernelMeta, self.drugKernel = self._readKernelFile(drugKernelFpath)
        
    def _readKernelFile(self, fpath):
        with open(fpath) as f:
            content = f.readlines()

        kernelMeta = []
        kernel = None
        for idx,c in enumerate(content):
            if idx==0:
                kernelMeta = [i.strip() for i in c.split()]
                n = len(kernelMeta)
                kernel = np.zeros((n,n),dtype=float)
            else:
                valStr = [i.strip() for i in c.split()]
                assert(valStr[0]==kernelMeta[idx-1])
                del valStr[0]
                i = idx - 1
                for j,v in enumerate(valStr):
                    kernel[i][j] = float(v)

        return (kernelMeta, kernel)

