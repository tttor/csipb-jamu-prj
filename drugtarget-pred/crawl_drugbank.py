# crawl_drugbank.py

import time
import MySQLdb
from collections import defaultdict

db = MySQLdb.connect("localhost","root","123","ijah" )
cursor = db.cursor()

def main():
    drugProteinDict = parseDrugbank() 
    insertDrug(drugProteinDict)
    insertCompoundVsProtein(drugProteinDict)
    db.close()

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

def insertDrug(drugProteinDict):
    idx = 0
    for i,v in drugProteinDict.iteritems():
        idx += 1
        print 'inserting idx=',str(idx),'of', str(len(drugProteinDict))
        
        comId = str(idx)
        comId = comId.zfill(8)
        comId = '"'+'COM'+comId+'"'
        comName = '"'+v['name']+'"'
        comDrugbankId = '"'+i+'"'
        qf = 'INSERT INTO compound (com_id,com_drugbank_id,com_name) VALUES ('
        qm = comId+','+comDrugbankId+','+comName
        qr = ')'
        sql = qf+qm+qr
        # print sql

        try:
            cursor.execute(sql)
            db.commit()
        except:
            assert False, 'dbErr'
            db.rollback()

def parseDrugbank():
    dpFpath = '/home/tor/robotics/prj/csipb-jamu-prj/dataset/drugbank/durgbank_20161002/uniprot_links.csv'

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
    
    return drugProteinDict

if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
