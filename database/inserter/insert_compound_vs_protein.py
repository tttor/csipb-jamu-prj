# insert_compound_vs_protein.py

def main():
    fpath = '/home/tor/robotics/prj/csipb-jamu-prj/dataset/drugbank/drugbank_20161002/drugbank_drug_data_2016-10-05_10:16:42.860649.pkl'
    with open(fpath, 'rb') as handle:
        drugData = pickle.load(handle)
    # insertDrug(drugData)
    insertDrugVsProtein(drugData)

    #
    db.close()

def insertDrugVsProtein(drugProteinDict):
    idx = 0
    log = []; logFpath = outDir+'/insertDrugVsProtein.log'
    src = 'drugbank.ca'; weight = '1.0'
    for i,v in drugProteinDict.iteritems():
        idx += 1

        qf = 'SELECT com_id FROM compound WHERE com_drugbank_id ='
        qm = '"' + i + '"'
        qr = ''
        sql = qf+qm+qr
        comIdR = util.mysqlCommit(db,cursor,sql);

        pList = list(set(v['uniprotTargets']))
        for p in pList:
            msg = 'inserting '+ i+ ' vs '+ p+' idx= '+ str(idx)+ ' of '+ str(len(drugProteinDict))
            print msg

            qf = 'SELECT pro_id FROM protein WHERE pro_uniprot_id ='
            qm = '"' + p + '"'
            qr = ''
            sql = qf+qm+qr
            proIdR = util.mysqlCommit(db,cursor,sql);

            if comIdR!=None and proIdR!=None:
                proId = proIdR[0]
                comId = comIdR[0]

                insertVals = [comId,proId,weight,src]
                insertVals = ['"'+j+'"' for j in insertVals]

                qf = '''INSERT INTO compound_vs_protein (com_id,pro_id,
                                                         weight,source)
                        VALUES ('''
                qm = ','.join(insertVals)
                qr = ')'
                sql = qf+qm+qr
                util.mysqlCommit(db,cursor,sql)
            else:
                msg = 'FAIL: '+msg
                print msg
                log.append(msg)

    with open(logFpath,'w') as f:
        for l in log:
            f.write(str(l)+'\n')

if __name__ == '__main__':
    main()
