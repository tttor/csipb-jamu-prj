import numpy as np
import urllib2 as ulib
import csv
import psycopg2
import sys
import time
import json
'''
to do:
SUPERTARGET
BRENDA
DsigDB
'''

sys.path.append('../../utility')
from map_id_util import mapUniprotToKEGG,mapKEGGToCAS,mapPCToCAS,baseURL

sys.path.append('../../config')
from database_config import databaseConfig as dcfg

connDB = psycopg2.connect(database=dcfg['name'],user=dcfg['user'],password=dcfg['passwd'],
                                host=dcfg['host'],port=dcfg['port'])
cur = connDB.cursor()

columnTable = {'protein':["pro_id","pro_uniprot_id"],'compound':['com_id','com_cas_id'
            ,'com_pubchem_id','com_drugbank_id'], 'int':['com_id','pro_id']}
condTable = {'int':["weight = 1"]}

def main():
    if (len(sys.argv)<2 or len(sys.argv)>3):
        print "Error Usage: python pullCompProtInteraction.py [kegg|matador tsv_file]"
        return
    source = sys.argv[1]
    if source == "matador":
        dataPath = sys.argv[2]
    print "load known data"
    protein = loadTable('protein',columnTable['protein'])
    ijahUniprotDict = {p[1]:p[0] for p in protein}
    uniProtId = set([p[1] for p in protein])
    compound = loadTable('compound',columnTable['compound'])
    casId = set([c[1] for c in compound])
    ijahCasDict = {c[1]:c[0] for c in compound}
    knownInt = loadTable('compound_vs_protein',columnTable['int'],condTable['int'])
    knownInt = set(knownInt)
    newInt = dict()

    if source == "kegg":
        print "Get KEGG ID"
        upToKegg,keggSet = mapUniprotToKEGG(list(uniProtId))
        print "Get Interaction Data"
        keggInt,kcID = getKEGGinteractionData(list(keggSet))
        print "Get CAS ID"
        kCasDict = mapKEGGToCAS(list(kcID))
        for prot in protein:
            newInt[prot[1]] = []
            if prot[1] in upToKegg:
                for i in upToKegg[prot[1]]:
                    if i in keggInt:
                        newInt[prot[1]] += keggInt[i]

        for pK,cL in newInt.iteritems():
            casList = []
            for c in cL:
                if c in kCasDict:
                    casList += [kCasDict[c]]
            newInt[pK] = casList
    elif source == "matador":
        with open(dataPath,'r') as df:
            csvContent = csv.reader(df,delimiter='\t',quotechar='\"')
            pcID = set()
            newInt = dict()
            for i,row in enumerate(csvContent):
                if i==0:
                    continue
                pcID.add(row[0])
                for prot in row[6].split():
                    if prot[:6] in newInt:
                        newInt[prot[:6]] += [row[0]]
                    else:
                        newInt[prot[:6]] = [row[0]]

        pcCasDict = mapPCToCAS(list(pcID))
        for pKey,cList in newInt.iteritems():
            casList = []
            for c in cList:
                if int(c) in pcCasDict:
                    casList += pcCasDict[int(c)]
            newInt[pKey] = casList
    else:
        print "Invalid dbSource"
        return

    # validate pair with known database
    additionInt = []
    for pKey,cList in newInt.iteritems():
        if pKey in uniProtId:
            pIjahKey = ijahUniprotDict[pKey]
            for c in cList:
                if (c in casId):
                    cIjahkey = ijahCasDict[c]
                    if (pIjahKey,cIjahkey) not in knownInt:
                        additionInt.append((pIjahKey,cIjahkey))

    print len(additionInt)

    insertInteraction(additionInt,source)
    connDB.close()

def insertInteraction(interaction,s):
    for i in interaction:
        query = "INSERT INTO compound_vs_protein VALUES"
        query +=  "(\'%s\',\'%s\',\'%s\',1)"%(i[1],i[0],s)
        cur.execute()
    connDB.commit()

def getKEGGinteractionData(kID):
    retDict = dict()
    retList = []
    startBatch = 0
    step = 10
    nQuery = len(kID)
    while (startBatch < nQuery):
        print startBatch
        if startBatch+step < nQuery:
            lenBatch = step
        else:
            lenBatch = nQuery - startBatch
        urlTarget = baseURL['kegg']+"get/"
        for i in range(startBatch,lenBatch+startBatch):
            if i > startBatch:
                urlTarget += "+"
            urlTarget += kID[i]
        connection = ulib.urlopen(urlTarget)
        content = connection.read()
        lines = content.split("\n")
        pullData = False
        dataList = []
        for line in lines:
            headWord = line[:12].rstrip()
            content = line[12:].strip()
            if len(headWord)!=0:
                if headWord == "DRUG_TARGET":
                    pullData = True
                elif headWord == "ENTRY":
                    keggid = content.split()[0]
                elif headWord == "ORGANISM":
                    org = content.split()[0]
                else:
                    pullData = False
            if pullData:
                dbId,record = content.split(":")
                retList+=record.split()
                if org+":"+keggid in retDict:
                    retDict[org+":"+keggid] += record.split()
                else:
                    retDict[org+":"+keggid] = record.split()
        startBatch += lenBatch
    return retDict,set(retList)

def loadTable(table,column,condStr = "",optionStr = ""):
    queryStr = "SELECT "
    for i,col in enumerate(column):
        if i > 0:
            queryStr += ","
        queryStr = queryStr + col
    queryStr = queryStr + " FROM " + table

    if condStr is not "":
        queryStr += " WHERE "
        for i,cond in enumerate(condStr):
            if i > 0:
                queryStr += " OR "
            queryStr = queryStr + cond
    queryStr += " "+optionStr
    dataList = []
    cur.execute(queryStr)
    dataRows = cur.fetchall()
    for i,row in enumerate(dataRows):
        dataList.append(row)

    return dataList

if __name__ == '__main__':
    startTime = time.time()
    main()
    print time.time()-startTime
