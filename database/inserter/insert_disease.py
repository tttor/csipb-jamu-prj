# insert_disease.py
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

    insertDiseaseUniprot(csr,paths[0])

    conn.commit()
    conn.close()

def insertDiseaseUniprot(csr,fpath):
    diseaseList = None
    with open(fpath, 'rb') as handle:
        diseaseList = pickle.load(handle)

    omimDict = dict()
    for d in diseaseList:
        name, abbrv, omimId = d

        if omimId in omimDict:
            omimDict[omimId]['name'].append(name)
            omimDict[omimId]['abbrv'].append(abbrv)
        else:
            omimDict[omimId] = {'name':[name],'abbrv':[abbrv]}

    # for k,v in omimDict.iteritems():
    #     if len(v['name'])>1 or len(v['abbrv'])>1:
    #         print k,v
    # print len(omimDict)
    # return

    # representedList = []
    # # by "Epilepsy, idiopathic generalized 11"
    # representedList.append("Juvenile myoclonic epilepsy 8")
    # representedList.append("Juvenile absence epilepsy 2")

    idx = 0; n = len(omimDict)
    for omimId,v in omimDict.iteritems():
        idx += 1
        idStr = str(idx)
        idStr = idStr.zfill(8)
        idStr = 'DIS'+idStr
        print 'inserting ', idx, 'of', n

        name = '|'.join(v['name']);
        name = name.replace("'","''")
        abbrv = '|'.join(v['abbrv'])

        dis = [idStr,omimId,name,abbrv]
        dis = ["'"+i+"'" for i in dis]

        qf = 'INSERT INTO disease (dis_id,dis_omim_id,dis_name,dis_uniprot_abbrv) VALUES ('
        qm = ','.join(dis)
        qr = ')'
        sql = qf+qm+qr
        csr.execute(sql)

if __name__ == '__main__':
    start_time = time.time()
    main(sys.argv)
    print("--- %s seconds ---" % (time.time() - start_time))
