# insert_plant.py
import os
import sys
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

def main(argv):
    assert len(argv)==1
    fpath = argv[1] #e.g.: knapsack_jsp_plant_vs_compound.pkl'
    plantCompoundDict = None
    with open(fpath, 'rb') as handle:
        plantCompoundDict = pickle.load(handle)

    insertPlants(plantCompoundDict.keys())

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

if __name__ == '__main__':
    start_time = time.time()
    main(sys.argv)
    print("--- %s seconds ---" % (time.time() - start_time))
