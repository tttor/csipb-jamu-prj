#!/usr/bin/python
import sys
import socket
import signal
from datetime import datetime

from config import loadBalancerConfig as lbcfg
from config import serverConfig as scfg

connFromPredictorPHP = None

def main():
    if len(sys.argv)!=1:
        print 'USAGE: phyton prediction_load_balancer.py'
        return

    host = lbcfg['host']
    port = lbcfg['port']
    upAt = datetime.now().strftime("%Y:%m:%d %H:%M:%S")
    nQueries = 0

    serverUsage = []
    serverPorts = []
    for k,v in scfg['ports'].iteritems():
        ports = range(v[0],v[1]+1)
        serverPorts.append(ports)
        serverUsage.append([0]*len(ports))

    global connFromPredictorPHP
    connFromPredictorPHP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connFromPredictorPHP.bind( (host,port) )

    backlog = 1
    connFromPredictorPHP.listen(backlog)

    while True:
        print("###############################################################")
        print("Ijah predictor load-balancer :)")
        print("[HasDispatched= "+str(nQueries)+" queries]")
        print("[upFrom= "+upAt+"]")
        print("[serverUsage= "+str(serverUsage)+']')

        print('')
        print("Waiting for any query from 'predict.php' at "+host+":"+str(port))

        signal.signal(signal.SIGINT, signalHandler)
        connToPredictorPHP, connToPredictorAddr = connFromPredictorPHP.accept()
        try:
            print >>sys.stderr, 'Connection from', connToPredictorAddr

            message = ""
            while True:
                bufsize = 1024
                dataTemp = connToPredictorPHP.recv(bufsize)
                print >>sys.stderr, 'Received "%s"' % dataTemp
                message += dataTemp

                if message[-3:]=="end":
                    break
        finally:
            # get server with fewest #servedQuery'
            serverIdx = serverUsage.index( min(serverUsage) )
            serverThreadIdx = serverUsage[serverIdx].index( min(serverUsage[serverIdx]) )
            serverPort = serverPorts[serverIdx][serverThreadIdx]

            serverUsage[serverIdx][serverThreadIdx] += 1
            nQueries += 1

            #Send serverport to predict.php
            connToPredictorPHP.sendall( str(serverPort) )
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
    main()
