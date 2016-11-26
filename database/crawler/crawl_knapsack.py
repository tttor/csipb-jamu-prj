import time
import json
import sys
import yaml
import MySQLdb
import pickle
import dbcrawler_util as util
from collections import defaultdict
from bs4 import BeautifulSoup
from urllib2 import urlopen
from datetime import datetime

def main(argv):
    '''
    arg[1]: outDir
    arg[2:]: seedPlantListFPaths, e.g. ijah_jamu_plants.lst
    '''
    assert len(argv)>=3

    outDir = argv[1]
    seedPlantListFPaths = argv[2:]
    parseKnapsack(seedPlantListFPaths, outDir)

def parseKnapsack(seedPlantListFPaths, outDir):
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

                    existingCom = [ c[0] for c in plantCompoundDict[plantName]]
                    if comKnapsackId not in existingCom:
                        plantCompoundDict[plantName].append( compoundDatum )

    jsonFpath = outDir+'/knapsack_jsp_plant_vs_compound_'+str(now.date())+'_'+str(now.time())+'.json'
    with open(jsonFpath, 'w') as f:
        json.dump(plantCompoundDict, f, indent=2, sort_keys=True)

    pklFpath = outDir+'/knapsack_jsp_plant_vs_compound_'+str(now.date())+'_'+str(now.time())+'.pkl'
    with open(pklFpath, 'wb') as f:
        pickle.dump(plantCompoundDict, f)

    return plantCompoundDict

if __name__ == '__main__':
    start_time = time.time()
    main(sys.argv)
    print("--- %s seconds ---" % (time.time() - start_time))
