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

def _loadKlekotaroth(keggComID):
   dpath = sh.getConst('comFeaDir')
   fea = np.loadtxt(os.path.join(dpath,keggComID+'.fpkr'), delimiter=",")
   return fea

def _loadAAC(keggProID):
   dpath = sh.getConst('proFeaDir')
   fea = np.loadtxt(os.path.join(dpath,keggProID+'.aac'), delimiter=",")
   return fea

def _mergeComProFea(comFea,proFea):
   fea = np.append(comFea,proFea)
   fea = fea.tolist()
   return fea

def loadFeature(x,comFeaDir,proFeaDir):
   comList = [i[0] for i in x]
   proList = [i[1] for i in x]
   sh.setConst(comFeaDir=comFeaDir)
   sh.setConst(proFeaDir=proFeaDir)

   print 'comFeaList...'
   comFeaList = list( fu.map(_loadKlekotaroth,comList) )

   print 'proFeaList...'
   proFeaList = list( fu.map(_loadAAC,proList) )

   print 'merge...'
   comFeaDict = dict( zip(comList,comFeaList) )
   proFeaDict = dict( zip(proList,proFeaList) )
   xf = [_mergeComProFea(comFeaDict[com],proFeaDict[pro]) for com,pro in x ]

   return xf

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
