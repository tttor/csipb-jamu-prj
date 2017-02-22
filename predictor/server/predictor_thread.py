# predictor_machine_thread.py
import threading
import time
import sys

sys.path.append('../rndly')
from rndly import RNDLy
sys.path.append('../blmnii')
from blm_ajm import BLMNII

class PredictorThread(threading.Thread):
    def __init__ (self,iid,iname,imethod,imaxtime):
        threading.Thread.__init__(self)
        self.id = iid
        self.name = iname
        self.method = imethod
        self.maxTime = imaxtime

        self.predictionList = []
        self.queryList = []
        self.predictionNumber = -1

        self.predictor = None
        if self.method=='rndly':
            self.predictor = RNDLy()
            self.batchLength = 1 #Move this to conflict..?
        elif self.method=='blmnii':
            self.predictor = BLMNII()
            self.batchLength = 2
        else:
            assert False, 'FATAL: Unknown prediction method!'

    def run(self):
        print self.name+': started'
        while True:
            if len(self.queryList)==0:
                continue

            startTime = time.time()
            nQuery = len(self.queryList)
            elapsedTime = 0
            del self.predictionList[:]

            queryBatch = [self.queryList[i:i+self.batchLength]
                          for i in range(0,nQuery,self.batchLength)]
            for i,query in enumerate(queryBatch):
                elapsedTime += time.time()-startTime
                prediction = [-1.0]*self.batchLength # invalid prediction result
                if  elapsedTime <= self.maxTime:
                    print (self.name+': predicting query= '+
                           str(i+len(query))+' of '+str(nQuery))
                    prediction = self.predictor.predict(query)
                self.predictionList += prediction
            self.predictionNumber += 1

            del self.queryList[:]

    def getPredictionList(self):
        return self.predictionList[:]

    def setQueryList(self,iqueryList):
        self.queryList = iqueryList[:]
    def getPredictionNumber(self):
        return self.predictionNumber
