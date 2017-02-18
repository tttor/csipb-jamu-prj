# rndly.py
import numpy as np

class RNDLy:
    def __init__(self):
    	self.name = 'rndly'

    def predict(self,query):
    	com,pro = query.split(":")
    	timestamp = '000'

        lo = 0.0
        hi = 1.0
        pred = np.random.uniform(lo,hi,1)[0]

        predMsgList = [com,pro,str(pred),self.name,timestamp]
        predMsg = '|'.join(predMsgList)

        return predMsg
