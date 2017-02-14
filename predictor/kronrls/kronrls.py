# kronrls.py
import numpy as np
import util

from numpy import linalg as LA
from scipy import sparse
from collections import defaultdict

import yamanishi_data_util as yam

class KronRLS:
    '''
    in kronRLS, the (learned) model is the kernel
    _trConnData contain com-pro connectivity for training
    '''
    _trConnData = None
    _trConnMat = None
    _trComKernel = None
    _trProKernal = None

    _yamanishiKernelDict = None

    def __init__(self,iTrConnData):
        _yamanishiKernelDict = yam.loadKernel()

        # _trConnData = iTrConnData
        # _trConnMat, _trComList, _trProList = _makeConnMat(_trConnData)
        # _trComKernel = _makeComKernel(_trComList)
        # _trProKernel = _makeProKernel()

    def predict(com,pro,gamma):
        # make com-pro conn matrix (adjacency matrix)

        # make kernel dim1: com

        # make kernel dim2: pro

        # make prediction
        ypred = _predict(comKernel,proKernel,connMat,gamma)

    def _predict(self,k1,k2,y,gamma=1.0):
        w1,v1 = LA.eig(k1)
        w2,v2 = LA.eig(k2)

        # http://stackoverflow.com/questions/17035767/kronecker-product-in-python-and-matlab
        v = sparse.kron( np.diag(v2).transpose(),np.diag(v1) ).toarray()
        inv = v / (v+gamma)

        m1 = w1.transpose() * y * w2
        m2 = m1 * inv

        ypred = w1.dot(m2).dot( w2.transpose() )
        return ypred

    def _makeConnMat(connData):
        comProDict = defaultdict(list)
        comList = []
        proList = []
        for d in connData:
            com,pro = d
            conProDict[com].append(pro)
            comList.append(com)
            proList.append(pro)

        comList = list(set(comList))
        proList = list(set(proList))
        connMat = np.zeros( (len(comList),len(proList)) )

        for com,proList in comProDict.iteritems():
            comIdx = comList.index(com)
            for pro in proList:
                proIdx = proList.index(pro)
                connMat[comIdx][proIdx] = 1

        return (connMat, comList, proList)

    def _makeComKernel(comList):
        n = len(comList)
        kernel = mat.np.zeros((n,n))

        for i,ci in enumerate(comList):
            for j,cj in comList:
                kernel[i][j] = _computeComKernel(ci,cj)

    def _computeComKernel(com1,com2):
        kernel = _yamanishiKernelDict[(com1,com2)]
        return kernel
