# crawl_drugbank.py

import time
import pickle
import json
import MySQLdb
import httplib
import urllib2 as urllib
from collections import defaultdict
import dbcrawler_util as util
from datetime import datetime
from bs4 import BeautifulSoup as bs

outDir = '/home/tor/robotics/prj/csipb-jamu-prj/dataset/drugbank/drugbank_20161002'
db = MySQLdb.connect("localhost","root","123","ijah" )
cursor = db.cursor()

def main():
    #########
    # drugProteinDict = parseUniprotlinkFile() # contain drug-protein binding info

    # drugbankIdList = drugProteinDict.keys()
    # drugbankIdList = ['DB01627','DB05101','DB05107','DB08423','DB05127']
    # drugData = parseDrugWebpage(drugbankIdList)
    # drugData = parseSmiles(drugbankIdList)

    # fixDrugData()

    ##########
    fpath = '/home/tor/robotics/prj/csipb-jamu-prj/dataset/drugbank/drugbank_20161002/drugbank_drug_data_2016-10-05_10:16:42.860649.pkl'
    with open(fpath, 'rb') as handle:
        drugData = pickle.load(handle)
    insertDrug(drugData)
    # insertCompoundVsProtein(drugData)

    #
    db.close()

def fixDrugData(): 
    badWords = ['email','class="wrap"','.smiles','href']
    old = None
    smilesDict = None

    fpath = '/home/tor/robotics/prj/csipb-jamu-prj/dataset/drugbank/drugbank_20161002/drugbank_drug_data_2016-10-05_10:16:42.860649.ori.pkl' 
    with open(fpath, 'rb') as handle:
        old = pickle.load(handle)

    fpath = '/home/tor/robotics/prj/csipb-jamu-prj/dataset/drugbank/drugbank_20161002/drugbank_drug_smiles_2016-10-05_12:35:37.724557.pkl' 
    with open(fpath, 'rb') as handle:
        smilesDict = pickle.load(handle)

    nOld = len(old)
    new = old
    idx = 0
    for k,v in old.iteritems():
        idx += 1
        print 'fixing', k, 'idx=', str(idx), 'of', nOld

        if 'SMILES' in v.keys():
            oldSmiles = v['SMILES']
            bad = False
            for b in badWords:
                if b in oldSmiles:
                    bad = True
                    break

            if bad:
                new[k]['SMILES'] = smilesDict[k]
        else:
            new[k]['SMILES'] = smilesDict[k]

        for k2,v2 in v.iteritems():
            for b in badWords:
                if b in v2:
                    new[k][k2] = 'not-available'
    
    assert(len(old)==len(new))
    fpath = '/home/tor/robotics/prj/csipb-jamu-prj/dataset/drugbank/drugbank_20161002/drugbank_drug_data_2016-10-05_10:16:42.860649.pkl' 
    with open(fpath, 'wb') as f:
        pickle.dump(new, f)

    fpath = '/home/tor/robotics/prj/csipb-jamu-prj/dataset/drugbank/drugbank_20161002/drugbank_drug_data_2016-10-05_10:16:42.860649.json' 
    with open(fpath, 'w') as f:
        json.dump(new, f, indent=2, sort_keys=True)

def insertCompoundVsProtein(drugProteinDict):
    idx = 0
    for i,v in drugProteinDict.iteritems():
        idx += 1
        print 'inserting i=', str(idx), 'of', str(len(drugProteinDict))

        qf = 'SELECT com_id FROM compound WHERE com_drugbank_id ='
        qm = '"' + i + '"'
        qr = ''
        sql = qf+qm+qr

        try:
            cursor.execute(sql)
            db.commit()
        except:
            assert False, 'dbErr'
            db.rollback()
        comId = cursor.fetchone()[0]
        comId = '"'+comId+'"'

        for p in v['targetProtein']:
            qf = 'SELECT pro_id FROM protein WHERE pro_uniprot_id ='
            qm = '"' + p + '"'
            qr = ''
            sql = qf+qm+qr
            # print sql

            try:
                cursor.execute(sql)
                db.commit()
            except:
                assert False, 'dbErr'
                db.rollback()

            resp = cursor.fetchone()
            if resp!=None:
                proId = resp[0]
                proId = '"'+proId+'"'

                weight = str(1.0)
                weight = '"'+weight+'"'

                factOrPred = 'fact'
                factOrPred = '"'+factOrPred+'"'                

                #
                qf = 'INSERT INTO compound_vs_protein (com_id,pro_id,weight,type) VALUES ('
                qm = comId+','+proId+','+weight+','+factOrPred
                qr = ')'
                sql = qf+qm+qr

                try:
                    cursor.execute(sql)
                    db.commit()
                except:
                    assert False, 'dbErr'
                    db.rollback()

def insertDrug(drugData):
    idx = 0
    for i,v in drugData.iteritems():
        if len(v['uniprotTargets'])!=0:
            idx += 1
            print 'inserting', i, 'idx=',str(idx),'of at most', str(len(drugData))
            
            comId = str(idx); comId = comId.zfill(8); comId = 'COM'+comId
            comDrugbankId = i
            na = 'not-available'
            
            insertVals = []
            insertVals.append(comId)
            insertVals.append(comDrugbankId)

            insertKeys = ['CAS number', 'pubchemCid', 'InChI Key', 'Chemical Formula', 
                          'SMILES','com_knapsack_id','com_kegg_id']
            for k in insertKeys:
                if k in v.keys():
                    insertVals.append(v[k])
                else:
                    insertVals.append(na)

            assert len(insertVals)==9
            insertVals = ['"'+iv+'"' for iv in insertVals ]

            qf = '''INSERT INTO compound (com_id,com_drugbank_id,
                                          com_cas_id,com_pubchem_id, 
                                          com_inchikey, com_formula, com_smiles,
                                          com_knapsack_id, com_kegg_id)
                 VALUES ('''
            qm = ','.join(insertVals)
            qr = ')'
            sql = qf+qm+qr
            # print sql

            util.mysqlCommit(db, cursor, sql)

def parseUniprotlinkFile():
    dpFpath = '/home/tor/robotics/prj/csipb-jamu-prj/dataset/drugbank/drugbank_20161002/uniprot_links.csv'

    now = datetime.now()
    drugProteinDict = dict()
    idx = 0
    with open(dpFpath) as infile:        
        first = True
        hot = ''
        for line in infile:
            if not(first):
                idx += 1
                print 'parsing idx=', idx
                
                line = line.strip();
                quoteIdx = [i for i,c in enumerate(line) if c=='"']; assert(len(quoteIdx)%2==0)
                quoteIdx = [j for i,j in enumerate(quoteIdx) if i%2==0] # take only odd-indexed idx
                
                words = line.split('"')
                words2 = []
                for w in words:
                    i = line.find(w) # just after an opening quote
                    w2 = w
                    if (i-1) in quoteIdx:
                        w2 = w.replace(',','$')
                    if len(w2)!=0:
                        words2.append(w2)
                line = ' '.join(words2)

                words = line.split(','); 
                words = words[0:4]
                words = [w.strip() for w in words]
                words = [w.replace('$',',') for w in words]
                
                drugbankId = words[0]
                name = words[1]
                uniprotId = words[3]

                if hot != drugbankId:
                    hot = drugbankId
                    drugProteinDict[hot] = defaultdict(list)

                if len(drugProteinDict[hot]['name'])==0:
                    drugProteinDict[hot]['name'] = name

                drugProteinDict[hot]['targetProtein'].append(uniprotId)
            first = False
    
    jsonFpath = outDir+'/drugbank_drug_vs_protein_'+str(now.date())+'_'+str(now.time())+'.json'
    with open(jsonFpath, 'w') as f:
        json.dump(drugProteinDict, f, indent=2, sort_keys=True)

    pklFpath = outDir+'/drugbank_drug_vs_protein_'+str(now.date())+'_'+str(now.time())+'.pkl'
    with open(pklFpath, 'wb') as f:
        pickle.dump(drugProteinDict, f)

    return drugProteinDict

def parseDrugWebpage(drugbankIdList): # e.g. http://www.drugbank.ca/drugs/DB05107
    html = None
    comData = dict()
    now = datetime.now()

    nDbId = len(drugbankIdList)
    for idx, dbId in enumerate(drugbankIdList):
        print 'parsing', dbId, 'idx=', str(idx+1), 'of', str(nDbId)

        baseURL = 'http://www.drugbank.ca/drugs/'
        url = baseURL+dbId
        html = urllib.urlopen(url)
        # baseFpath = '/home/tor/robotics/prj/csipb-jamu-prj/dataset/drugbank/drugbank_20161002/' 
        # fpath = baseFpath+dbId+ '.html'
        # with open(fpath, 'r') as content_file:
        #     html = content_file.read()

        #
        soup = bs(html, 'html.parser')

        #
        datum = defaultdict(list)
        # datum['name'] = str(soup.title.string).split()[1].strip()

        trList = soup.find_all('tr')
        for tr in trList:
            trStr = str(tr)
            keys = ['InChI Key','CAS number','Chemical Formula','SMILES']

            for k in keys:
                if (k in trStr)and('.smiles' not in trStr)and('class="wrap"' not in trStr)and('href' not in trStr):
                    trStr = trStr.split('<td>')[1].replace('</td></tr>','')
                    trStr = trStr.replace('InChIKey=','')
                    trStr = trStr.replace('<div class="wrap">','').replace('</div>','')
                    trStr = trStr.replace('<sub>','').replace('</sub>','')

                    if ('wishart-not-available' in trStr) or trStr=='':
                        trStr = 'not-available'

                    # print trStr
                    datum[k] = trStr

        aList = soup.find_all('a')
        cidBaseUrl = 'http://pubchem.ncbi.nlm.nih.gov/summary/summary.cgi?cid='
        sidBaseUrl = 'http://pubchem.ncbi.nlm.nih.gov/summary/summary.cgi?sid='
        chemspiderBaseUrl = 'http://www.chemspider.com/Chemical-Structure.'
        uniprotBaseUrl = 'http://www.uniprot.org/uniprot/'
        for a in aList:
            href = str(a.get('href'))
            if cidBaseUrl in href:
                datum['pubchemCid']= str(a.get('href').strip(cidBaseUrl))
            elif sidBaseUrl in href:
                datum['pubchemSid']= str(a.get('href').strip(sidBaseUrl))
            elif chemspiderBaseUrl in href:
                datum['chemspiderId'] = str(a.get('href').strip(chemspiderBaseUrl).strip('.html'))
            elif uniprotBaseUrl in href:
                datum['uniprotTargets'].append( str(a.get('href').strip(uniprotBaseUrl)) )

        comData[dbId] = datum

        if ((idx+1)%100)==0 or idx==(nDbId-1):
            jsonFpath = outDir+'/drugbank_drug_data_'+str(now.date())+'_'+str(now.time())+'.json'
            with open(jsonFpath, 'w') as f:
                json.dump(comData, f, indent=2, sort_keys=True)

            pklFpath = outDir+'/drugbank_drug_data_'+str(now.date())+'_'+str(now.time())+'.pkl'
            with open(pklFpath, 'wb') as f:
                pickle.dump(comData, f)

    return comData

def parseSmiles(drugbankIdList):
    now = datetime.now()
    nDbId = len(drugbankIdList)
    baseURL = 'http://www.drugbank.ca/structures/structures/small_molecule_drugs/'

    smiles = dict() 
    for idx, dbId in enumerate(drugbankIdList):
        print 'parsing', dbId, 'idx=', str(idx+1), 'of', str(nDbId)

        s = 'not-available'
        url = baseURL+dbId+'.smiles'
        try: 
            s = urllib.urlopen(url)
        except urllib.HTTPError, e:
            print('HTTPError = ' + str(e.code))
        except urllib.URLError, e:
            print('URLError = ' + str(e.reason))
        except httplib.HTTPException, e:
            print('HTTPException')
        except Exception:
            import traceback
            print('generic exception: ' + traceback.format_exc())

        s = bs(s, 'html.parser')
        smiles[dbId] = str(s)

        if ((idx+1)%100)==0 or idx==(nDbId-1):
            jsonFpath = outDir+'/drugbank_drug_smiles_'+str(now.date())+'_'+str(now.time())+'.json'
            with open(jsonFpath, 'w') as f:
                json.dump(smiles, f, indent=2, sort_keys=True)

            pklFpath = outDir+'/drugbank_drug_smiles_'+str(now.date())+'_'+str(now.time())+'.pkl'
            with open(pklFpath, 'wb') as f:
                pickle.dump(smiles, f)

    # print smiles
    return smiles

# def parseDrugbankVocab():
#     fpath = '/home/tor/robotics/prj/csipb-jamu-prj/dataset/drugbank/drugbank_20161002/drugbank_vocabulary.csv'

#     with open(fpath) as infile:      
#         first = True
#         idx = 0
#         for line in infile:
#             if not(first):
#                 idx += 1
#                 print 'updating idx=', idx

#                 line = line.strip()
#                 words = line.split(',')
#                 words = words[0:4]

#                 drugbankId = words[0]
#                 cas = words[3]
#                 cas = cas.replace('"','')

#                 if len(cas)!=0 and len(drugbankId)!=0:
#                     drugbankId = '"'+drugbankId+'"'
#                     cas = '"'+cas+'"'

#                     qf = 'UPDATE compound SET '
#                     qm = 'com_cas_id='+cas
#                     qr = ' WHERE com_drugbank_id='+drugbankId
#                     q = qf+qm+qr
#                     # print q

#                     util.mysqlCommit(db, cursor, q)

#             first = False

if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
