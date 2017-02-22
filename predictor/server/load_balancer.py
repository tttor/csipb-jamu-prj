#!/usr/bin/python
import sys
import socket
import signal
from datetime import datetime

connFromPredictorPHP = None

def main(argv):
    if len(sys.argv)!=5:
        print 'USAGE: phyton load_balancer.py [phpApiPort] [serverPortLo] [serverPortHi] [waitingTimeStr]'
        return

    port = int(argv[1])
    serverPortLo = int(argv[2])
    serverPortHi = int(argv[3])
    waitingTimeStr = argv[4]

    host = '127.0.0.1'
    upAt = datetime.now().strftime("%Y:%m:%d %H:%M:%S")
    nQueries = 0

    # TODO Check which serverPorts are listening
    # http://stackoverflow.com/questions/7436801/identifying-listening-ports-using-python
    serverUsage = []
    serverPorts = []
    for p in range(serverPortLo,serverPortHi+1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        r = s.connect_ex((host,p))
        if r==0:
            serverPorts.append(p)
            serverUsage.append(0)
        s.close()

    global connFromPredictorPHP
    connFromPredictorPHP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connFromPredictorPHP.bind( (host,port) )

    backlog = 1
    connFromPredictorPHP.listen(backlog)

    while True:
        serverUsageDict = dict()
        for i,ii in enumerate(serverPorts):
            serverUsageDict[ii] = serverUsage[i]

        print("###############################################################")
        print("Ijah predictor load-balancer :)")
        print(">> upFrom= "+upAt)
        print(">> waitingTime= "+waitingTimeStr+" seconds")
        print(">> HasDispatched= "+str(nQueries)+" queries")
        print(">> serverUsage= "+str(serverUsageDict))
        print("NOW: waiting for any query from 'predict.php' at "+host+":"+str(port))

        signal.signal(signal.SIGINT, signalHandler)
        connToPredictorPHP, connToPredictorAddr = connFromPredictorPHP.accept()
        try:
            print >>sys.stderr, 'Connection from', connToPredictorAddr

            message = ""
            while True:
                bufsize = 1024
                dataTemp = connToPredictorPHP.recv(bufsize)
                # print >>sys.stderr, 'Received "%s"' % dataTemp
                message += dataTemp

                if message[-3:]=="end":
                    break
        finally:
            # get server with fewest #servedQuery'
            serverIdx = serverUsage.index( min(serverUsage) )
            serverPort = serverPorts[serverIdx]

            serverUsage[serverIdx] += 1
            nQueries += 1

            #Send time to wait for prediction to predict.php
            connToPredictorPHP.sendall(waitingTimeStr)
            connToPredictorPHP.close()

            #Forward the message as is (received from predict.php)
            print 'passing the msg to '+host+': '+str(serverPort)
            connToServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connToServer.connect( (host,serverPort) )
            connToServer.sendall(message)
            connToServer.close()

    print 'load-balancer: shutting down ...'
    connFromPredictorPHP.close()

def signalHandler(signal, frame):
    sys.stderr.write("Closing socket ...\n")
    connFromPredictorPHP.close()
    sys.exit(0)

if __name__ == '__main__':
    main(sys.argv)
