# insert_protein.py
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
    elif mode=='updateProteinSmithWaterman':
        updateProteinSmithWaterman(csr,paths[0],paths[1])
    else:
        assert False,'Unknown Mode!'

    conn.commit()
    conn.close()

def updateProteinSmithWaterman(csr,simFpath,metaFpath):
    proList = [] # uniprodID
    with open(metaFpath,'r') as f:
        for line in f:
            s = line.strip()
            proList.append(s)

    mat = np.loadtxt(simFpath,delimiter=',')
    assert mat.shape[0]==mat.shape[1]
    assert mat.shape[0]==len(proList)

    ## get uniproID to proID mapping
    q = "SELECT pro_uniprot_id,pro_id FROM protein where pro_uniprot_id!=''"
    csr.execute(q)
    resp = csr.fetchall(); assert len(resp)>0
    uniprotID2proID = {u:p for u,p in resp}

    print len(uniprotID2proID)

    ## update
    for i,pro in enumerate(proList):
        s = 'updating proSimSW '+pro+' idx= '+str(i+1)+' of '+str(len(proList))
        print s

        simStrList = []
        for j,pro2 in enumerate(proList):
            sim = mat[i][j]
            simStr = uniprotID2proID[pro2]+':'+pro2+'='+str(sim)
            simStrList.append(simStr)

        simStrMerged = ','.join(simStrList)
        simStrMerged = "'"+simStrMerged+"'"
        qf = "UPDATE protein SET pro_similarity_smithwaterman="+simStrMerged
        qr = " WHERE pro_uniprot_id="+"'"+pro+"'"
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
