# rndly.py
import numpy as np

class RNDLy:
    def __init__(self):
    	self.name = 'rndly'

    def predict(self,query):
        lo = 0.0
        hi = 1.0
        pred = np.random.uniform(lo,hi,1)[0]
        return pred
