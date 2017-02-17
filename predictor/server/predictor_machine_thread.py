# predictor_machine_thread.py
import threading
import time
import psycopg2
import sys

sys.path.append('../rndly')
from rndly import RNDLy

class PredictorMachineThread(threading.Thread):
    def __init__ (self,iid,iname,iqueryList,imethod,imaxtime):
        threading.Thread.__init__(self)
        self.id = iid
        self.name = iname
        self.queryList = iqueryList
        self.method = method
        self.maxTime = imaxtime

        connDB = psycopg2.connect(database=db['name'],user=db['user'],password=db['passwd'],
                                  host=db['host'],port=db['port'])
        self.cur = connDB.cursor()

        self.predictor = None
        if self.method=='rndly':
            predictor = RNDLy()
        # elif self.method=='blmnii':
        #     predictor = BLMNII()
        else:
            pass

    def run(self):
        nQuery = len(self.queryList)
        startTime = time.time()
        self.predictionStr = ""
        for i,query in enumerate(self.queryList):
            print >> sys.stderr, self.name+' predicting pair= '+str(i+1)+' of '+str(nQuery)
            if (i>0):
                self.predictionStr += ","

            elapsedTime = time.time()-startTime
            if  elapsedTime <= self.maxTime:
                self.predictionStr += self._predict(query)
            else:
                self.predictionStr += self._predictDummy(query)

    def join(self):
        threading.Thread.join(self)
        return self.predictionStr

    def _predict(self,query):
        # Run prediction
        predictionStr = self.predictor.predict(query)

        # Insert prediction result to DB
        # TODO

        return predictionStr

    def _predictDummy(query):
        comId,proId = query.split(":")
        weight = 0
        source = 'null'
        timestamp = 'null'
        predictionStrList = [comId,proId,str(weight),source,timestamp]
        predictionStr = '|'.join(predictionStrList)
        return predictionStr
