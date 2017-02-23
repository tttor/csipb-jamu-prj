# rndly.py
import numpy as np

class RNDLy:
    def __init__(self):
    	self.name = 'rndly'

    def predict(self,queryList):
    	lo = 0.0
        hi = 1.0
    	n = len(queryList)

        preds = np.random.uniform(lo,hi,n)
        preds = preds.tolist()

        return preds
