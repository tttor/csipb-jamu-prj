# predictor_machine_thread.py
import threading
import time
import sys

sys.path.append('../rndly')
from rndly import RNDLy
sys.path.append('../blmnii')
from blm_ajm import BLMNII
sys.path.append('../kronrls')
from kronrls import KronRLS

class PredictorThread(threading.Thread):
    def __init__ (self,iid,iname,imethod,imaxtime,ibatchlen):
        threading.Thread.__init__(self)
        self.id = iid
        self.name = iname
        self.method = imethod
        self.maxTime = imaxtime

        self.predictionList = []
        self.queryList = []
        self.predictionNumber = -1
        self.batchLength = ibatchlen

        self.predictor = None
        if self.method=='rndly':
            self.predictor = RNDLy()
        elif self.method=='blmnii':
            self.predictor = BLMNII()
        elif self.method=='kronrls':
            self.predictor = KronRLS()
        else:
            assert False, 'FATAL: Unknown prediction method!'

    def run(self):
        print self.name+': started'

        while True:
            nQuery = len(self.queryList)
            if nQuery==0:
                continue

            ##
            startTime = time.time()
            elapsedTime = 0.0
            del self.predictionList[:]

            ##
            queryBatch = [self.queryList[i:i+self.batchLength]
                          for i in range(0,nQuery,self.batchLength)]

            ##
            for i,queries in enumerate(queryBatch):
                elapsedTime += time.time()-startTime
                predictions = [float('NaN')]*self.batchLength # invalid prediction result

                if  elapsedTime <= self.maxTime:
                    predictions = self.predictor.predict(queries)

                self.predictionList += predictions

            ##
            self.predictionNumber += 1
            del self.queryList[:]

    def getPredictionList(self):
        return self.predictionList[:]

    def setQueryList(self,iqueryList):
        self.queryList = iqueryList[:]
    def getPredictionNumber(self):
        return self.predictionNumber
