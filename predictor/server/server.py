#!/usr/bin/python
import sys
from datetime import datetime

from server_thread import ServerThread as Server

def main(argv):
    if len(sys.argv)!=4:
        print 'USAGE: phyton prediction_server.py [serverId] [portLo] [portHi]'
        return

    host = '127.0.0.1'
    serverId = argv[1]
    portLo,portHi = int(argv[2]),int(argv[3])
    upAt = datetime.now().strftime("%Y:%m:%d %H:%M:%S")

    print >> sys.stderr, '******************************************************'
    print >> sys.stderr,"Ijah predictor server :)"
    print >> sys.stderr,"[id= "+serverId+"]"
    print >> sys.stderr,"[ports= "+str(portLo)+" to "+str(portHi)+"]"
    print >> sys.stderr,"[upFrom= "+upAt+"]"

    threadList = [Server(i,"serverThread_"+str(serverId)+"_"+str(i),host,port)
                  for i,port in enumerate(range(portLo, portHi+1))]

    for t in threadList:
        t.daemon=True
        t.start()

    while True:
        pass

if __name__ == '__main__':
    main(sys.argv)
