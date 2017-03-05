# util.py
import os
import numpy as np

def loadComProConn(mode,dPath):
    print 'loading yamanishi connectivity...'
    fpath = os.path.join(dpath,'bind_orfhsa_drug_'+mode+'.txt')

    data = []
    with open(fpath,'r') as f:
        for line in f:
            words = [i.strip() for i in line.split()]
            assert len(words)==2

            pro = words[0].replace(':','')
            com = words[1]
            data.append((com,pro))

    return data

def loadComProConnMat(mode,dpath):
    print 'loading yamanishi conn matrix...'
    fpath = os.path.join(dpath,'admat_dgc_'+mode+'.txt')

    comList = []
    proList = []
    connList = []
    gotHeader = False
    with open(fpath,'r') as f:
        for line in f:
            if not(gotHeader):
                comList = [i.strip() for i in line.split()]
                gotHeader = True
            else:
                words = [i.strip() for i in line.split()]
                proList.append(words[0])
                connList.append(words[1:])

    nCom = len(comList)
    nPro = len(proList)
    mat = np.zeros((nCom,nPro))
    for i,ii in enumerate(comList):
        for j,jj in enumerate(proList):
            mat[i][j] = connList[j][i]

    return (mat,comList,proList)

def loadKernel(mode,dpath):
    print 'loading yamanishi kernel...'
    fnames = ['compound/simmat_dc_'+mode+'.txt','protein/simmat_dg_'+mode+'.txt']

    kernel = dict()
    for fname in fnames:
        fpath = os.path.join(dpath,fname)
        gotHeader = False

        colNames = []
        rowNames = []
        rowValues = []
        with open(fpath,'r') as f:
            for line in f:
                if not(gotHeader):
                    colNames = [i.strip() for i in line.split()]
                    gotHeader = True
                else:
                    row = [i.strip() for i in line.split()]
                    rowNames.append(row[0])
                    rowValues.append(row[1:])

        for i,r in enumerate(rowNames):
            for j,c in enumerate(colNames):
                kernel[(r,c)] = rowValues[i][j]
    return kernel
