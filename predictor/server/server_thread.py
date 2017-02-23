# predictor_server_thread.py
import threading
import socket
import sys
import psycopg2

from predictor_thread import PredictorThread as Predictor
from config import predictorConfig as pcfg
from config import databaseConfig as dcfg

class ServerThread(threading.Thread):
    def __init__(self,iid,iname,ihost,iport):
        threading.Thread.__init__(self)
        self.id = iid
        self.name = iname
        self.host = ihost
        self.port = iport
        self.queryNum = -1

        self.connDB = psycopg2.connect(database=dcfg['name'],user=dcfg['user'],password=dcfg['passwd'],
                                        host=dcfg['host'],port=dcfg['port'])
        self.cur = self.connDB.cursor()

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
                print >>sys.stderr,self.name+': Connection from',connToLBAddr
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
                queryList = [tuple(m.split(":")) for m in message.split(",")]
                for t in predictorThreads:
                    t.setQueryList(queryList)

                # Wait for all predictor threads to finish
                print >>sys.stderr,self.name+': Wait for all predictor threads to finish'
                for p in predictorThreads:
                    while p.getPredictionNumber()!=self.queryNum:
                        pass

                # Merge prediction results from predictor threads
                print >>sys.stderr,self.name+': Merge prediction results'
                predictionListRaw = [] # [2D] row: method and col: ith query
                for t in predictorThreads:
                    predictionListRaw.append( t.getPredictionList() )

                predictionList = []
                nMethods = len(pcfg['methods'])
                for i in range(len(queryList)):
                    normPred = 0.0
                    nValidPred = 0
                    for j in range(nMethods):
                        pred = predictionListRaw[j][i]
                        if (pred>=0)and(pred<=1):# valid
                            w = pcfg['methods'][j][1]
                            normPred +=  (w * pred)
                            nValid += 1

                    normalizer = 1.0/float(nValidPred)
                    normPred = normPred/normalizer

                    predictionList.append(nPred)
                # print self.name+': predictionList '+str(predictionList)

                # Push the prediction result to database
                print >>sys.stderr,self.name+': Push the prediction result to database'
                for i,p in enumerate(predictionList):
                    if p<0.0:# invalid
                        continue

                    comId,proId = queryList[i]
                    src = ','.join([i[0] for i in pcfg['methods']])

                    queryCheck = "SELECT * FROM compound_vs_protein WHERE "
                    queryCheck += "com_id='"+comId+"' AND pro_id='"+proId+"'"
                    self.cur.execute(queryCheck)
                    dataRows = self.cur.fetchall()

                    # ## Update row if data is already exsist on table ##
                    if len(dataRows)>0:
                        query1 = "UPDATE compound_vs_protein "
                        query2 = "SET source='"+src+"',weight='"+ str(p)+"',time_stamp=now() "
                        query3 = "WHERE com_id='"+comId+"' AND pro_id='"+proId+"'"

                    # ## Insert if no record found ##
                    else:
                        #May use INSERT INTO ..VALUE ... ON DUPLICATE KEY UPDATE
                        values = [comId,proId,src,str(p)]
                        values = ["'"+i+"'" for i in values]
                        valueStr = ",".join(values)

                        query1 = "INSERT INTO compound_vs_protein (com_id,pro_id,source,weight) "
                        query2 = "VALUES ("+valueStr+")"
                        query3 = ""

                    query = query1+query2+query3
                    self.cur.execute(query)
                    self.connDB.commit()
        self.connDB.close()
