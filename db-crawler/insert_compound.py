# insert_compound.py
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
    assert len(argv)>=9

    db = argv[1]
    user = argv[2]; passwd = argv[3]
    host = argv[4]; port = argv[5]
    mode = argv[6]; outDir = argv[7]
    paths = argv[8:]

    conn = psycopg2.connect(database=db, user=user, password=passwd,
                            host=host, port=port)
    csr = conn.cursor()

    if mode=='insertComFromDrugbank':
        insertComFromDrugbank(csr,paths[0])
    elif mode=='insertComFromKnapsack':
        insertComFromKnapsack(csr,outDir,paths[0])
    elif mode=='insertComFromKegg':
        insertComFromKegg(csr,outDir,paths[0],paths[1])
    # elif mode=='updateForSimcomp':
    #     updateForSimcomp()
    else:
        assert False,'Unknown Mode!'

    conn.commit()
    conn.close()

def insertComFromDrugbank(csr,fpath):
    drugData = None
    with open(fpath, 'rb') as handle:
        drugData = pickle.load(handle)

    comIdx = 0
    currComId = pg.getMax(csr,'com_id','compound')
    if currComId!=None:
        comIdx = int(currComId.strip('COM'))
    assert comIdx==0,'insertComFromDrugbank _must_ be carried our first as the baseline!'

    for i,v in drugData.iteritems():
        if len(v['uniprotTargets'])==0:
            continue

        comIdx += 1
        print 'inserting', i, 'comIdx=',str(comIdx),'of', str(len(drugData))

        comId = str(comIdx); comId = comId.zfill(8); comId = 'COM'+comId
        comDrugbankId = i

        insertKeys = ['com_id','com_drugbank_id']
        insertVals = [comId,comDrugbankId]
        for ii,vv in v.iteritems():
            if vv!='not-available' and vv!='':
                if ii=='SMILES':
                    insertKeys.append('com_smiles')
                    insertVals.append(vv)
                elif ii=='InChI Key':
                    insertKeys.append('com_inchikey')
                    insertVals.append(vv)
        insertVals = ["'"+i+"'" for i in insertVals]

        qf = 'INSERT INTO compound ('+','.join(insertKeys)+') VALUES ('
        qm = ','.join(insertVals)
        qr = ')'
        sql = qf+qm+qr
        csr.execute(sql)

    return comIdx

def insertComFromKnapsack(csr,outDir,fpath):
    plantCompoundDict = None
    with open(fpath, 'rb') as handle:
        plantCompoundDict = pickle.load(handle)

    compoundDict = {}
    for comList in plantCompoundDict.values():
        for kId,cas,name,form in comList:
            compoundDict[kId] = cas

    comIdx = 0
    currComId = pg.getMax(csr,'com_id','compound')
    if currComId!=None:
        comIdx = int(currComId.strip('COM'))

    nCom = len(compoundDict)
    matchList = []
    idx = 0
    for k,cas in compoundDict.iteritems():
        idx += 1
        print 'insert/updating', k, 'idx=',str(idx), 'of', nCom

        if pg.doesExist(csr,'compound','com_cas_id',cas):
            # print 'match'
            matchList.append(cas)

            qf = 'UPDATE compound SET com_knapsack_id='
            qm = "'"+k+"'"
            qr = 'WHERE com_cas_id='+"'"+cas+"'"
            q = qf+qm+qr
            csr.execute(q)
        else:# insert
            comIdx += 1
            comIdStr = 'COM'+str(comIdx).zfill(8)

            insertVals = [comIdStr,cas,k]
            insertVals = ["'"+i+"'" for i in insertVals]

            qf = 'INSERT INTO compound (com_id,com_cas_id,com_knapsack_id) VALUES ('
            qm =','.join(insertVals)
            qr = ')'
            q = qf+qm+qr
            csr.execute(q)

    fpath = outDir+'/compound_match_knapsack_vs_drugbank.lst'
    with open(fpath,'w') as f:
        for m in matchList:
            f.write(str(m)+'\n')

    return comIdx

def insertComFromKegg(csr,outDir,comDataDpath,drugDataFpath):
    # Load Kegg compound data
    comData = {}
    for filename in os.listdir(comDataDpath):
        if filename.endswith(".pkl"):
            fpath = os.path.join(comDataDpath, filename)
            dPerFile = {}
            with open(fpath, 'rb') as handle:
                dPerFile = pickle.load(handle)

            for k,v in dPerFile.iteritems():
                if len(v)!=0:
                    comData[k] = v

    sortedK = comData.keys()
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
    n = len(comData); idx = 0
    for keggId,d in comData.iteritems():
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

        mustInsert = False
        if knapsackId!='':
            # check if exist
            if pg.doesExist(csr,'compound','com_knapsack_id',knapsackId):
                # update based on knapsackID
                qf = 'UPDATE compound '
                qm = 'SET '+ 'com_kegg_id=' + "'"+keggId+"'"
                if casId!='':
                    qm = qm + ',' + ' com_cas_id=' + "'"+casId+"'"
                if drugbankId!='':
                    qm = qm + ',' + ' com_drugbank_id=' + "'"+drugbankId+"'"
                qr = ' WHERE com_knapsack_id='+ "'" + knapsackId + "'"
                q = qf+qm+qr
                csr.execute(q)
            else:
                mustInsert = True

        if drugbankId!='':
            if pg.doesExist(csr,'compound','com_drugbank_id',drugbankId):
                # update based on drugbankId
                qf = 'UPDATE  compound '
                qm = 'SET '+ 'com_kegg_id=' + "'"+keggId+"'"
                if casId!='':
                    qm = qm + ','+ ' com_cas_id=' + "'"+casId+"'"
                if knapsackId!='':
                    qm = qm + ','+ ' com_knapsack_id=' + "'"+knapsackId+"'"
                qr = ' WHERE com_drugbank_id='+ "'" + drugbankId + "'"
                q = qf+qm+qr
                csr.execute(q)
            else:
                mustInsert = True

        comIdx = 0
        currComId = pg.getMax(csr,'com_id','compound')
        if currComId!=None:
            comIdx = int(currComId.strip('COM'))

        if mustInsert:
            comIdx += 1
            comIdStr = 'COM'+ str(comIdx).zfill(8)

            insertKeys = ['com_id','com_kegg_id']
            insertVals = [comIdStr,keggId]

            if casId!='':
                insertKeys.append('com_cas_id')
                insertVals.append(casId)
            if drugbankId!='':
                insertKeys.append('com_drugbank_id')
                insertVals.append(drugbankId)
            if knapsackId!='':
                insertKeys.append('com_knapsack_id')
                insertVals.append(knapsackId)

            insertVals = ["'"+i+"'" for i in insertVals]

            qf = 'INSERT INTO compound ('+','.join(insertKeys)+')'
            qr = ' VALUES (' + ','.join(insertVals) + ')'
            q = qf + qr
            csr.execute(q)

            insertList.append(q)

    insertListFpath = outDir + '/compound_insertion_from_keggComData_and_keggDrugData.lst'
    with open(insertListFpath,'w') as f:
        for l in insertList:
            f.write(str(l)+'\n')

    return comIdx

def updateForSimcomp():
    dirpath = '/home/tor/robotics/prj/csipb-jamu-prj/dataset/kegg/kegg_20161010/simcomp'

    # SELECT com_id FROM `compound` where com_kegg_id!=''
    q = 'SELECT com_id,com_kegg_id FROM `compound` where com_kegg_id!=""'
    resp = util.mysqlCommit(db,cursor,q, True)

    kegg2ComIdMap = {}

    for i in resp:
        kegg2ComIdMap[i[1]] = i[0]

    #
    for filename in os.listdir(dirpath):
        if filename.endswith(".sim"):
            keggId = filename.split('_')[1].strip('.sim').strip()
            fpath = os.path.join(dirpath, filename)

            simcomp = []
            with open(fpath) as infile:
                for line in infile:
                    words = line.split('=')
                    words = [i.strip() for i in words]
                    keggId2 = words[0]
                    if keggId2 in kegg2ComIdMap.keys():
                        comId = kegg2ComIdMap[keggId2]
                        score = words[1]
                        simcomp.append( comId+':'+keggId2+'='+score)

            if len(simcomp)!=0:
                simcompStr = '\n'.join(simcomp)
                simcompStr = '"'+simcompStr+'"'
                qf = 'UPDATE compound SET com_simcomp='+simcompStr
                qr = ' WHERE com_kegg_id='+'"'+keggId+'"'
                q = qf+qr
                util.mysqlCommit(db,cursor,q)

if __name__ == '__main__':
    start_time = time.time()
    main(sys.argv)
    print("--- %s seconds ---" % (time.time() - start_time))
