#!/usr/bin/env python

from blm_core import BLM

def main():
    fpath = '/home/tor/robotics/prj/csipb-jamu-prj/dataset/yamanishi/ground-truth/bind_orfhsa_drug_e.txt'
    blm = BLM(fpath)
    blm.run()

if __name__ == '__main__':
    main()
