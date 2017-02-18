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

        serverAddr = (self.host,self.port)
        self.socketConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketConn.bind(serverAddr)
        self.resPredict = ""

    def run(self):
        self.socketConn.listen(1)
        dataTemp = ""
        message = ""
        while True:
            print >>sys.stderr,self.name+": Waiting for any query at "+self.host+":"+str(self.port)

            conn, addr = self.socketConn.accept()
            try:
                print >>sys.stderr, self.name+': Connection from', addr
                while True:
                    dataTemp = conn.recv(1024)
                    print >>sys.stderr, self.name+': Received "%s"' % dataTemp
                    message += dataTemp

                    if message[-3:]=="end":
                        # sys.stderr.write ("Fetching Data Finished....\n")
                        message = message.split("|")[0]
                        conn.close()
                        break
            finally:
                conn, addr = self.socketConn.accept()
                print >>sys.stderr, self.name+': Connection from', addr

                queryList = message.split(",")
                threadList = [Predictor(i,'predictorThread_'+self.name+'_'+method,
                                        queryList,method,pcfg['maxElapsedTime'])
                              for i,method in enumerate(pcfg['methods'])]

                for t in threadList:
                    t.daemon=True
                    t.start()

                for t in threadList:
                    self.resPredict += t.join()
                #TODO: a lock for Synchronizing the query string...?

                print >> sys.stderr, self.name+': resPredict = '+self.resPredict
                conn.sendall(self.resPredict)
                conn.close()

                self.resPredict = ""
                message = ""
                dataTemp = ""
