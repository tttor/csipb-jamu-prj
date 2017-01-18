# crawl_plantlist.py
import glob
import time
import json
import datetime

def main():
    dirpath = '/home/tor/robotics/prj/csipb-jamu-prj/dataset/plant-list'
    parsePlaList(dirpath)

def parsePlaList(dirpath):
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
