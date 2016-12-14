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

    insertPlantVsCompoundKnapsack(csr,outDir,paths[0])
    deletePlantsHavingNoCompound(csr)

    conn.commit()
    conn.close()

def insertPlantVsCompoundKnapsack(csr,outDir,fpath):
    pc = None # as plantCompoundDict
    with open(fpath, 'rb') as handle:
        pc = pickle.load(handle)

    src = 'knapsack.kanaya.naist.jp'
    idx = 0; n = len(pc); log = []
    for p,v in pc.iteritems():
        idx += 1

        qf = 'SELECT pla_id FROM plant WHERE pla_name ='
        qm = "'"+p+"'"
        qr = ''
        q = qf+qm+qr
        csr.execute(q)
        plaIdR = csr.fetchall(); assert len(plaIdR)==1

        comList = list( set([c[0] for c in v]) )
        for c in comList:
            msg = 'inserting '+ p+ ' vs '+ c+ ' idx= '+ str(idx)+ ' of '+ str(n)
            print msg

            qf = 'SELECT com_id FROM compound WHERE com_knapsack_id ='
            qm = "'" + c + "'"
            qr = ''
            q = qf+qm+qr
            csr.execute(q)
            comIdR = csr.fetchall();

            if len(plaIdR)!=0 and len(comIdR)!=0:
                plaId = plaIdR[0][0]
                comId = comIdR[0][0]

                insertVals = [plaId,comId,src]
                insertVals = ["'"+i+"'" for i in insertVals]

                qf = 'INSERT INTO plant_vs_compound (pla_id,com_id,source) VALUES ('
                qm = ','.join(insertVals)
                qr = ')'
                q = qf+qm+qr
                csr.execute(q)
            else:
                log.append('FAIL: '+msg)

    with open(outDir+'/plant_vs_compound_insertion_from_knapsack.log','w') as f:
        for i in log: f.write(str(i)+'\n')

def deletePlantsHavingNoCompound(csr):
    print 'deletePlantsHavingNoCompound...'
    q = '''
        DELETE FROM plant where pla_id IN (
        SELECT
        distinct plant.pla_id
        FROM
        plant
        LEFT JOIN
        plant_vs_compound
        ON
        plant.pla_id = plant_vs_compound.pla_id
        WHERE
        plant_vs_compound.pla_id IS NULL
        );
        '''
    csr.execute(q)

if __name__ == '__main__':
    start_time = time.time()
    main(sys.argv)
    print("--- %s seconds ---" % (time.time() - start_time))
