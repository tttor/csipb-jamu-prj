# classifier_util.py
import os
import numpy as np
from scoop import futures as fu
from scoop import shared as sh
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import KFold

def divideSamples(x,y,maxSamplesPerBatch):
   nSplits = ( len(x)/maxSamplesPerBatch ) + 1
   if nSplits==1:# take all
      idxesList = [ range(len(x)) ]
   else:# abusely use StratifiedKFold, taking only the testIdx
      if y is None:
         cv = KFold(n_splits=nSplits)
         idxesList = [testIdx for  _, testIdx in cv.split(x) ]
      else:
         cv = StratifiedKFold(n_splits=nSplits,shuffle=True)
         idxesList = [testIdx for  _, testIdx in cv.split(x,y) ]

   ##
   xyList = []
   for idxes in idxesList:
      xList = [x[i] for i in idxes]
      if y is None: yList = None
      else: yList = [y[i] for i in idxes]
      xyList.append( (xList,yList) )

   return xyList

def makeComProKernelMatFromSimMat(x1,x2,simMat):
   comSimMat = simMat['com']
   proSimMat = simMat['pro']
   mat = np.zeros( (len(x1),len(x2)) )
   for i,ii in enumerate(x1):
      for j,jj in enumerate(x2):
         icom,ipro = [int(k) for k in ii]
         jcom,jpro = [int(k) for k in jj]
         comSim = comSimMat[icom][jcom]
         proSim = simMat['pro'][ipro][jpro]
         mat[i][j] = mergeComProKernel( comSim,proSim )
   return mat

def mergeComProKernel(comSim,proSim,alpha = 0.5):
   sim = alpha*comSim + (1.0-alpha)*proSim
   return sim

def extractComProFea(compro):
   com,pro = compro
   comFea = sh.getConst('krDict')[com]
   proFea = sh.getConst('aacDict')[pro]
   fea = np.append(comFea,proFea)
   fea = fea.tolist()
   return fea
