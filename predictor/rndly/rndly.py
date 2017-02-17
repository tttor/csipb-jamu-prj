# rndly.py
import numpy as np

class RNDLy:
    def __init__():
        pass

    def predict(queryList):
        lo = 0.0
        hi = 1.0
        n = len(queryList)

        predictionList = np.random.uniform(lo,hi,n)
        predictionList = predictionList.tolist()

        return predictionList
