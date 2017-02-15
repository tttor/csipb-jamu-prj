# util.py
import os

def loadComProConn(mode):
    print 'loading yamanishi connectivity...'
    dpath = '../../dataset/connectivity/compound_vs_protein/yamanishi/ground-truth'
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

def loadKernel(mode):
    print 'loading yamanishi kernel...'
    dpath = '../../dataset/connectivity/compound_vs_protein/yamanishi/similarity-mat'
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
