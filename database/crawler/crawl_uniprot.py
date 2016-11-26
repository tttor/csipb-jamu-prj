import time
import json
import pickle
from collections import defaultdict

dirPath = '/home/tor/robotics/prj/csipb-jamu-prj/dataset/uniprot/uniprot_human_dat_20160928'

def main():
    parseUniprotData()

def parseUniprotData():
    path = dirPath+'/uniprot_sprot_human.dat'

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

    with open(dirPath+'/uniprot_sprot_human.pkl', 'wb') as f:
        pickle.dump(data2, f)
    with open(dirPath+'/uniprot_sprot_human.json', 'w') as fp:
        json.dump(data2, fp, indent=2, sort_keys=True)

    with open(dirPath+'/uniprot_sprot_human_protein.pkl', 'wb') as f:
        pickle.dump(proteinList, f)
    with open(dirPath+'/uniprot_sprot_human_protein.lst', 'w') as fp:
        for p in proteinList: fp.write(str(p)+'\n')

    with open(dirPath+'/uniprot_sprot_human_disease.pkl', 'wb') as f:
        pickle.dump(diseaseList, f)
    with open(dirPath+'/uniprot_sprot_human_disease.lst', 'w') as fp:
        for d in diseaseList: fp.write(str(d)+'\n')

if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
