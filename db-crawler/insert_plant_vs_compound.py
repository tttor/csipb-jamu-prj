# insert_plant_vs_compound.py
import os
import time
import json
import yaml
import MySQLdb
import pickle
import dbcrawler_util as util
from collections import defaultdict
from bs4 import BeautifulSoup
from urllib2 import urlopen
from datetime import datetime

def main():
    insertPlantVsCompound(plantCompoundDict)

def insertPlantVsCompound(plantCompoundDict):
    pc = plantCompoundDict
    src = 'knapsack.kanaya.naist.jp'
    log = []; logFpath = outDir+'/insertPlantVsCompound.log'

    n = len(pc); idx = 0;
    for p,v in pc.iteritems():
        idx += 1

        qf = 'SELECT pla_id FROM plant WHERE pla_name ='
        qm = '"'+p+'"'
        qr = ''
        q = qf+qm+qr
        plaIdR = util.mysqlCommit(db,cursor,q);

        comList = list( set([c[0] for c in v]) )
        for c in comList:
            msg = 'inserting '+ p+ ' vs '+ c+ ' idx= '+ str(idx)+ ' of '+ str(n)
            print msg

            qf = 'SELECT com_id FROM compound WHERE com_knapsack_id ='
            qm = '"' + c + '"'
            qr = ''
            q = qf+qm+qr
            comIdR = util.mysqlCommit(db,cursor,q);

            if plaIdR!=None and comIdR!=None:
                plaId = plaIdR[0]
                comId = comIdR[0]

                insertVals = [plaId,comId,src]
                insertVals = ['"'+i+'"' for i in insertVals]

                qf = 'INSERT INTO plant_vs_compound (pla_id,com_id,source) VALUES ('
                qm = ','.join(insertVals)
                qr = ')'
                q = qf+qm+qr
                util.mysqlCommit(db,cursor,q)
            else:
                log.append('FAIL: '+msg)

    with open(logFpath,'w') as f:
        for i in log:
            f.write(str(i)+'\n')
            
if __name__ == '__main__':
    main()
