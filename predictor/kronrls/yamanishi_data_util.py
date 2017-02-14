# util.py
import os

def loadComProConn(mode):
    print 'loading yamanishi connectivity...'
    dpath = '../../dataset/connectivity/compound_vs_protein/yamanishi/ground-truth'
    fpath = os.path.join(dpath,mode)

    data = []
    with open(fpath,'r') as f:
        for line in f:
            words = [i.strip() for i in line.split()]
            assert len(words)==2

            pro = words[0]
            com = words[1]
            data.append((com,pro))

    return data

def loadKernel():
    print 'loading yamanishi kernel...'
    dpath = '../../dataset/connectivity/compound_vs_protein/yamanishi/similarity-mat'
    fnames = ['compound/simmat_dc_e.txt','compound/simmat_dc_gpcr.txt',
             'compound/simmat_dc_ic.txt','compound/simmat_dc_nr.txt']

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
                kernel[(r,c)] = rowValues[j]

    return kernel
