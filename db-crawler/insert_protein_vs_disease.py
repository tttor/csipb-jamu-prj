# insert_protein_vs_disease.py

def main():
    insertProteinVsDisease(proteinDiseaseDict)

def insertProteinVsDisease(proteinDiseaseDict):
    src = 'uniprot.org'
    n = len(proteinDiseaseDict)
    log = []; logFpath = dirPath+'/insertProteinVsDisease.log'
    idx = 0
    for p,v in proteinDiseaseDict.iteritems():
        idx += 1

        qf = 'SELECT pro_id FROM protein WHERE pro_uniprot_abbrv ='
        qm = '"' + p + '"'
        qr = ''
        q = qf+qm+qr
        proIdR = util.mysqlCommit(db,cursor,q)

        for d in v['disease']:
            msg = 'inserting '+ p+ ' vs '+ d[1]+ 'idx= '+ str(idx)+ ' of '+ str(n)
            print msg

            qf = 'SELECT dis_id FROM disease WHERE dis_omim_id ='
            qm = '"' + d[2] + '"'
            qr = ''
            q = qf+qm+qr
            disIdR = util.mysqlCommit(db,cursor,q)

            if proIdR!=None and disIdR!=None:
                proId = proIdR[0]
                disId = disIdR[0]

                insertVals = [proId, disId, src]
                insertVals = ['"'+i+'"' for i in insertVals]

                qf = 'INSERT INTO protein_vs_disease (pro_id,dis_id,pro_vs_dis_source) VALUES ('
                qm = ','.join(insertVals)
                qr = ')'
                q = qf+qm+qr

                util.mysqlCommit(db,cursor,q)
            else:
                log.append('FAIL: '+msg)

    with open(logFpath,'w') as f:
        for i in log:
            f.write(str(i)+'\n')

if __name__ == '__main__':
    main()
