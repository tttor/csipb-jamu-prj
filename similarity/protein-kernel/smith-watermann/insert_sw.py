# insert_sw.py
import os
import sys
import time
import psycopg2
import numpy as np

sys.path.append('../../../config')
from database_config import databaseConfig as dcfg

sys.path.append('../../../utility')
import postgresql_util as util

def main(argv):
    assert len(argv)==4
    outDir = argv[1]
    simFpath = argv[2]
    metaFpath = argv[3]

    conn = psycopg2.connect(database=dcfg['name'],
                            user=dcfg['user'],password=dcfg['passwd'],
                            host=dcfg['host'],port=dcfg['port'])
    csr = conn.cursor()
    insert(csr,conn,outDir,simFpath,metaFpath)
    conn.close()

def insert(csr,conn,outDir,simFpath,metaFpath):
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

    ## insert
    method = 'smith-watermann'
    for i,pro in enumerate(proList):
        if pro in uniprotID2proID:
            pro = uniprotID2proID[pro]
        else:
            continue

        s = 'inserting proSimSW '+pro+' idx= '+str(i+1)+' of '+str(len(proList))
        print s

        for j,pro2 in enumerate(proList):
            if pro2 in uniprotID2proID:
                pro2 = uniprotID2proID[pro2]
            else:
                continue

            if pro==pro2:
                continue

            val = mat[i][j]
            q  = "INSERT INTO protein_similarity (pro_id_i,pro_id_j,method,value) "
            q += "VALUES ("+util.quote(pro)+","+util.quote(pro2)+","
            q += util.quote(method)+","+str(val)+")"
            print q
            csr.execute(q)
        conn.commit()

if __name__ == '__main__':
    start_time = time.time()
    main(sys.argv)
    print("--- %s seconds ---" % (time.time() - start_time))
