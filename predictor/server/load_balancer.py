#!/usr/bin/python
import sys
import socket
import signal
from datetime import datetime

from config import loadBalancerConfig as lbcfg
from config import serverConfig as scfg

conn = None

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

    global conn
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.bind( (host,port) )

    backlog = 1
    conn.listen(backlog)
    message = ""
    while True:
        print("###############################################################")
        print("Ijah predictor load-balancer :)")
        print("[HasDispatched= "+str(nQueries)+" queries]")
        print("[upFrom= "+upAt+"]")
        print("[serverUsage= "+str(serverUsage)+']')

        print('')
        print("Waiting for any query from 'predict.php' at "+host+":"+str(port))

        signal.signal(signal.SIGINT, signalHandler)
        conn, addr = conn.accept()
        try:
            print >>sys.stderr, 'Connection from', addr
            while True:
                bufsize = 1024
                dataTemp = conn.recv(bufsize)
                print >>sys.stderr, 'Received "%s"' % dataTemp
                message += dataTemp

                if message[-3:]=="end":
                    # sys.stderr.write ("Fetching Data Finished....\n")
                    break
        finally:
            # get server with fewest #servedQuery'
            serverIdx = serverUsage.index( min(serverUsage) )
            serverThreadIdx = serverUsage[serverIdx].index( min(serverUsage[serverIdx]) )
            serverPort = serverPorts[serverIdx][serverThreadIdx]

            serverUsage[serverIdx][serverThreadIdx] += 1
            nQueries += 1

            #Connecting to serverThread server
            conn2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn2.connect( (host,serverPort) )

            #Forward the message as is (received from predict.php)
            print 'passing the msg to '+host+': '+str(serverPort)
            conn2.sendall(message)

            #Send serverport to predict.php
            conn.sendall( str(serverPort) )

            #close connection
            conn2.close()

            #Reset Variables
            message = ""

    print 'load-balancer: shutting down ...'
    conn.close()

def signalHandler(signal, frame):
    sys.stderr.write("Closing socket ...\n")
    conn.close()
    sys.exit(0)

if __name__ == '__main__':
    main()
