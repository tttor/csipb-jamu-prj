# predictor_server_thread.py
import threading
import socket

from predictor_machine_thread import PredictorMachineThread as PMT

class PredictorServerThread(threading.Thread):
    def __init__(self, threadId, name, host, port):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.name = name
        self.host = host
        self.port = port
        serverAddr = (self.host,self.port)
        self.socketConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketConn.bind(serverAddr)
        self.resPredict = ""

    def run(self):
        self.socketConn.listen(1)
        nQueries = 0
        dataTemp = ""
        message = ""
        while True:
            # print "###############################################################"
            # print >> sys.stderr,"Ijah predictor server :)"
            # print >> sys.stderr,"[port= "+str(self.port)+" on "+self.name+"]"
            # print >> sys.stderr,"[maxElapsedTimePerQuery= "+str(maxElapsedTime)+" seconds]"
            # print >> sys.stderr,"[HasServed= "+str(nQueries)+" queries]"
            # print >> sys.stderr,"[upFrom= "+upAt+"]"
            # print >> sys.stderr,self.name+": Waiting for any query at "+self.host+":"+str(self.port)

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
                nQueries += 1
                queryPair = message.split(",")

                threadList = [PMT(i,key+" on Port: "+str(self.port), queryPair,key) for i,key in enumerate(funcPointer)]
                for t in threadList:
                    t.daemon=True
                    t.start()
                for t in threadList:
                    self.resPredict += t.join()
                #a lock for Synchronizing the query string...?

                print >> sys.stderr, self.name+': resPredict = '+self.resPredict
                conn.sendall(self.resPredict)
                conn.close()

                self.resPredict = ""
                message = ""
                dataTemp = ""
