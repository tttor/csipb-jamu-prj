# crawl_kegg.py
import time
import pickle
import json
import sys
import MySQLdb
import httplib
import urllib2 as urllib
from collections import defaultdict
import dbcrawler_util as util
from datetime import datetime
from bs4 import BeautifulSoup as bs

baseDir = '/home/tor/robotics/prj/csipb-jamu-prj/dataset/kegg/kegg_20161010'

def main(argv):
    lo = int(argv[1]); hi = int(argv[2])
    parseCompoundWebpage(lo,hi)

def parseCompoundWebpage(loIdx, hiIdx):
    baseFpath = '/home/tor/robotics/prj/csipb-jamu-prj/dataset/kegg/kegg_20161010/'
    baseURL = 'http://www.genome.jp/dbget-bin/www_bget?cpd:'
    now = datetime.now()
    n = hiIdx - loIdx

    data = {}
    for i,j in enumerate(range(loIdx,hiIdx)):
        msg = 'parsing i= '+ str(i+1)+ '/'+ str(n)
        idStr = 'C'+str(j).zfill(5)

        url = baseURL+idStr
        html = urllib.urlopen(url)
        msg = msg + ' from '+ url

        # fpath = baseFpath+idStr+ '.html'
        # with open(fpath, 'r') as content_file:
        #     html = content_file.read()
        # msg = msg + ' from '+ fpath

        print msg
        soup = bs(html,'html.parser')
        datum = {}
        
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

        if ((i+1)%10)==0 or i==(n-1):
            jsonFpath = baseDir+'/kegg_compound_data_'+str(now.date())+'_'+str(now.time())+'.json'
            with open(jsonFpath, 'w') as f:
                json.dump(data, f, indent=2, sort_keys=True)

            pklFpath = baseDir+'/kegg_compound_data_'+str(now.date())+'_'+str(now.time())+'.pkl'
            with open(pklFpath, 'wb') as f:
                pickle.dump(data, f)

    return data

if __name__ == '__main__':
    main(sys.argv)
