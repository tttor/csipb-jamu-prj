#!/usr/bin/env python

import time
from blm_core import BLM

def main():
    fpath = '/home/tor/robotics/prj/csipb-jamu-prj/dataset/yamanishi/ground-truth/bind_orfhsa_drug_nr.txt'
    blm = BLM(fpath)
    blm.eval()

if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
