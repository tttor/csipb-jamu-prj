# classifier_util.py
import numpy as np

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
