#!/usr/bin/env python

import time
import sys
import os
from blm_core import BLM
from datetime import datetime

def main(argv):
    assert len(argv)==7
    interactionFpath = argv[1]
    drugKernelFpath = argv[2]
    proteinKernelFpath = argv[3]

    outDir = argv[4]
    xprmtType = argv[5]
    dataset = argv[6]

    t = datetime.now().time()
    d = datetime.now().date()
    outDir = outDir+'/xprmt-'+dataset+'-'+xprmtType+'_'+str(d)+'-'+str(t)

    if not os.path.exists(outDir):
        os.makedirs(outDir)

    blm = BLM(interactionFpath, drugKernelFpath, proteinKernelFpath)
    blm.eval(xprmtType, outDir)

if __name__ == '__main__':
    start_time = time.time()
    main(sys.argv)
    print("--- %s seconds ---" % (time.time() - start_time))
