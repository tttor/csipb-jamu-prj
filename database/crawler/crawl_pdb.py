# crawl_pdb.py
import json
import pickle
from collections import defaultdict

def main():
    parse_pdbsws_chain()

def parse_pdbsws_chain():
    fpath = '/home/tor/robotics/prj/csipb-jamu-prj/dataset/pdb/27Nov2016/pdb_uniprot_chain_map.lst.2'
    fpathOut = '/home/tor/robotics/prj/csipb-jamu-prj/dataset/pdb/27Nov2016/uniprot2pdb.json'
    fpathOut2 = '/home/tor/robotics/prj/csipb-jamu-prj/dataset/pdb/27Nov2016/uniprot2pdb.pkl'
    uniprot2pdb = defaultdict(list)

    with open(fpath,'r') as f:
        for line in f:
            line = line.strip()
            words = line.split()

            if len(words)!=3:
                continue
            if words[2]=='?':
                continue

            pdb = words[0]
            uniprot = words[2]

            uniprot2pdb[uniprot].append(pdb)

    for k,v in uniprot2pdb.iteritems():
        uniprot2pdb[k] = list(set(v))

    # print len(uniprot2pdb)
    with open(fpathOut,'w') as f:
        json.dump(uniprot2pdb, f, indent=2, sort_keys=True)

    with open(fpathOut2,'w') as f:
        pickle.dump(uniprot2pdb,f)

if __name__ == '__main__':
    main()
