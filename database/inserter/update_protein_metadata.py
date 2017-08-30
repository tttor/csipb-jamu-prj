# insert_protein.py

## PROTEIN #####################################################################
elif [ "$1" == "uppdb" ]; then
  mode=updateProteinPDB
  uniprot2pdbFpath=/home/tor/robotics/prj/csipb-jamu-prj/dataset/pdb/27Nov2016/uniprot2pdb.pkl
  python insert_protein.py $db $user $passwd $host $port $mode $outDir $uniprot2pdbFpath


import os
import sys
import time
import json
import yaml
import MySQLdb
import pickle
import psycopg2
import numpy as np
import postgresql_util as pg
from collections import defaultdict
from bs4 import BeautifulSoup
from urllib2 import urlopen
from datetime import datetime

def main(argv):
    assert len(argv)>=9

    db = argv[1]
    user = argv[2]; passwd = argv[3]
    host = argv[4]; port = argv[5]
    mode = argv[6]; outDir = argv[7]
    paths = argv[8:]

    conn = psycopg2.connect(database=db, user=user, password=passwd,
                            host=host, port=port)
    csr = conn.cursor()

    if mode=='insertProteinUniprot':
        insertProteinUniprot(csr,paths[0])
    elif mode=='updateProteinPDB':
        updateProteinPDB(csr,paths[0])
    else:
        assert False,'Unknown Mode!'

    conn.commit()
    conn.close()

def updateProteinPDB(csr,path):
    uniprot2pdb = None
    with open(path,'r') as f:
        uniprot2pdb = pickle.load(f)

    # _ = [len(i) for i in uniprot2pdb.values()]
    # print max(_)

    i = 0
    for uniprot,pdbList in uniprot2pdb.iteritems():
        i += 1
        s = 'updating pdb '+uniprot+' idx= '+str(i)+' of '+str(len(uniprot2pdb))
        print s

        simStrMerged = ','.join(pdbList)
        simStrMerged = "'"+simStrMerged+"'"
        qf = "UPDATE protein SET pro_pdb_id="+simStrMerged
        qr = " WHERE pro_uniprot_id="+"'"+uniprot+"'"
        q = qf+qr
        csr.execute(q)

def insertProteinUniprot(csr,fpath):
    proteinList = None
    with open(fpath, 'rb') as handle:
        proteinList = pickle.load(handle)

    for i,p in enumerate(proteinList):
        proId = str(i+1)
        proId = proId.zfill(8)
        proId = 'PRO'+proId
        print 'inserting ', proId, 'of', str(len(proteinList))

        proName, proUniprotId, proUniprotAbbrv = p
        proName = proName.replace("'","''")
        pro = [proId, proName, proUniprotId, proUniprotAbbrv]
        pro = ["'"+i+"'" for i in pro]

        # Prepare SQL query to INSERT a record into the database.
        qf = 'INSERT INTO protein (pro_id,pro_name,pro_uniprot_id,pro_uniprot_abbrv) VALUES ('
        qm = ','.join(pro)
        qr = ')'
        sql = qf+qm+qr
        csr.execute(sql)

if __name__ == '__main__':
    start_time = time.time()
    main(sys.argv)
    print("--- %s seconds ---" % (time.time() - start_time))
