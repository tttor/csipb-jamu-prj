import util
import time
import sys
import numpy
import scipy.stats as stats
from collections import defaultdict
from operator import itemgetter

import fitness_func as ff
import config as cfg
import util

def main(argv):
    assert len(argv)==2

    dirpath = argv[1]
    assert sys.isDirs(dirpath)

    # set pop
    pop = []
    pop = ...

    # rank
    valid, recallRankMat = testKendal(pop, data)
    print valid
    print recallRankMat

if __name__ == "__main__":
    start_time = time.time()
    main(sys.argv)
    print("--- %s seconds ---" % (time.time() - start_time))
