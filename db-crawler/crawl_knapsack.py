import time
import json
import MySQLdb
from collections import defaultdict
from bs4 import BeautifulSoup
from urllib2 import urlopen

db = MySQLdb.connect("localhost","root","123","ijah" )
cursor = db.cursor()

outDir = '/home/tor/robotics/prj/csipb-jamu-prj/dataset/knapsack/20161003'

def main():
    parseKnapsack()
    # insertPlants()
    # insertCompounds()
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

            if len(datum)!=0:
                comKnapsackId = datum[0]
                comCasId = datum[1]
                comName = datum[2]
                comFormula = datum[3]
                plantName = datum[5]

                compoundDatum = ( comCasId, comName, comFormula )
                plantCompoundDict[plantName].append( compoundDatum )

    with open(outDir+'/knapsack_jsp_plant_vs_compound.json', 'w') as fp:
        json.dump(plantCompoundDict, fp, indent=2, sort_keys=True)

    return plantCompoundDict

# def insertPlants(plantList):
#     for idx, p in enumerate(plantList):
#         plaId = 
#         qf = 'INSERT INTO plant (pla_id,pla_name) VALUES ('
#         qm = plaId+','+plaName
#         qr = ')'
#         sql = qf+qm+qr
#         # print sql

#         try:
#             cursor.execute(sql)
#             db.commit()
#         except:
#             assert False, 'dbErr'
#             db.rollback()

# def insertCompound():

# def insertPlantVsCompound():
#     pass

if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))