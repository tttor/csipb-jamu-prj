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
        self.predMsg = ""

    def run(self):
        while True:
            connFromLB = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connFromLB.bind( (self.host,self.port) )
            connFromLB.listen(1)

            print >>sys.stderr,self.name+": Waiting for any query at "+self.host+":"+str(self.port)
            connToLB, connToLBAddr = connFromLB.accept()

            try:
                print >>sys.stderr, self.name+': Connection from', connToLBAddr

                dataTemp = ""
                message = ""
                while True:
                    dataTemp = connToLB.recv(1024)
                    print >>sys.stderr, self.name+': Received "%s"' % dataTemp
                    message += dataTemp

                    if message[-3:]=="end":
                        message = message.split("|")[0]
                        connToLB.close()
                        connFromLB.close()
                        break
            finally:
                queryList = message.split(",")
                threadList = [Predictor(i,self.name+'_'+method,
                                        queryList,method,pcfg['maxElapsedTime'])
                              for i,method in enumerate(pcfg['methods'])]

                for t in threadList:
                    t.daemon=True
                    t.start()

                #TODO: a lock for Synchronizing the query string...?
                for t in threadList:
                    self.predMsg += t.join()
                print >> sys.stderr, self.name+': predMsg = '+self.predMsg

                ## Send to predict.php
                connToPredictorPHP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                connToPredictorPHP.connect( (self.host,self.port) )

                connToPredictorPHP.sendall(self.predMsg)
                connToPredictorPHP.close()

                self.predMsg = ""
