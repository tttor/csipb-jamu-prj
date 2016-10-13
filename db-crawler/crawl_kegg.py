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

def main(argv):
    # lo = int(argv[1]); hi = int(argv[2])
    # parseCompoundWebpage(lo,hi)

    # fpath = baseDir+'/drug'
    # parseDrugFile(fpath)

    parseSimcomp()

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

def parseSimcomp():
    # http://www.genome.jp/tools/gn_tools_api.html
    # url = 'http://rest.genome.jp/simcomp/C00022/compound/cutoff=0.1'
    baseURL = 'http://rest.genome.jp/simcomp/'
    database = 'compound' # KEGG compunds

    outDir = baseDir+'/simcomp'
    if not os.path.exists(outDir):
        os.makedirs(outDir)

    # ideally: cutoff is 7-decimal digit as kegg outputs up to 6 decimal digits
    # (but float to string uses scientific notation for more than 4 digits)
    cutoff = 0.0001

    # Get all valid keggComID
    fpath = baseDir+'/keggComData_validComId.lst'
    with open(fpath) as infile:
        for line in infile:
            keggId = line.strip()
            url = baseURL+keggId+'/'+database+'/cutoff='+str(cutoff)
            print url

            html = None
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

            if html==None:
                continue

            soup = bs(html,'html.parser')
            words = str(soup).split(); assert len(words)%2==0

            simcomp = []
            for i,keggId2 in enumerate(words):
                if i%2==0:
                    target = words[i]
                    score = words[i+1]
                    simcomp.append( target+'='+score )

            fpath = outDir+'/simcomp_'+keggId
            with open(fpath,'w') as f:
                for s in simcomp:
                    f.write(str(s)+'\n')

if __name__ == '__main__':
    main(sys.argv)
