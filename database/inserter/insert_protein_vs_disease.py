# insert_protein_vs_disease.py
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
    assert len(argv)>=8

    db = argv[1]
    user = argv[2]; passwd = argv[3]
    host = argv[4]; port = argv[5]
    outDir = argv[6]
    paths = argv[7:]

    conn = psycopg2.connect(database=db, user=user, password=passwd,
                            host=host, port=port)
    csr = conn.cursor()

    insertProteinVsDiseaseUniprot(csr,paths[0])
    deleteDiseasesHavingNoProtein(csr)

    conn.commit()
    conn.close()

def insertProteinVsDiseaseUniprot(csr,fpath):
    proteinDiseaseDict = None
    with open(fpath, 'rb') as handle:
        proteinDiseaseDict = pickle.load(handle)

    src = 'uniprot.org'
    idx = 0; log = []; n = len(proteinDiseaseDict)
    for p,v in proteinDiseaseDict.iteritems():
        idx += 1

        qf = 'SELECT pro_id FROM protein WHERE pro_uniprot_abbrv ='
        qm = "'" + p + "'"
        qr = ''
        q = qf+qm+qr
        csr.execute(q)
        proIdR = csr.fetchall(); assert len(proIdR)==1

        for d in v['disease']:
            omimId = d[2]
            msg = 'inserting '+p+' vs '+omimId+' idx= '+str(idx)+' of '+str(n)
            print msg

            qf = 'SELECT dis_id FROM disease WHERE dis_omim_id ='
            qm = "'" + omimId + "'"
            qr = ''
            q = qf+qm+qr
            csr.execute(q)
            disIdR = csr.fetchall(); assert len(disIdR)==1

            proId = proIdR[0][0]
            disId = disIdR[0][0]

            insertVals = [proId, disId, src]
            insertVals = ["'"+i+"'" for i in insertVals]

            qf = 'INSERT INTO protein_vs_disease (pro_id,dis_id,source) VALUES ('
            qm = ','.join(insertVals)
            qr = ')'
            q = qf+qm+qr
            csr.execute(q)

def deleteDiseasesHavingNoProtein(csr):
    print 'deleteDiseasesHavingNoProtein...'
    q = '''
        DELETE FROM disease where dis_id IN (
        SELECT
        distinct disease.dis_id
        FROM
        disease
        LEFT JOIN
        protein_vs_disease
        ON
        disease.dis_id = protein_vs_disease.dis_id
        WHERE
        protein_vs_disease.dis_id IS NULL
        );
        '''
    csr.execute(q)

if __name__ == '__main__':
    start_time = time.time()
    main(sys.argv)
    print("--- %s seconds ---" % (time.time() - start_time))
