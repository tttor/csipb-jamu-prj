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
    def __init__ (self,iid,iname,imaxtime,ipredictorParams):
        threading.Thread.__init__(self)
        self.id = iid
        self.name = iname
        self.maxTime = imaxtime
        self.predictorParams = ipredictorParams

        self.predictionList = []
        self.queryList = []
        self.predictionNumber = -1

        self.predictor = None
        self.batchSize = ipredictorParams['batchSize']
        predictorMethod = ipredictorParams['name']
        if predictorMethod=='rndly':
            self.predictor = RNDLy()
        elif predictorMethod=='blmnii':
            self.predictor = BLMNII()
        elif predictorMethod=='kronrls':
            self.predictor = KronRLS(ipredictorParams)
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
            queryBatch = [self.queryList[i:i+self.batchSize]
                          for i in range(0,nQuery,self.batchSize)]

            ##
            for i,queries in enumerate(queryBatch):
                elapsedTime += time.time()-startTime

                # init with invalid prediction result, i.e. NaN values
                predictions = [float('NaN')]*self.batchSize

                # check time limit
                if  elapsedTime <= self.maxTime:
                    predictions = self.predictor.predict(queries)

                # merge
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
