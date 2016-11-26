# insert_protein.py
import os
import sys
import time
import json
import yaml
import MySQLdb
import pickle
import psycopg2
import postgresql_util as pg
from collections import defaultdict
from bs4 import BeautifulSoup
from urllib2 import urlopen
from datetime import datetime

def main(argv):
    assert len(argv)>=7

    db = argv[1]
    user = argv[2]; passwd = argv[3]
    host = argv[4]; port = argv[5]
    paths = argv[6:]

    conn = psycopg2.connect(database=db, user=user, password=passwd,
                            host=host, port=port)
    csr = conn.cursor()

    insertProteinUniprot(csr,paths[0])

    conn.commit()
    conn.close()

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
