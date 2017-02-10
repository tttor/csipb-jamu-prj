#!/usr/bin/python
import sys
import socket
import signal
from datetime import datetime

socketConn = None
serverPorts = [5556,5557]
serverUsage = []

def main():
    if len(sys.argv)!=3:
        print 'USAGE: phyton prediction_load_balancer.py [host] [port]'
        return

    host = sys.argv[1]
    port = int(sys.argv[2])
    upAt = datetime.now().strftime("%Y:%m:%d %H:%M:%S")
    nQueries = 0
    serverUsage = [0]*len(serverPorts)

    global socketConn
    socketConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    balancerAddr = (host,port)
    socketConn.bind(balancerAddr)

    backlog = 1
    socketConn.listen(backlog)
    message = ""
    while True:
        print("###############################################################")
        print("Ijah predictor load-balancer :)")
        print("[HasServed= "+str(nQueries)+" queries]")
        print("[upFrom= "+upAt+"]")
        print("[serverUsage= "+str(serverUsage)+']')

        print('')
        print("Waiting for any query at "+host+":"+str(port))

        signal.signal(signal.SIGINT, signalHandler)
        conn, addr = socketConn.accept()
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
            print 'pass to the least busy server'
            serverIdx = serverUsage.index(min(serverUsage))
            serverUsage[serverIdx] += 1

            #Connecting to server
            socketConn2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serverAddr = (host,serverPorts[serverIdx])
            socketConn2.connect(serverAddr)
            #Forward the message
            socketConn2.sendall(message)

            #Send serverport to php
            conn.sendall(str(serverAddr[1]))
            #close every connection
            conn.close()
            socketConn2.close()

            #Reset Variables
            message = ""

def signalHandler(signal, frame):
    sys.stderr.write("Closing socket and database ...\n")
    socketConn.close()
    sys.exit(0)

if __name__ == '__main__':
    main()
