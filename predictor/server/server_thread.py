# predictor_server_thread.py
import threading
import socket
import sys

from predictor_thread import PredictorThread as Predictor
from config import predictorConfig as pcfg

class ServerThread(threading.Thread):
    def __init__(self,iid,iname,ihost,iport):
        threading.Thread.__init__(self)
        self.id = iid
        self.name = iname
        self.host = ihost
        self.port = iport
        self.queryNum = -1

    def run(self):
        connFromLB = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connFromLB.bind( (self.host,self.port) )
        connFromLB.listen(1)

        predictorThreads = []
        for i,mw in enumerate(pcfg['methods']):
            m = mw[0]
            name = self.name+'_'+m
            predictorThreads.append( Predictor(i,name,m,pcfg['maxElapsedTime']) )

        for t in predictorThreads:
            t.daemon = True
            t.start()

        while True:
            print >>sys.stderr,self.name+": Waiting for any query from LoadBalancer at "+self.host+":"+str(self.port)
            connToLB, connToLBAddr = connFromLB.accept()

            try:
                # print >>sys.stderr, self.name+': Connection from', connToLBAddr
                dataTemp = ""
                message = ""
                while True:
                    dataTemp = connToLB.recv(1024)
                    # print >>sys.stderr, self.name+': Received "%s"' % dataTemp
                    message += dataTemp
                    if message[-3:]=="end":
                        message = message.split("|")[0]
                        connToLB.close()
                        break
            finally:
                self.queryNum += 1
                queryList = message.split(",")
                for t in predictorThreads:
                    t.setQueryList(queryList)

                # Wait for all thread to finish
                while True:
                    finished = True
                    for i,t in enumerate(predictorThreads):
                        if t.getPredictionNumber()!=self.queryNum:
                            finished = False
                            break

                    if finished:
                        break

                # Merge predictionMsg
                predictionListRaw = [] # 2D: row: method and col: ith query
                for t in predictorThreads:
                    predictionListRaw.append( t.getPredictionList() )

                predictionList = []
                for i in range(len(queryList)):
                    nMethods = len(pcfg['methods'])
                    normalizer = 1.0/float(nMethods)
                    nPred = 0.0
                    for j in range(nMethods):
                        w = pcfg['methods'][j][1]
                        nPred += normalizer * w * predictionListRaw[j][i]
                    predictionList.append(nPred)
                # print self.name+': predictionList '+str(predictionList)

                # Push predMsg to DB
                # connDB = psycopg2.connect(database=db['name'],user=db['user'],password=db['passwd'],
                #                           host=db['host'],port=db['port'])
                # self.cur = connDB.cursor()
