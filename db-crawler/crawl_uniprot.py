# test2.py

import time
import json
import MySQLdb
from collections import defaultdict

def main():
    proteinDiseaseDict, proteinList, diseaseList = parseUniprotData()
    # insertDisease(diseaseList)
    # insertProtein(proteinList)
    insertProteinVsDisease(proteinDiseaseDict)

def insertProteinVsDisease(proteinDiseaseDict):
    db = MySQLdb.connect("localhost","root","123","ijah" )
    cursor = db.cursor()

    idx = 0
    for i,v in proteinDiseaseDict.iteritems():
        idx += 1
        print 'inserting i=', str(idx), 'of', str(len(proteinDiseaseDict))

        qf = 'SELECT pro_id FROM protein WHERE pro_uniprot_abbrv ='
        qm = '"' + i + '"'
        qr = ''
        sql = qf+qm+qr

        try:
            cursor.execute(sql)
            db.commit()
        except:
            assert False, 'dbErr'
            db.rollback()
        proId = cursor.fetchone()[0]
        proId = '"'+proId+'"'
        
        for i in v['disease']:
            qf = 'SELECT dis_id FROM disease WHERE dis_omim_id ='
            qm = '"' + i[2] + '"'
            qr = ''
            sql = qf+qm+qr

            try:
                cursor.execute(sql)
                db.commit()
            except:
                assert False, 'dbErr'
                db.rollback()
            disId = cursor.fetchone()[0]
            disId = '"'+disId+'"'

            #
            qf = 'INSERT INTO protein_vs_disease (pro_id,dis_id) VALUES ('
            qm = proId+','+disId
            qr = ')'
            sql = qf+qm+qr

            try:
                cursor.execute(sql)
                db.commit()
            except:
                assert False, 'dbErr'
                db.rollback()

    db.close()

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
    path = '/home/tor/robotics/prj/csipb-jamu-prj/dataset/uniprot/uniprot_human_dat_20160928/uniprot_sprot_human.dat'
    outDir = '/home/tor/robotics/prj/csipb-jamu-prj/dataset/uniprot/uniprot_human_dat_20160928'

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
    
    with open(outDir+'/uniprot_sprot_human.json', 'w') as fp:
        json.dump(data2, fp, indent=2, sort_keys=True)

    return (data2, proteinList, diseaseList)
    
if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
