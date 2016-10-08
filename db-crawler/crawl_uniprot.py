# test2.py

import time
import json
import MySQLdb
import dbcrawler_util as util
from collections import defaultdict

dirPath = '/home/tor/robotics/prj/csipb-jamu-prj/dataset/uniprot/uniprot_human_dat_20160928'
db = MySQLdb.connect("localhost","root","123","ijah" )
cursor = db.cursor()

def main():
    proteinDiseaseDict, proteinList, diseaseList = parseUniprotData()
    # insertDisease(diseaseList)
    # insertProtein(proteinList)
    insertProteinVsDisease(proteinDiseaseDict)

    db.close()

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
            msg = 'inserting '+ p+ ' vs '+ d+ 'idx= '+ str(idx)+ ' of '+ str(n)
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

def insertProtein(proteinList):
    db = MySQLdb.connect("localhost","root","123","ijah" )
    cursor = db.cursor()

    for i,p in enumerate(proteinList):
        proId = str(i+1)
        proId = proId.zfill(8)
        proId = 'PRO'+proId
        print 'inserting ', proId, 'of', str(len(proteinList))

        proName, proUniprotId, proUniprotAbbrv = p
        pro = [proId, proName, proUniprotId, proUniprotAbbrv]
        pro = ['"'+i+'"' for i in pro]

        # Prepare SQL query to INSERT a record into the database.
        qf = 'INSERT INTO protein (pro_id,pro_name,pro_uniprot_id,pro_uniprot_abbrv) VALUES ('
        qm = pro[0]+','+pro[1]+','+pro[2]+','+pro[3]
        qr = ')'
        sql = qf+qm+qr
        # print sql

        try:
            cursor.execute(sql)
            db.commit()
        except:
            assert False, 'dbErr'
            db.rollback()

    db.close()

def insertDisease(diseaseList):
    #
    db = MySQLdb.connect("localhost","root","123","ijah" )
    cursor = db.cursor()

    for i,d in enumerate(diseaseList):
        disId = str(i+1)
        disId = disId.zfill(8)
        disId = 'DIS'+disId
        print 'inserting ', disId, 'of', str(len(diseaseList))

        disName, disAbbrv, disOmimId = d
        dis = [disId,disName,disOmimId,disAbbrv]
        dis = ['"'+i+'"' for i in dis]

        # Prepare SQL query to INSERT a record into the database.
        qf = 'INSERT INTO disease (dis_id,dis_name,dis_omim_id,dis_uniprot_abbrv) VALUES ('
        qm = dis[0]+','+dis[1]+','+dis[2]+','+dis[3]
        qr = ')'
        sql = qf+qm+qr
        # print sql

        try:
            cursor.execute(sql)
            db.commit()
        except:
            assert False, 'dbErr'
            db.rollback()

    db.close()

def parseUniprotData():
    path = dirPath+'/uniprot_sprot_human.dat'
    
    data = dict()
    with open(path) as infile:
        hot = None
        diseaseStr = ''
        diseaseStrComplete = True

        for line in infile:
            words = line.split()

            h = words[0]
            if h=='ID': 
                hot = words[1]
                data[hot] = defaultdict(list)
            elif h=='AC':
                if len(data[hot]['access'])==0:
                    ac = words[1].replace(';','')
                    data[hot]['access'] = ac
            elif h=='DE':
                if len(data[hot]['name'])==0:
                    if words[1]=='RecName:':
                        del words[0]; del words[0]
                        name = ' '.join(words)
                        name = name.replace(';','')
                        name = name.replace('Full=','')
                        _ = name.find('{')
                        if _!=-1:
                            name = name[0:_]; name = name.strip()
                        data[hot]['name'] = name
            elif h=='CC':
                if words[1]=='-!-' and words[2]=='DISEASE:':
                    del words[0]; del words[0]; del words[0]
                    diseaseStr = ' '.join(words)
                    if 'Note=' in diseaseStr or 'May be involved' in diseaseStr:
                        diseaseStr = ''
                        diseaseStrComplete = True
                    else:
                        diseaseStrComplete = False
                elif not(diseaseStrComplete):
                    del words[0]
                    diseaseStr += ' '.join(words)
                
                if len(diseaseStr)!=0 and not(diseaseStrComplete):
                    mimIdx = diseaseStr.find('[MIM:')
                    if mimIdx!=-1:
                        mimStr = diseaseStr[mimIdx+5:]
                        mimStr = mimStr.split()[0]
                        mimStr = mimStr.replace(']:','')

                        diseaseStr = diseaseStr[0:mimIdx].strip()                        
                        abbIdx = diseaseStr.find('('); assert abbIdx!=-1
                        abbStr = diseaseStr[abbIdx+1:-2]
                        diseaseStr = diseaseStr[0:abbIdx].strip()

                        data[hot]['disease'].append( (diseaseStr,abbStr,mimStr) )
                        diseaseStrComplete = True
                        diseaseStr = ''

    data2 = dict()
    diseaseList = []
    proteinList = []
    for i,v in data.iteritems():
        if 'disease' in v.keys():
            data2[i] = v
            diseaseList += v['disease']

            p = (v['name'], v['access'], i)
            proteinList.append(p)

    diseaseList = list(set(diseaseList))
    assert(len(proteinList)==len(data2))
    
    with open(dirPath+'/uniprot_sprot_human.json', 'w') as fp:
        json.dump(data2, fp, indent=2, sort_keys=True)

    return (data2, proteinList, diseaseList)
    
if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
