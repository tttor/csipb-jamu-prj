# classifier_util.py
import os
import numpy as np

def loadFeature(x,comFeaDir,proFeaDir):
   xf = []
   for com,pro in x:
      comFea = loadKlekotaroth(com,comFeaDir).tolist()
      proFea = loadAAC(pro,proFeaDir).tolist()
      xf.append( mergeComProFea(comFea,proFea) )
   return xf

def mergeComProFea(comFea,proFea):
   return comFea+proFea

def loadKlekotaroth(keggComID,dpath):
   fea = np.loadtxt(os.path.join(dpath,keggComID+'.fpkr'), delimiter=",")
   return fea

def loadAAC(keggProID,dpath):
   fea = np.loadtxt(os.path.join(dpath,keggProID+'.aac'), delimiter=",")
   return fea

def makeKernel(x1,x2,simDict):
   mat = np.zeros( (len(x1),len(x2)) )
   for i,ii in enumerate(x1):
      for j,jj in enumerate(x2):
         comSim = simDict['com'][ (ii[0],jj[0]) ]
         proSim = simDict['pro'][ (ii[1],jj[1]) ]
         mat[i][j] = mergeComProKernel( comSim,proSim )
   return mat

def mergeComProKernel(comSim,proSim,alpha = 0.5):
   sim = alpha*comSim + (1.0-alpha)*proSim
   return sim
