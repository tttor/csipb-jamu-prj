# insert_compound.py
import time
import json
import yaml
import MySQLdb
import pickle
import dbcrawler_util as util
from collections import defaultdict
from bs4 import BeautifulSoup
from urllib2 import urlopen
from datetime import datetime

outDir = '/home/tor/robotics/prj/csipb-jamu-prj/dataset/knapsack/20161003'
db = MySQLdb.connect("localhost","root","123","ijah" )
cursor = db.cursor()

def main():
    idx = 0
    insertComFromDrugbank(idx)
    # insertComFromKnapsack()

def insertComFromDrugbank(idx):
    drugData = None
    fpath = '/home/tor/robotics/prj/csipb-jamu-prj/dataset/drugbank/drugbank_20161002/drugbank_drug_data_2016-10-05_10:16:42.860649.pkl'
    with open(fpath, 'rb') as handle:
        drugData = pickle.load(handle)

    for i,v in drugData.iteritems():
        if len(v['uniprotTargets'])==0:
            continue

        idx += 1
        print 'inserting', i, 'idx=',str(idx),'of at most', str(len(drugData))
        
        comId = str(idx); comId = comId.zfill(8); comId = 'COM'+comId
        comDrugbankId = i
        na = ''
        
        insertVals = []
        insertVals.append(comId)
        insertVals.append(comDrugbankId)

        insertKeys = ['CAS number', 'pubchemCid', 'InChI Key', 
                      'SMILES','com_knapsack_id','com_kegg_id', 'com_simcomp']
        for k in insertKeys:
            if k in v.keys():
                insertVals.append(v[k])
            else:
                insertVals.append(na)

        insertVals = ['' if 'not-available' in i else i for i in insertVals]
        insertVals = ['"'+iv+'"' for iv in insertVals ]; assert len(insertVals)==9

        qf = '''INSERT INTO compound (com_id, com_drugbank_id,
                                      com_cas_id, com_pubchem_id, com_inchikey, 
                                      com_smiles, com_knapsack_id, com_kegg_id, com_simcomp)
             VALUES ('''
        qm = ','.join(insertVals)
        qr = ')'
        sql = qf+qm+qr
        util.mysqlCommit(db, cursor, sql)

    return idx

def insertComFromKnapsack():
    plantCompoundDict = None
    fpath = '/home/tor/robotics/prj/csipb-jamu-prj/dataset/knapsack/20161003/knapsack_jsp_plant_vs_compound_2016-10-04_16:34:06.468234.pkl'  
    with open(fpath, 'rb') as handle:
        plantCompoundDict = pickle.load(handle)

    compoundDict = {}
    for comList in plantCompoundDict.values():
        for kId,cas,name,form in comList:
            compoundDict[kId] = (cas,form)
    insertCompound(compoundDict)

    # get the last of the current comId, after inserting from drugbank
    comIdStr = 'COM00006661' #TODO unhardcode
    comId = int(comIdStr.strip('COM'))

    #
    idx = 0
    nCom = len(compoundDict)
    matchList = []
    for k,v in compoundDict.iteritems():
        idx += 1
        print 'insert/updating', k, 'idx=',str(idx), 'of', nCom

        cas,form = v

        casMatch = None
        if cas!='':
            qf = 'SELECT * FROM compound WHERE com_cas_id='
            qm = '"'+cas+'"'
            qr = ''
            q = qf+qm+qr
            casMatch = util.mysqlCommit(db, cursor,q)
        # print casMatch

        if casMatch!=None:
            # print 'match'
            matchList.append(cas)

            qf = 'UPDATE compound SET com_knapsack_id='
            qm = '"'+k+'"'
            qr = 'WHERE com_cas_id='+'"'+cas+'"'
            q = qf+qm+qr
            util.mysqlCommit(db,cursor,q)
        else:
            comId += 1
            comIdStr = 'COM'+str(comId).zfill(8)

            insertVals = [comIdStr,cas,k]
            insertVals = ['not-available' if i=='' else i for i in insertVals]
            insertVals = ['"'+i+'"' for i in insertVals]

            qf = 'INSERT INTO compound (com_id,com_cas_id,com_knapsack_id) VALUES ('
            qm =','.join(insertVals)
            qr = ')'
            q = qf+qm+qr
            util.mysqlCommit(db,cursor,q)

    fpath = outDir+'/knapsack_compound_match_with_drugbank.lst'
    with open(fpath,'w') as f:
        for m in matchList:
            f.write(str(m)+'\n')

if __name__ == '__main__':
    main()
    db.close()
