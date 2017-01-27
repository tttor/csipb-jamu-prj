# crawl_plantlist.py
import glob
import time
import json
import datetime
import yaml
from urllib2 import urlopen
from bs4 import BeautifulSoup

def main():
    # dirpath = '/home/tor/robotics/prj/csipb-jamu-prj/dataset/plant-list'
    # parseMiscPlantList(dirpath)

    latin2idr = None
    with open('/home/tor/robotics/prj/csipb-jamu-prj/dataset/plant-list/misc/latin2idr_20170118-114630.json','r') as f:
        latin2idr = yaml.load(f)

    list2 = parseHerbalisnusantara()
    print list2

    existingIdrNames = ' '.join( latin2idr.values() )
    list3 = []
    for i in list2:
        if i.capitalize() not in existingIdrNames:
            list3.append(i)
    print list3
    print len(list3)

def parseHerbalisnusantara():
    baseURL = 'http://www.herbalisnusantara.com/obatherbal/'
    ##
    html = None

    url = baseURL+'index.html'
    html = urlopen(url).read()

    # url = '/home/tor/robotics/prj/csipb-jamu-prj/dataset/plant-list/herbalisnusantara.html'
    # with open(url,'r') as f:
    #     html = f.read()

    ##
    soup = BeautifulSoup(html, "lxml")
    # with open('soup.html','w') as f:
    #     f.write( soup.prettify().encode('utf-8').strip() )

    ##
    atags = [i for i in soup.find_all('a') if 'view' in i.get('href')];
    hrefs = [i.get('href') for i in atags]
    names = [i.getText() for i in atags]
    names = [i.replace('\n','') for i in names]
    names2 = []
    for n in names:
        _ = n.split()
        nn = [i.encode('utf-8').strip() for i in _ if len(i)!=0]
        names2.append(' '.join(nn))
    names = list(set(names2[:]))
    names = [n.capitalize() for n in names]

    for h in hrefs:
        html2 = None

        url2 = baseURL+h
        html2 = urlopen(url2).read()

        # url2 = '/home/tor/robotics/prj/csipb-jamu-prj/dataset/plant-list/herbalisnusantara/herbalisnusantara_jahe.html'
        # with open(url2,'r') as f:
        #     html2 = f.read()

        print url2

        soup2 = BeautifulSoup(html2, "lxml")
        itags = soup2.find_all('td')
        # ttt = [i.getText() for i in itags]
        # for t in ttt:
        #     print t
        # itags = [i.encode('utf-8').strip() for i in itags]
        itags = [str(i) for i in itags]
        itags = [i for i in itags if '/blockquote' in i]
        itags = [i for i in itags if '(' in i and ')' in i]

        # for i in itags:
        #     s = BeautifulSoup(i, "lxml")
        #     ss = s.find_all('td')
        #     for j in ss:
        #         print j.getText()
        break

    # print hrefs
    return names

def parseMiscPlantList(dirpath):
    latin2idr = {}
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    idrSeparator = '/'

    fpathList = glob.glob(dirpath+"/*.list")
    for fpath in fpathList:
        with open(fpath,'r') as f:
            for line in f:
                line = line.strip()
                print line, 'at', fpath
                comps = line.split('=')
                comps = [c.strip().lower() for c in comps]
                assert len(comps)==2

                idr = comps[0]
                latin = comps[1]

                # condition the idr
                # sanity check
                idr = idr.replace('atau',',')
                idr = idr.replace('/',',')
                idr = idr.replace('(',',')
                idr = idr.replace(')','')

                idrWords = idr.split(' ')
                idrWords = [w.strip().lower() for w in idrWords]
                idrWords = [w for w in idrWords if (len(w)!=0)]
                idr = ' '.join(idrWords)

                idrComps = idr.split(',')
                idrComps = [i.strip().capitalize() for i in idrComps if ',' not in i]
                idrComps = [c for c in idrComps if (len(c)!=0)]
                idr = idrSeparator.join(idrComps)

                if (len(idr))==0:
                    continue

                # condition the latin
                # get only the 2 first latin words
                latinWords = latin.split(' ')
                latinWords = [w.strip().lower() for w in latinWords if len(w)!=0]
                if len(latinWords)<2:
                    continue # because only the family name
                latin = ' '.join(latinWords[0:2])
                latin = latin.capitalize()
                if (len(latin)<2):
                    continue;

                # Put in the dict
                if (latin in latin2idr):
                    if idr not in latin2idr[latin]:
                        latin2idr[latin] += (idrSeparator+idr)
                else:
                    latin2idr[latin] = idr

    with open(dirpath+'/latin2idr_'+timestamp+'.json', 'w') as fp:
        json.dump(latin2idr, fp, indent=2, sort_keys=True)

if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
