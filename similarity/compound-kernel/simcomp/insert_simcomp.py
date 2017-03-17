# insert_simcomp.py
import os
import sys
import time
import psycopg2

sys.path.append('../../../config')
from database_config import databaseConfig as dcfg

sys.path.append('../../../utility')
import postgresql_util as pgUtil

def main(argv):
    assert len(argv)==3
    outDir = argv[1]
    simcompDir = argv[2]

    conn = psycopg2.connect(database=dcfg['name'],
                            user=dcfg['user'],password=dcfg['passwd'],
                            host=dcfg['host'],port=dcfg['port'])
    csr = conn.cursor()
    insert(csr,conn,outDir,simcompDir)
    conn.close()

def insert(csr,conn,outDir,simcompDir):
    # SELECT com_id FROM `compound` where com_kegg_id!=''
    q = "SELECT com_kegg_id,com_id FROM compound where com_kegg_id!=''"
    csr.execute(q)
    resp = csr.fetchall(); assert len(resp)>0
    kegg2ComIdMap = {kegg:comId for kegg,comId in resp}

    #
    method = 'simcomp'
    idx = 0; log = []; n = len(kegg2ComIdMap)
    for keggId,comId in kegg2ComIdMap.iteritems():
        idx += 1
        s = 'inserting simcomp '+keggId+':'+comId+ ' idx= '+str(idx)+' of '+str(n)
        print s

        fname = 'simcomp_'+keggId
        fpath = os.path.join(simcompDir,fname)

        if os.path.exists(fpath):
            with open(fpath,'r') as infile:
                for line in infile:
                    words = line.split('=')
                    words = [i.strip() for i in words]
                    keggId2 = words[0]

                    if keggId2 in kegg2ComIdMap.keys():
                        comId2 = kegg2ComIdMap[keggId2]
                        score = words[1]

                        q  = "INSERT INTO compound_similarity (com_id_i,com_id_j,method,value) "
                        q += "VALUES ("+pgUtil.quote(comId)+","+pgUtil.quote(comId2)+","
                        q += pgUtil.quote(method)+","+score+")"
                        csr.execute(q)
                        conn.commit()
        else:
            s = 'NOT-FOUND: '+fpath+' for '+s
            log.append(s)

        if idx%100==0 or idx==n:
            with open(os.path.join(outDir,'updateComSimcomp.log'),'w') as f:
                for l in log: f.write(l+'\n')

if __name__ == '__main__':
    start_time = time.time()
    main(sys.argv)
    print("--- %s seconds ---" % (time.time() - start_time))
