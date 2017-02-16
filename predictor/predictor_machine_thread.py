# predictor_machine_thread.py
import threading

class PredictorMachineThread(threading.Thread):
    def __init__ (self,threadId,name,queryPair,key):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.name = name
        self.queryPair = queryPair
        self.cur = connDB.cursor()
        self.funcKey = key
    def run(self):
        # Pass db cursor to predict
        nPairs = len(self.queryPair)
        startTime = time.time()
        self.predictionStr = ""
        print >> sys.stderr, "Start Predicting with "+self.name
        for i,query in enumerate(self.queryPair):
            print >> sys.stderr, '*********************************************************'
            print >> sys.stderr, self.name+' predicting pair= '+str(i+1)+' of '+str(nPairs)
            if (i>0):
                self.predictionStr += ","

            elapsedTime = time.time()-startTime
            print >> sys.stderr, self.name+' elapsedTime= '+str(elapsedTime)+' of max= '+str(maxElapsedTime)

            if  elapsedTime <= maxElapsedTime:
                self.predictionStr += funcPointer[self.funcKey](query,self.cur)
            else:
                self.predictionStr += predictDummy(query)
    def join(self):
        threading.Thread.join(self)
        return self.predictionStr
