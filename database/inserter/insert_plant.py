# insert_plant.py
import os
import sys
import time
import json
import yaml
import MySQLdb
import pickle
import psycopg2
import datetime
from collections import defaultdict
from bs4 import BeautifulSoup
from urllib2 import urlopen

def main(argv):
    assert len(argv)>=8

    db = argv[1]
    user = argv[2]; passwd = argv[3]
    host = argv[4]; port = argv[5]
    mode = argv[6]; outDir = argv[7]
    paths = argv[8:]

    conn = psycopg2.connect(database=db, user=user, password=passwd,
                            host=host, port=port)
    csr = conn.cursor()

    if mode=='insertPlantsFromKnapsack':
        assert False,'fix insertPlantsFromKnapsack()'
    elif mode=='updatePlantIdrName':
        updatePlantIdrName(csr,outDir,paths[0])

    conn.commit()
    conn.close()

def updatePlantIdrName(csr,outDir,fpath):
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    latin2idr = {}
    with open(fpath,'r') as f:
        latin2idr = yaml.load(f)

    idx = 0
    log = []
    for latin,idr in latin2idr.iteritems():
        idx += 1
        s = 'updating '+latin+': '+idr+ ' idx= '+str(idx)+' of '+str(len(latin2idr))
        print s

        qf = "UPDATE plant SET pla_idr_name="+"'"+idr+"'"
        qr = " WHERE pla_name="+"'"+latin+"'"
        q = qf+qr
        csr.execute(q)
        affectedRows = csr.rowcount;

        if affectedRows==0:
            log.append('NOT FOUND:'+s)

    with open(outDir+'/updatePlantIdrName_'+timestamp+'.log','w') as f:
        for i in log: f.write(i+'\n');

def insertPlantsFromKnapsack(plantList,db,user,passwd,host,port):
    conn = psycopg2.connect(database=db, user=user, password=passwd,
                            host=host, port=port)
    cur = conn.cursor()

    nPlant = len(plantList)
    for idx, p in enumerate(plantList):
        plaId = str(idx+1)
        plaId = plaId.zfill(8)
        plaId = "'"+'PLA'+plaId+"'"
        print 'inserting ', plaId, 'of', str(nPlant)

        plaName = "'"+p+"'"

        qf = 'INSERT INTO plant (pla_id,pla_name) VALUES ('
        qm = plaId+','+plaName
        qr = ')'
        q = qf+qm+qr
        cur.execute(q)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    start_time = time.time()
    main(sys.argv)
    print("--- %s seconds ---" % (time.time() - start_time))
