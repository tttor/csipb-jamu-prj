# insert_plant.py
import os
import sys
import time

import json
import yaml
import pickle
import psycopg2
import datetime
from collections import defaultdict
from bs4 import BeautifulSoup
from urllib2 import urlopen

sys.path.append('../utility')
import postgre_util as pgu

with open('../config_database.json','r') as f:
    dcfg = yaml.load(f)

def main(argv):
    conn = psycopg2.connect(database=dcfg['database'],
                          user=dcfg['user'], password=dcfg['password'],
                          host=dcfg['host'], port=dcfg['port'])
    csr = conn.cursor()


    conn.commit()
    conn.close()

def insertPlantsFromKnapsack(csr):
    fpath = ...
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

if __name__ == '__main__':
    start_time = time.time()
    main(sys.argv)
    print("--- %s seconds ---" % (time.time() - start_time))
