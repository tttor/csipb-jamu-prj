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
                queryList = [tuple(m.split(":")) for m in message.split(",")]
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
                for i,p in enumerate(predictionList):
                    if p<0.0:# invalid
                        continue

                    comId,proId = queryList[i].split(":")
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
