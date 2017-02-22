#!/usr/bin/python
import sys
from datetime import datetime

from server_thread import ServerThread as Server

def main(argv):
    if len(sys.argv)!=5:
        print 'USAGE: phyton server.py [serverId] [host] [portLo] [portHi]'
        return

    serverId = argv[1]
    host = argv[2]
    portLo,portHi = int(argv[3]),int(argv[4])
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
