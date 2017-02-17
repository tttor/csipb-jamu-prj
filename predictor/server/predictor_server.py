#!/usr/bin/python
import sys
from datetime import datetime

from predictor_server_thread import PredictorServerThread as PST
from config import serverConfig as scfg

def main():
    if len(sys.argv)!=2:
        print 'USAGE: phyton prediction_server.py [serverId]'
        return

    serverId = sys.argv[1]
    if serverId not in scfg['ports']:
        print 'FATAL: serverId unknown'
        return

    host = scfg['host']
    portLo,portHi = scfg['ports'][serverId]
    upAt = datetime.now().strftime("%Y:%m:%d %H:%M:%S")

    print >> sys.stderr, '******************************************************'
    print >> sys.stderr,"Ijah predictor server :)"
    print >> sys.stderr,"[id= "+serverId+"]"
    print >> sys.stderr,"[ports= "+str(portLo)+" to "+str(portHi)+"]"
    print >> sys.stderr,"[upFrom= "+upAt+"]"

    threadList = [PST(i,"serverThread_"+str(serverId)+"_"+str(i),host,port)
                  for i,port in enumerate(range(portLo, portHi+1))]

    for t in threadList:
        t.daemon=True
        t.start()

    while True:
        pass

if __name__ == '__main__':
    main()
