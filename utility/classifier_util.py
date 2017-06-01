# classifier_util.py
import numpy as np

def makeKernel(xtr1,xtr2,simDict):
   mat = np.zeros( (len(xtr1),len(xtr2)) )
   for i,ii in enumerate(xtr1):
      for j,jj in enumerate(xtr2):
         comSim = simDict['com'][ (ii[0],jj[0]) ]
         proSim = simDict['pro'][ (ii[1],jj[1]) ]
         mat[i][j] = mergeComProKernel( comSim,proSim )
   return mat

def mergeComProKernel(comSim,proSim,alpha = 0.5):
   sim = alpha*comSim + (1.0-alpha)*proSim
   return sim
