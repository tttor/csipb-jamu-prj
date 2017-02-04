#!/usr/bin/env python

def loadYamanishi(fpath):
    with open(fpath) as f:
        content = f.readlines()

    drugList = []
    proteinList = []
    for c in content:
        tmp = [i.strip() for i in c.split()]
        proteinList.append(tmp[0])
        drugList.append(tmp[1])

    drugSet = set(drugList)
    proteinSet = set(proteinList)
        
    print(len(content))
    print(len(drugSet))
    print(len(proteinSet))

def main():
    loadYamanishi('/home/tor/robotics/prj/csipb-jamu-prj/dataset/yamanishi/ground-truth/bind_orfhsa_drug_e.txt')

if __name__ == '__main__':
    main()
