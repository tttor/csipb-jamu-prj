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
    elif mode=='updateComBasedOnKegg':
        updateComBasedOnKegg(csr,outDir,paths[0],paths[1])
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

    supercededList = []
    supercededList.append('DB02630')# by DB02053
    supercededList.append('DB03357')# by DB02280
    supercededList.append('DB02539')# by DB02234
    supercededList.append('DB01786')# by DB00160
    supercededList.append('DB00994')# by DB00452
    supercededList.append('DB02174')# by DB00130
    supercededList.append('DB02351')# by DB00006
    supercededList.append('DB03225')# by DB00150

    casIdConflictList = []
    casIdConflictList.append('DB03655')# by DB06614 **
    casIdConflictList.append('DB02031')# by DB00116 **
    casIdConflictList.append('DB02975')# by DB02514 **
    casIdConflictList.append('DB02201')# by DB02175 **

    for i,v in drugData.iteritems():
        if len(v['uniprotTargets'])==0:
            continue

        if (i in supercededList) or (i in casIdConflictList):
            continue

        comIdx += 1
        print 'inserting',i,'comIdx=',str(comIdx),'of',str(len(drugData)),'(at most)'

        comId = str(comIdx); comId = comId.zfill(8); comId = 'COM'+comId
        comDrugbankId = i

        insertKeys = ['com_id','com_drugbank_id']
        insertVals = [comId,comDrugbankId]

        cas = v['CAS number']
        smiles = v['SMILES']
        if (cas!='not-available' and cas!='') and (smiles!='not-available' and smiles!=''):
            insertKeys.append('com_cas_id')
            insertVals.append(cas)

            insertKeys.append('com_smiles')
            insertVals.append(smiles)

            for ii,vv in v.iteritems():
                if vv!='not-available' and vv!='':
                    if ii=='InChI Key':
                        insertKeys.append('com_inchikey')
                        insertVals.append(vv)
                    elif ii=='pubchemCid':
                        insertKeys.append('com_pubchem_id')
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
        if k=='C00001193': #TODO why this breaks unique constraint in knapsackId
            continue

        idx += 1
        print 'insert/updating', k, 'idx=',str(idx), 'of', nCom,'(at most)'

        if cas!='' and cas!='not-available':
            if pg.doesExist(csr,'compound','com_cas_id',cas):
                # print 'match'
                matchList.append(cas)

                qf = 'UPDATE compound SET com_knapsack_id='
                qm = "'"+k+"'"
                qr = 'WHERE com_cas_id='+"'"+cas+"'"
                q = qf+qm+qr
                csr.execute(q)
            else:
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

def updateComBasedOnKegg(csr,outDir,comDataDpath,drugDataFpath):
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
    comIdx = 0
    currComId = pg.getMax(csr,'com_id','compound')
    if currComId!=None:
        comIdx = int(currComId.strip('COM'))

    insertList = []
    n = len(comData); idx = 0
    duplicateList = ['C00031','C10906','C00334','C00116','C00475']# TODO fix this
    for keggId,d in comData.iteritems():
        if keggId in duplicateList:
            continue

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

        knapsackIdFound = False # knapsackId should always represent(have) casId
        if knapsackId!='':
            if pg.doesExist(csr,'compound','com_knapsack_id',knapsackId):
                knapsackIdFound = True

        drugbankIdFound = False
        if drugbankId!='':
            if pg.doesExist(csr,'compound','com_drugbank_id',drugbankId):
                drugbankIdFound = True

        knapsackId = "'"+knapsackId+"'"
        drugbankId = "'"+drugbankId+"'"
        keggId = "'"+keggId+"'"

        if drugbankIdFound or knapsackIdFound:
            qf = 'UPDATE compound '
            qm = 'SET '+ 'com_kegg_id='+keggId
            if drugbankId!="''":
                qm = qm + ',' + ' com_drugbank_id=' + drugbankId
            if knapsackId!="''":
                qm = qm + ','+ ' com_knapsack_id=' + knapsackId
            qr = ' WHERE com_knapsack_id='+knapsackId+' OR com_drugbank_id='+drugbankId
            q = qf+qm+qr
            csr.execute(q)

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
