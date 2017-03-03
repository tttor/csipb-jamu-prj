# kronrls.py
import numpy as np

from numpy import linalg as LA
from scipy import sparse
from collections import defaultdict

class KronRLS:
    # these vars hold _all_ available training data
    _trComList = None
    _trProList = None
    _trConnMat = None
    _kernelDict = None

    def __init__(self,iTrConnMat=None,iTrComList=None,iTrProList=None,iKernelDict=None):
        self._trConnMat = iTrConnMat
        self._trComList = iTrComList
        self._trProList = iTrProList
        self._kernelDict = iKernelDict

    def predict(self,xTest,gamma,threshold):
        ## train
        model = self._train(xTest)
        connMat,comKernelMat,proKernelMat,xIdxTest = model

        ## make prediction
        connMatPred = self._predict(comKernelMat,proKernelMat,connMat,gamma)

        ##
        yPred = []
        for cIdx,pIdx in xIdxTest:
            y = connMatPred[cIdx][pIdx]
            y = int(y>=threshold)
            yPred.append(y)

        return yPred

    def _train(self,xTest):
        '''
        in kronRLS, the (learned) model refers to the connMat and  the kernel
        '''
        ## take a subset of training data
        # now: all
        comList = self._trComList
        proList = self._trProList
        connMat = self._trConnMat

        ## clear any element of conn mat that is in testing
        xIdxTest = []
        for c,p in xTest:
            cIdx = -1
            if c in comList:
                cIdx = comList.index(c)
            else:
                assert False,'new compound'

            pIdx = -1
            if p in proList:
                pIdx = proList.index(p)
            else:
                assert False,'new protein'

            if cIdx!=-1 and pIdx!=-1:
                connMat[cIdx][pIdx] = 0 # yes, setting to zero for test samples
                xIdxTest.append( (cIdx,pIdx) )

        ##
        comKernelMat = self._makeKernelMat(comList,comList)
        proKernelMat = self._makeKernelMat(proList,proList)

        ##
        model = (connMat,comKernelMat,proKernelMat,xIdxTest)

        return model

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
