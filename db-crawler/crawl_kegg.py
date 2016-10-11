# crawl_kegg.py
import time
import pickle
import json
import sys
import os
import MySQLdb
import httplib
import urllib2 as urllib
from collections import defaultdict
import dbcrawler_util as util
from datetime import datetime
from bs4 import BeautifulSoup as bs

baseDir = '/home/tor/robotics/prj/csipb-jamu-prj/dataset/kegg/kegg_20161010'
db = MySQLdb.connect("localhost","root","123","ijah" )
cursor = db.cursor()

def main(argv):
    # lo = int(argv[1]); hi = int(argv[2])
    # parseCompoundWebpage(lo,hi)

    # fpath = baseDir+'/drug'
    # parseDrugFile(fpath)

    comDataDpath = baseDir+'/keggCom_20161010x'
    drugDataFpath = baseDir+'/keggdrug_data_2016-10-11_16:58:04.683546.pkl'
    insertCompoundData(comDataDpath,drugDataFpath)

def insertCompoundData(comDataDpath,drugDataFpath):
    # Load Kegg compound data
    data = {}
    for filename in os.listdir(comDataDpath):
        if filename.endswith(".pkl"): 
            fpath = os.path.join(comDataDpath, filename)
            d = {}
            with open(fpath, 'rb') as handle:
                d = pickle.load(handle)

            for k,v in d.iteritems():
                if len(v)!=0:
                    data[k] = v
    # print len(data)

    # Load Kegg drug data, to infer their drugbank equivalent
    drugData = None
    with open(drugDataFpath, 'rb') as handle:
        drugData = pickle.load(handle)

    # Update or Insert
    comId = 21994 # TODO unhardcode
    insertList = []

    n = len(data)
    idx = 0
    for keggId,d in data.iteritems():
        idx += 1
        print 'insert/update keggId=', keggId, 'idx=', idx, 'of', n

        knapsackId = 'not-available'
        if 'knapsackId' in d.keys():
            knapsackId = d['knapsackId']

        drugbankId = 'not-available'
        if 'keggDrugId' in d.keys():
            _ = drugData[ d['keggDrugId'] ]['drugbankId']
            if len(_)!=0:
                drugbankId = _ 

        casId = 'not-available'
        if 'casId' in d.keys():
            casId = d['casId']

        insert = False

        if knapsackId!='not-available':
            # update based on knapsackID, assume exist
            qf = 'UPDATE compound '
            qm = 'SET '+ 'com_kegg_id=' + '"'+keggId+'"'
            if casId!='not-available':
                qm = qm + ',' + ' com_cas_id=' + '"'+casId+'"'
            if drugbankId!='not-available':
                qm = qm + ',' + ' com_drugbank_id=' + '"'+drugbankId+'"'
            qr = ' WHERE com_knapsack_id='+ '"' + knapsackId + '"'
            q = qf+qm+qr
            resp = util.mysqlCommit(db,cursor,q)

            if cursor.rowcount==0:# not exist, then insert
                insert = True
            else:
                insert = False

        if drugbankId!='not-available':
            # update based on knapsackID, assume exist
            qf = 'UPDATE  compound '
            qm = 'SET '+ 'com_kegg_id=' + '"'+keggId+'"'
            if casId!='not-available':
                qm = qm + ','+ ' com_cas_id=' + '"'+casId+'"'
            if knapsackId!='not-available':
                qm = qm + ','+ ' com_knapsack_id=' + '"'+knapsackId+'"'
            qr = ' WHERE com_drugbank_id='+ '"' + drugbankId + '"'
            q = qf+qm+qr
            resp = util.mysqlCommit(db,cursor,q)

            if cursor.rowcount==0:
                insert = True
            else:
                insert = False

        if insert:
            comId += 1
            comIdStr = 'COM'+ str(comId).zfill(8)

            insertVals = [comIdStr, casId,drugbankId,knapsackId,keggId]
            insertVals = ['"'+i+'"' for i in insertVals]

            qf = '''INSERT INTO compound (com_id,com_cas_id,com_drugbank_id,
                                          com_knapsack_id,com_kegg_id) '''
            qr = 'VALUES (' + ','.join(insertVals) + ')'
            q = qf + qr
            # resp = util.mysqlCommit(db,cursor,q) 

            insertList.append(q)

    insertListFpath = baseDir + '/insertion_from_keggComData.lst'
    with open(insertListFpath,'w') as f:
        for l in insertList:
            f.write(str(l)+'\n')

def parseDrugFile(fpath):
    hot = ''; n = 0; lookfor = False
    data = {}; now = datetime.now()
    with open(fpath) as infile:        
        for line in infile:
            n += 1
            words = line.split()

            if words[0]=='ENTRY':
                assert len(words)==3 or len(words)==4
                hot = words[1]
                data[hot] = defaultdict(list)
            elif words[0]=='REMARK' and words[1]=='Same' and words[2]=='as:':
                del words[0]; del words[0]; del words[0]
                cList = [w for w in words if 'C' in w]
                data[hot]['keggComId'] += cList
            elif words[0]=='DBLINKS':
                if 'DrugBank:' in words:
                    data[hot]['drugbankId'] = words[-1]
                else:
                    lookfor = True
            elif lookfor:
                if words[0]=='DrugBank:':
                    data[hot]['drugbankId'] = words[-1]
                    lookfor = False

    jsonFpath = baseDir+'/keggdrug_data_'+str(now.date())+'_'+str(now.time())+'.json'
    with open(jsonFpath, 'w') as f:
        json.dump(data, f, indent=2, sort_keys=True)

    pklFpath = baseDir+'/keggdrug_data_'+str(now.date())+'_'+str(now.time())+'.pkl'
    with open(pklFpath, 'wb') as f:
        pickle.dump(data, f)

    return data

def parseCompoundWebpage(loIdx, hiIdx):
    baseFpath = '/home/tor/robotics/prj/csipb-jamu-prj/dataset/kegg/kegg_20161010/'
    baseURL = 'http://www.genome.jp/dbget-bin/www_bget?cpd:'
    now = datetime.now()
    n = hiIdx - loIdx

    data = {}
    for i,j in enumerate(range(loIdx,hiIdx)):
        msg = 'parsing i= '+ str(i+1)+ '/'+ str(n)
        idStr = 'C'+str(j).zfill(5)

        # url = baseFpath+idStr+ '.html'
        url = baseURL+idStr
        msg = msg + ' from '+ url
        print msg

        html = None
        # with open(url, 'r') as content_file:
        #     html = content_file.read()
        try: 
            html = urllib.urlopen(url)
        except urllib.HTTPError, e:
            print('HTTPError = ' + str(e.code))
        except urllib.URLError, e:
            print('URLError = ' + str(e.reason))
        except httplib.HTTPException, e:
            print('HTTPException')
        except Exception:
            import traceback
            print('generic exception: ' + traceback.format_exc())

        datum = {}
        if html!=None:
            soup = bs(html,'html.parser')
            
            hrefDict = {}
            hrefDict['keggDrugId'] = '/dbget-bin/www_bget?dr:'
            hrefDict['pubchemSid'] = 'http://pubchem.ncbi.nlm.nih.gov/summary/summary.cgi?sid='
            hrefDict['knapsackId'] = 'http://kanaya.naist.jp/knapsack_jsp/information.jsp?sname=C_ID&word='

            aList = soup.find_all('a')
            for a in aList:
                href = str(a.get('href'))
                for k,h in hrefDict.iteritems():
                    if h in href:
                        datum[k] = href.strip(h)
        
            if 'knapsackId' in datum.keys():
                datum['knapsackId'] = 'C'+datum['knapsackId']        

            divList = soup.find_all('div')
            for d in divList:
                v = str(d.get('style'))
                if 'margin-left:3em' in v:
                    d = str(d).strip('<div style="margin-left:3em">').strip('</div>')
                    datum['casId'] = d

        data[idStr] = datum

        if ((i+1)%100)==0 or i==(n-1):
            jsonFpath = baseDir+'/kegg_compound_data_'+str(now.date())+'_'+str(now.time())+'.json'
            with open(jsonFpath, 'w') as f:
                json.dump(data, f, indent=2, sort_keys=True)

            pklFpath = baseDir+'/kegg_compound_data_'+str(now.date())+'_'+str(now.time())+'.pkl'
            with open(pklFpath, 'wb') as f:
                pickle.dump(data, f)

    return data

if __name__ == '__main__':
    main(sys.argv)
    db.close()

