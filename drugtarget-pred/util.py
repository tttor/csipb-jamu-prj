#!/usr/bin/env python3

def loadYamanishi(fpath):
    with open(fpath) as f:
        content = f.readlines()

    for c in content:
        tmp = c.split()
        
    print(len(content))
    print(content[1])

def main():
    loadYamanishi('/home/tor/robotics/prj/csipb-jamu-prj/dataset/yamanishi/ground-truth/bind_orfhsa_drug_e.txt')

if __name__ == '__main__':
    main()
