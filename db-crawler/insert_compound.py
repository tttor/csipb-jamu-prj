# insert_compound.py
import os
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

outDir = '/home/tor/robotics/prj/csipb-jamu-prj/dataset/db-log'
db = MySQLdb.connect("localhost","root","123","ijah" )
cursor = db.cursor()

def main():
    if not os.path.exists(outDir):
        os.makedirs(outDir)

    # idx = int(util.mysqlGetMax(db,cursor,table='compound',col='com_id').strip('COM'))
    # idx = insertComFromDrugbank(idx)

    # idx = int(util.mysqlGetMax(db,cursor,table='compound',col='com_id').strip('COM'))
    # idx = insertComFromKnapsack(idx)

    idx = int(util.mysqlGetMax(db,cursor,table='compound',col='com_id').strip('COM'))
    idx = insertComFromKegg(idx)

def insertComFromDrugbank(comIdx):
    drugData = None
    fpath = '/home/tor/robotics/prj/csipb-jamu-prj/dataset/drugbank/drugbank_20161002/drugbank_drug_data_2016-10-05_10:16:42.860649.pkl'
    with open(fpath, 'rb') as handle:
        drugData = pickle.load(handle)

    for i,v in drugData.iteritems():
        if len(v['uniprotTargets'])==0:
            continue

        comIdx += 1
        print 'inserting', i, 'comIdx=',str(comIdx),'of at most', str(len(drugData))

        comId = str(comIdx); comId = comId.zfill(8); comId = 'COM'+comId
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

        insertVals = ['' if len(i)==0 else i for i in insertVals]
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

    return comIdx

def insertComFromKnapsack(comIdx):
    plantCompoundDict = None
    fpath = '/home/tor/robotics/prj/csipb-jamu-prj/dataset/knapsack/20161003/knapsack_jsp_plant_vs_compound_2016-10-04_16:34:06.468234.pkl'
    with open(fpath, 'rb') as handle:
        plantCompoundDict = pickle.load(handle)

    compoundDict = {}
    for comList in plantCompoundDict.values():
        for kId,cas,name,form in comList:
            compoundDict[kId] = cas

    idx = 0
    nCom = len(compoundDict)
    matchList = []
    for k,cas in compoundDict.iteritems():
        idx += 1
        print 'insert/updating', k, 'idx=',str(idx), 'of', nCom

        if util.mysqlExist(db, cursor,
                           table='compound', where='com_cas_id='+'"'+cas+'"'):
            # print 'match'
            matchList.append(cas)

            qf = 'UPDATE compound SET com_knapsack_id='
            qm = '"'+k+'"'
            qr = 'WHERE com_cas_id='+'"'+cas+'"'
            q = qf+qm+qr
            util.mysqlCommit(db,cursor,q)
        else:
            comIdx += 1
            comIdStr = 'COM'+str(comIdx).zfill(8)

            insertVals = [comIdStr,cas,k]
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

    return comIdx

def insertComFromKegg(comIdx):
    comDataDpath = '/home/tor/robotics/prj/csipb-jamu-prj/dataset/kegg/kegg_20161010/keggCom_20161010_1-100K'
    drugDataFpath = '/home/tor/robotics/prj/csipb-jamu-prj/dataset/kegg/kegg_20161010/keggdrug_data_2016-10-11_16:58:04.683546.pkl'

    # Load Kegg compound data
    data = {}
    for filename in os.listdir(comDataDpath):
        if filename.endswith(".pkl"):
            fpath = os.path.join(comDataDpath, filename)
            dPerFile = {}
            with open(fpath, 'rb') as handle:
                dPerFile = pickle.load(handle)

            for k,v in dPerFile.iteritems():
                if len(v)!=0:
                    data[k] = v

    sortedK = data.keys()
    sortedK.sort()
    fpath = outDir + '/keggComData_validComId.lst'
    with open(fpath,'w') as f:
        for k in sortedK:
            f.write(str(k)+'\n')

    # Load Kegg drug data, to infer their drugbank equivalent
    drugData = None
    with open(drugDataFpath, 'rb') as handle:
        drugData = pickle.load(handle)

    # Update or Insert
    insertList = []

    n = len(data)
    idx = 0
    for keggId,d in data.iteritems():
        idx += 1
        print 'insert/update keggId=', keggId, 'idx=', idx, 'of', n

        knapsackId = ''
        if 'knapsackId' in d.keys():
            knapsackId = d['knapsackId']

        drugbankId = ''
        if 'keggDrugId' in d.keys():
            _ = drugData[ d['keggDrugId'] ]['drugbankId']
            if len(_)!=0:
                drugbankId = _

        casId = ''
        if 'casId' in d.keys():
            casId = d['casId']

        insert = False

        if knapsackId!='':
            # check if exist
            if util.mysqlExist(db, cursor,
                               table='compound',where='com_knapsack_id='+'"'+knapsackId+'"'):
                # update based on knapsackID
                qf = 'UPDATE compound '
                qm = 'SET '+ 'com_kegg_id=' + '"'+keggId+'"'
                if casId!='':
                    qm = qm + ',' + ' com_cas_id=' + '"'+casId+'"'
                if drugbankId!='':
                    qm = qm + ',' + ' com_drugbank_id=' + '"'+drugbankId+'"'
                qr = ' WHERE com_knapsack_id='+ '"' + knapsackId + '"'
                q = qf+qm+qr
                resp = util.mysqlCommit(db,cursor,q)
            else:
                insert = True

        if drugbankId!='':
            if util.mysqlExist(db, cursor,
                               table='compound',where='com_drugbank_id='+'"'+drugbankId+'"'):
                # update based on drugbankId
                qf = 'UPDATE  compound '
                qm = 'SET '+ 'com_kegg_id=' + '"'+keggId+'"'
                if casId!='':
                    qm = qm + ','+ ' com_cas_id=' + '"'+casId+'"'
                if knapsackId!='':
                    qm = qm + ','+ ' com_knapsack_id=' + '"'+knapsackId+'"'
                qr = ' WHERE com_drugbank_id='+ '"' + drugbankId + '"'
                q = qf+qm+qr
                resp = util.mysqlCommit(db,cursor,q)
            else:
                insert = True

        if insert:
            comIdx += 1
            comIdStr = 'COM'+ str(comIdx).zfill(8)

            insertVals = [comIdStr, casId,drugbankId,knapsackId,keggId]
            insertVals = ['"'+i+'"' for i in insertVals]

            qf = 'INSERT INTO compound (com_id,com_cas_id,com_drugbank_id,com_knapsack_id,com_kegg_id)'
            qr = ' VALUES (' + ','.join(insertVals) + ')'
            q = qf + qr
            resp = util.mysqlCommit(db,cursor,q)

            insertList.append(q)

    insertListFpath = outDir + '/insertion_from_keggComData.lst'
    with open(insertListFpath,'w') as f:
        for l in insertList:
            f.write(str(l)+'\n')

    return comIdx

if __name__ == '__main__':
    main()
    db.close()
