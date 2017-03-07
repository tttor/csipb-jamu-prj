# rndly.py
import numpy as np
import time

class RNDLy:
    def __init__(self):
        self.name = 'rndly'

    def predict(self,queryList):
        lo = 0.0
        hi = 1.0
        n = len(queryList)

        preds = np.random.uniform(lo,hi,n)
        preds = preds.tolist()

        time.sleep(0.5)
        return preds

    def close(self):
        pass

