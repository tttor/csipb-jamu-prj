#!/usr/bin/python
import sys
from datetime import datetime

from server_thread import ServerThread as Server

def main(argv):
    if len(sys.argv)!=5:
        print 'USAGE: phyton server.py [serverId] [hostToListenFrom] [portToListenFromLo] [portToListenFromHi]'
        return

    serverId = argv[1]
    hostToListenFrom = argv[2]
    portToListenFromLo,portToListenFromHi = int(argv[3]),int(argv[4])
    upAt = datetime.now().strftime("%Y:%m:%d %H:%M:%S")

    print >> sys.stderr, '******************************************************'
    print >> sys.stderr,"Ijah predictor server :)"
    print >> sys.stderr,"[id= "+serverId+"]"
    print >> sys.stderr,"[portToListenFroms= "+str(portToListenFromLo)+" to "+str(portToListenFromHi)+"]"
    print >> sys.stderr,"[upFrom= "+upAt+"]"

    threadList = [Server(i,"serverThread_"+str(serverId)+"_"+str(i),hostToListenFrom,portToListenFrom)
                  for i,portToListenFrom in enumerate(range(portToListenFromLo, portToListenFromHi+1))]

    for t in threadList:
        t.daemon=True
        t.start()

    while True:
        pass

if __name__ == '__main__':
    main(sys.argv)
