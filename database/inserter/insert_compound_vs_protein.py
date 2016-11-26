# insert_compound_vs_protein.py
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

    insertCompoundVsProteinDrugbank(csr,outDir,paths[0])

    conn.commit()
    conn.close()

def insertCompoundVsProteinDrugbank(csr,outDir,fpath):
    drugProteinDict = None # as plantCompoundDict
    with open(fpath, 'rb') as handle:
        drugProteinDict = pickle.load(handle)

    src = 'drugbank.ca'
    idx = 0; log = []; n = len(drugProteinDict)
    for i,v in drugProteinDict.iteritems():
        idx += 1

        qf = 'SELECT com_id FROM compound WHERE com_drugbank_id ='
        qm = "'" + i + "'"
        qr = ''
        q = qf+qm+qr
        csr.execute(q)
        comIdR = csr.fetchall(); #assert len(comIdR)==1

        pList = list(set(v['uniprotTargets']))
        for p in pList:
            msg = 'inserting '+i+ ' vs '+p+' idx= '+ str(idx)+ ' of '+ str(n)
            print msg

            qf = 'SELECT pro_id FROM protein WHERE pro_uniprot_id ='
            qm = "'" + p + "'"
            qr = ''
            q = qf+qm+qr
            csr.execute(q)
            proIdR = csr.fetchall(); #assert len(proIdR)==1

            if len(comIdR)!=0 and len(proIdR)!=0:
                proId = proIdR[0][0]
                comId = comIdR[0][0]

                insertVals = [comId,proId,src]
                insertVals = ["'"+j+"'" for j in insertVals]

                qf = '''INSERT INTO compound_vs_protein (com_id,pro_id,source)
                        VALUES ('''
                qm = ','.join(insertVals)
                qr = ')'
                q = qf+qm+qr
                csr.execute(q)
            else:
                msg = 'FAIL: '+msg
                print msg
                log.append(msg)

    with open(outDir+'/compound_vs_protein_insertion_from_drugbank.log','w') as f:
        for l in log: f.write(str(l)+'\n')

if __name__ == '__main__':
    start_time = time.time()
    main(sys.argv)
    print("--- %s seconds ---" % (time.time() - start_time))
