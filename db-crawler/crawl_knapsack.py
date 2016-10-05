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
    #################
    plantCompoundDict = None
    # plantCompoundDict = parseKnapsack()
    fpath = '/home/tor/robotics/prj/csipb-jamu-prj/dataset/knapsack/20161003/knapsack_jsp_plant_vs_compound_2016-10-04_16:34:06.468234.pkl'  
    with open(fpath, 'rb') as handle:
        plantCompoundDict = pickle.load(handle)

    # insertPlants(plantCompoundDict.keys())

    #################
    compoundDict = {}
    for comList in plantCompoundDict.values():
        for kId,cas,name,form in comList:
            compoundDict[kId] = (cas,form)
    insertCompound(compoundDict)

    ################
    # insertPlantVsCompound()
    db.close()

def parseKnapsack():
    # get the seed plant list
    seedPlantListFPaths = ['/home/tor/robotics/prj/csipb-jamu-prj/dataset/knapsack/20161003/ijah_jamu_plants.lst']

    seedPlantList = []
    for fp in seedPlantListFPaths:
        with open(fp) as infile:        
            idx = 0
            for line in infile:
                idx += 1
                print 'parsing idx=', idx, 'of', fp
                line = line.strip()
                words = line.split()

                if len(words)==3:
                    pass
                elif len(words)==4:
                    pass

                name = ' '.join(words)
                seedPlantList.append(name)

    # crawl knapsack
    BASE_URL = 'http://kanaya.naist.jp/knapsack_jsp/result.jsp?sname=organism&word='
    plantCompoundDict = defaultdict(list)
    now = datetime.now()

    for idx,p in enumerate(seedPlantList):
        idx += 1
        print 'crawling idx=', idx, 'of', len(seedPlantList)

        url = BASE_URL + p
        # print 'crawling url=', url

        html = urlopen(url).read()
        soup = BeautifulSoup(html, "lxml")
        table = soup.find("table", "sortable d1")
        table = table.find_all('tr')

        compoundData = dict()
        for i,row in enumerate(table):
            datum = []
            cols = row.find_all('td', 'd1')
            for pos,col in enumerate(cols):
                datum.append(str(col.get_text()))

            if len(datum)==6:
                comKnapsackId = datum[0]
                comCasId = datum[1]
                comName = datum[2]
                comFormula = datum[3]
                plantName = datum[5]
                
                plantNameWords = plantName.split()
                if len(plantNameWords)>1:
                    plantNameWords = plantNameWords[0:2]
                    plantName = ' '.join(plantNameWords)
                    plantName = plantName.capitalize()

                    compoundDatum = ( comKnapsackId, comCasId, comName, comFormula )
                    plantCompoundDict[plantName].append( compoundDatum )

    jsonFpath = outDir+'/knapsack_jsp_plant_vs_compound_'+str(now.date())+'_'+str(now.time())+'.json'
    with open(jsonFpath, 'w') as f:
        json.dump(plantCompoundDict, f, indent=2, sort_keys=True)

    pklFpath = outDir+'/knapsack_jsp_plant_vs_compound_'+str(now.date())+'_'+str(now.time())+'.pkl'
    with open(pklFpath, 'wb') as f:
        pickle.dump(plantCompoundDict, f)

    return plantCompoundDict

def insertPlants(plantList):
    nPlant = len(plantList)
    for idx, p in enumerate(plantList):
        plaId = str(idx+1)
        plaId = plaId.zfill(8)
        plaId = '"'+'PLA'+plaId+'"'
        print 'inserting ', plaId, 'of', str(nPlant)

        plaName = '"'+p+'"'

        qf = 'INSERT INTO plant (pla_id,pla_name) VALUES ('
        qm = plaId+','+plaName
        qr = ')'
        q = qf+qm+qr
        util.mysqlCommit(q)

def insertCompound(compoundDict):
    # get the last of the current comId, after inserting from drugbank
    comIdStr = 'COM00006661'
    comId = int(comIdStr.strip('COM'))

    #
    idx = 0
    nCom = len(compoundDict)
    matchList = []
    for k,v in compoundDict.iteritems():
        idx += 1
        print 'insert/updating', k, 'idx=',str(idx), 'of', nCom

        cas,form = v
        # assert(cas!='' and form!='')
        # assert(cas!='not-available' and form!='not-available')

        qf = 'SELECT * FROM compound WHERE com_cas_id='
        qm = '"'+cas+'"'
        qr = ''
        q = qf+qm+qr
        casMatch = util.mysqlCommit(db, cursor,q)

        qf = 'SELECT * FROM compound WHERE com_formula='
        qm = '"'+form+'"'
        qr = ''
        q = qf+qm+qr
        formMatch = util.mysqlCommit(db, cursor,q)

        if casMatch!=None or formMatch!=None:# match
            matchList.append( (cas,form) )
        else:
            comId += 1
            comIdStr = 'COM'+str(comId).zfill(8)

            insertVals = [comIdStr,cas,form]
            insertVals = ['not-available' if i=='' else i for i in insertVals]
            insertVals = ['"'+i+'"' for i in insertVals]

            qf = 'INSERT INTO compound (com_id,com_cas_id,com_formula) VALUES ('
            qm =','.join(insertVals)
            qr = ')'
            q = qf+qm+qr
            util.mysqlCommit(db,cursor,q)

    fpath = outDir+'/knapsack_compound_match_with_drugbank.lst'
    with open(fpath,'w') as f:
        for m in matchList:
            f.write(s+'\n')

# def insertPlantVsCompound():
#     pass

if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))