#!/usr/bin/env python

import time
from blm_core import BLM

def main():
    fpath = '/home/tor/jamu/dataset/yamanishi/ground-truth/bind_orfhsa_drug_nr.txt'
    proteinKernelFpath = '/home/tor/jamu/dataset/yamanishi/similarity-mat/protein/nr_simmat_dg.txt'
    drugKernelFpath = '/home/tor/jamu/dataset/yamanishi/similarity-mat/compound/nr_simmat_dc.txt'
    outDir = '/home/tor/jamu/xprmt/drugtarget-pred'

    blm = BLM(fpath, drugKernelFpath, proteinKernelFpath)
    blm.eval(outDir)

if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
