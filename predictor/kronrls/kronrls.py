# kronrls.py
import numpy as np

from numpy import linalg as LA
from scipy import sparse
from collections import defaultdict

class KronRLS:
    '''
    in kronRLS, the (learned) model is the kernel
    '''
    _trConnMat = None
    _trComList = None
    _trProList = None
    _trComKernelMat = None
    _trProKernelMat = None

    _kernelDict = None

    def __init__(self,iTrConnMat,iTrComList,iTrProList,iKernelDict):
        self._trConnMat = iTrConnMat
        self._trComList = iTrComList
        self._trProList = iTrProList
        self._kernelDict = iKernelDict

        self._trComKernelMat = self._makeKernelMat(self._trComList,self._trComList)
        self._trProKernelMat = self._makeKernelMat(self._trProList,self._trProList)

    def predict(self,xTest,gamma):
        ##
        connMat = self._trConnMat
        xIdxTest = []
        for c,p in xTest:
            cIdx = self._trComList.index(c)
            pIdx = self._trProList.index(p)
            connMat[cIdx][pIdx] = 0
            xIdxTest.append((cIdx,pIdx))

        ##
        comKernelMat = self._trComKernelMat
        proKernelMat = self._trProKernelMat

        ## make prediction
        connMatPred = self._predict(comKernelMat,proKernelMat,connMat,gamma)

        ##
        yPred = []
        for cIdx,pIdx in xIdxTest:
            y = connMatPred[cIdx][pIdx]
            y = int(y>=0.5)
            yPred.append(y)

        return yPred

    def _predict(self,k1,k2,y,gamma=1.0):
        la,Qa = LA.eig(k1)
        lb,Qb = LA.eig(k2)

        la = la.flatten()
        lb = lb.flatten()
        la = np.diag(la)
        lb = np.diag(lb)

        # http://stackoverflow.com/questions/17035767/kronecker-product-in-python-and-matlab
        diagLa = np.diag(la)
        diagLa = diagLa.reshape((len(diagLa),1))
        diagLbTrans = np.diag(lb).transpose()
        diagLbTrans = diagLbTrans.reshape((1,len(diagLbTrans)))

        l = sparse.kron( diagLbTrans,diagLa ).toarray()
        inverse = l / (l+gamma)

        m1 = Qa.transpose().dot(y).dot(Qb)
        m2 = m1 * inverse

        ypred = Qa.dot(m2).dot( Qb.transpose() )
        ypred = ypred.real

        return ypred

    def _makeKernelMat(self,list1,list2):
        m = len(list1)
        n = len(list2)
        kernel = np.zeros((m,n))

        for i,ii in enumerate(list1):
            for j,jj in enumerate(list2):
                kernel[i][j] = self._computeKernel(ii,jj)

        return kernel

    def _computeKernel(self,di,dj):
        kernel = self._kernelDict[(di,dj)]
        return kernel
