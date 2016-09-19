#!/usr/bin/env python

import time
import sys
from blm_core import BLM

def main(argv):
    interactionFpath = argv[1]
    drugKernelFpath = argv[2]
    proteinKernelFpath = argv[3]
    outDir = argv[4]

    blm = BLM(interactionFpath, drugKernelFpath, proteinKernelFpath)
    blm.eval(outDir)

if __name__ == '__main__':
    start_time = time.time()
    main(sys.argv)
    print("--- %s seconds ---" % (time.time() - start_time))
