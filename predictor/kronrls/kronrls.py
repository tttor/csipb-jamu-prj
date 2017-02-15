# kronrls.py
import numpy as np
import util

from numpy import linalg as LA
from scipy import sparse
from collections import defaultdict

class KronRLS:
    '''
    in kronRLS, the (learned) model is the kernel
    _trConnData contain com-pro connectivity for training
    '''
    _trConnData = None
    _trConnMat = None
    _trComKernelMat = None
    _trProKernal = None

    _kernelDict = None

    def __init__(self,iTrConnData,iKernelDict):
        self._trConnData = iTrConnData
        self._kernelDict = iKernelDict

        self._trConnMat, self._trComList, self._trProList = self._makeConnMat(self._trConnData)
        self._trComKernelMat = self._makeKernelMat(self._trComList,self._trComList)
        self._trProKernelMat = self._makeKernelMat(self._trProList,self._trProList)

    def predict(self,com,pro,gamma):
        # make a new conn matrix with the given com,pro
        comNew = not(com in self._trComList)
        proNew = not(pro in self._trProList)

        connMat = self._trConnMat
        comKernelMat = self._trComKernelMat
        proKernelMat = self._trProKernelMat
        nRows,nCols = connMat.shape

        comIdx = -1
        proIdx = -1
        if not(comNew) and not(proNew):
            print 'not(comNew) and not(proNew)'
            assert False
            comIdx = self._trComList.index(com)
            proIdx = self._trProList.index(pro)
            connMat[comIdx][proIdx] = 0 # clear any given conn if any

            comIdx = self._trComList.index(com)
            proIdx = self._trComList.index(pro)
        elif comNew and not(proNew):
            print 'comNew and not(proNew)'
            assert False
            newRow = np.zeros((1,nCols))
            connMat = np.vstack((connMat,newRow))
        elif not(comNew) and proNew:
            print 'not(comNew) and proNew'
            newCol = np.zeros((nRows,1))
            connMat = np.hstack((connMat,newCol))

            proNewKernelRow = self._makeKernelMat([pro],self._trProList)
            proNewKernelCol = proNewKernelRow.transpose()
            proNewKernelCol = np.vstack( (proNewKernelCol,np.ones(1)) )

            proKernelMat = np.vstack((proKernelMat,proNewKernelRow))
            proKernelMat = np.hstack((proKernelMat,proNewKernelCol))

            comIdx = self._trComList.index(com)
            proIdx = connMat.shape[1]-1
        elif comNew and proNew:
            print 'comNew and proNew'
            assert False
            newRow = np.zeros((1,nCols))
            newCol = np.zeros((nRows+1,1))
            connMat = np.vstack((connMat,newRow))
            connMat = np.hstack((connMat,newCol))
        else:
            assert False

        # make prediction
        print 'comKernelMat.shape=',comKernelMat.shape
        print 'proKernelMat.shape=',proKernelMat.shape
        print 'connMat.shape=',connMat.shape
        connMatPred = self._predict(comKernelMat,proKernelMat,connMat,gamma)

        ypred = connMatPred[comIdx][proIdx]
        ypred = int(ypred>=0.5)
        return ypred

    def _predict(self,k1,k2,y,gamma=1.0):
        la,Qa = LA.eig(k1)
        lb,Qb = LA.eig(k2)

        la = la.flatten()
        lb = lb.flatten()
        la = np.diag(la)
        lb = np.diag(lb)

        print 'Qa.shape=',Qa.shape
        print 'Qb.shape=',Qb.shape
        print 'la.shape=',la.shape
        print 'lb.shape=',lb.shape

        # http://stackoverflow.com/questions/17035767/kronecker-product-in-python-and-matlab
        diagLa = np.diag(la)
        diagLa = diagLa.reshape((len(diagLa),1))
        diagLbTrans = np.diag(lb).transpose()
        diagLbTrans = diagLbTrans.reshape((1,len(diagLbTrans)))

        l = sparse.kron( diagLbTrans,diagLa ).toarray()
        print 'diagLa.shape= ',diagLa.shape
        print 'diagLbTrans.shape= ',diagLbTrans.shape
        print 'l.shape= ',l.shape

        inverse = l / (l+gamma)
        print 'inverse.shape=',inverse.shape

        m1 = Qa.transpose().dot(y).dot(Qb)
        m2 = m1 * inverse
        print 'm1.shape= ',m1.shape
        print 'm2.shape= ',m2.shape

        # print y.shape
        # print Qa.shape
        # print Qb.shape
        # print m2.shape

        ypred = Qa.dot(m2).dot( Qb.transpose() )
        ypred = ypred.real
        print 'ypred.shape=',ypred.shape
        return ypred

    def _makeConnMat(self,connData):
        comProDict = defaultdict(list)
        comList = []
        proList = []
        for d in connData:
            com,pro = d
            comProDict[com].append(pro)
            comList.append(com)
            proList.append(pro)

        comList = list(set(comList))
        proList = list(set(proList))
        connMat = np.zeros( (len(comList),len(proList)) )

        for com,pros in comProDict.iteritems():
            comIdx = comList.index(com)
            for pro in pros:
                proIdx = proList.index(pro)
                connMat[comIdx][proIdx] = 1

        return (connMat, comList, proList)

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
