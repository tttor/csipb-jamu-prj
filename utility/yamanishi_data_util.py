# util.py
import os
import numpy as np
import h5py

def saveFeaInHDF(yamType,feaName):
   bdir = '../dataset/connectivity/compound_vs_protein/yamanishi/feature'
   tdir = os.path.join(bdir,feaName,feaName+'-'+yamType)
   fnameList = os.listdir(tdir)
   feaList = []; iList = []
   for i,fname in enumerate(fnameList):
      print 'loading '+fname+' => '+str(i+1)+'/'+str(len(fnameList))
      fpath = os.path.join(tdir,fname)
      fea = np.loadtxt(fpath,delimiter=",")
      feaList.append(fea)
      iList.append( fname.split('.')[0] )

   print 'writing...'
   ofpath = os.path.join(bdir,feaName,feaName+'-'+yamType+'.h5')
   with h5py.File(ofpath,'w') as f:
      for i,fea in enumerate(feaList):
         key = iList[i]
         f.create_dataset(key,data=fea,dtype=np.float32)

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
    comKernel = loadKernel2('compound',mode,dpath)
    proKernel = loadKernel2('protein',mode,dpath)

    kernel = comKernel
    kernel.update(proKernel)

    return kernel

def loadKernel2(compro,mode,dpath):
    fname = None
    if compro=='compound':
        fname = 'compound/simmat_dc_'+mode+'.txt'
    elif compro=='protein':
        fname = 'protein/simmat_dg_'+mode+'.txt'
    else:
        assert False

    gotHeader = False
    kernel = dict(); colNames = []; rowNames = []; rowValues = []
    with open(os.path.join(dpath,fname),'r') as f:
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
            kernel[(r,c)] = float(rowValues[i][j])

    return kernel

def main():
   # saveFeaInHDF('nr','klekotaroth')
   # saveFeaInHDF('ic','klekotaroth')
   # saveFeaInHDF('nr','amino-acid-composition')
   # saveFeaInHDF('ic','amino-acid-composition')
   pass

if __name__ == '__main__':
   main()
