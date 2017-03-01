# crawl_pubchem.py
import urllib2 as urllib
import yaml
from bs4 import BeautifulSoup as bs
from time import sleep

def main():
    casListFpath = '../../dataset/metadata/compound/pubchem/com_cas_id_20170103-1606.csv'
    casList = []
    with open(casListFpath,'r') as f:
        for line in f:
            line = line.strip()
            casList.append(line)
    assert len(casList)>0

    ##
    # outdir = '../../dataset/metadata/compound/pubchem/pubchem_properties_20170301-1545/'
    # getCompoundProp(casList,outdir)

    ##
    outdir = '../../dataset/metadata/compound/pubchem/pubchem_synonyms_20170301-1545/'
    getCompoundSynonyms(casList,outdir)

def getCompoundProp(casList,outdir):
    # https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/50-78-2/property/CanonicalSMILES/json
    baseURL = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/'
    outFormat = 'JSON'
    props = 'InChIKey,IUPACName,InChI,CanonicalSMILES,IsomericSMILES'

    logs = []
    for i,cas in enumerate(casList):
        print 'crawling pubchem property: cas= '+cas+' => '+str(i+1)+'/'+str(len(casList))

        url = baseURL+cas+'/property/'+props+'/'+outFormat

        out = None
        success = False
        try:
            out = urllib.urlopen(url)
            success = True
        except urllib.HTTPError, e:
            s = str(i)+': '+cas+' => HTTPError= '+str(e.code)
            logs.append(s)
        except urllib.URLError, e:
            s = str(i)+': '+cas+' => URLError= '+str(e.reason)
            logs.append(s)
        except httplib.HTTPException, e:
            s = str(i)+': '+cas+' => HTTPException'
            logs.append(s)
        except Exception:
            import traceback
            s = str(i)+': '+cas+' => GenericException: '+traceback.format_exc()
            logs.append(s)

        if success:
            txt = bs(out, 'html.parser')
            fname = 'cas_'+cas+'_pubchem_prop.json'
            fpath = outdir+fname
            with open(fpath,'w') as f:
                f.write(str(txt))

        # to not make more than 5 requests per second
        sleep(0.3)

    logFpath = outdir+'pubchem_prop_crawling.log'
    with open(logFpath,'w') as f:
        for l in logs: f.write(l)

def getCompoundSynonyms(casList,outdir):
    # https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/50-78-2/synonyms/JSON
    baseURL = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/'
    outFormat = 'JSON'

    logs = []
    logFpath = outdir+'pubchem_synonyms_crawling.log'

    for i,cas in enumerate(casList):
        print 'crawling pubchem synonyms: cas= '+cas+' => '+str(i+1)+'/'+str(len(casList))

        url = baseURL+cas+'/synonyms/'+outFormat

        out = None
        success = False
        try:
            out = urllib.urlopen(url)
            success = True
        except urllib.HTTPError, e:
            s = str(i)+': '+cas+' => HTTPError= '+str(e.code)
            logs.append(s)
        except urllib.URLError, e:
            s = str(i)+': '+cas+' => URLError= '+str(e.reason)
            logs.append(s)
        except httplib.HTTPException, e:
            s = str(i)+': '+cas+' => HTTPException'
            logs.append(s)
        except Exception:
            import traceback
            s = str(i)+': '+cas+' => GenericException: '+traceback.format_exc()
            logs.append(s)

        if success:
            txt = bs(out, 'html.parser')
            fname = 'cas_'+cas+'_pubchem_synonyms.json'
            fpath = outdir+fname
            with open(fpath,'w') as f:
                f.write(str(txt))

        if (i%100==0) or (i==len(casList)-1):
            with open(logFpath,'w') as f:
                for l in logs: f.write(l)

        # to not make more than 5 requests per second
        sleep(0.3)

if __name__ == '__main__':
    main()
