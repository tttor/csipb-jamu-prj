import os
import sys
import threading
import time

import numpy as np

rootdir = '/home/banua/xprmt'


def calc_performance(rootdir, targetDir):
    subdir =  os.listdir(os.path.join(rootdir, targetDir))
    lenSub = len([i for i in subdir if 'xprmt' in i])
    tcounter = 0

    for subFolder in subdir:
        if 'xprmt' in subFolder:
            tcounter += 1
            print 'Procces {} of {} from {}'.format(tcounter, lenSub, targetDir)
            # print subFolder
            xprmtdir = os.path.join(targetDir, subFolder)
            # print xprmtdir
            print "%s: %s" % (targetDir, time.ctime(time.time()))
            bashCommand = "python -m scoop eval_svm.py " + xprmtdir + " 10"
            os.system(bashCommand)


try:
    (threading.Thread(target=calc_performance, args=(rootdir, 'similarity-func-labac01-0002'))).start()
    # (threading.Thread(target=calc_performance, args=(rootdir, 'similarity-func-labac03-0002'))).start()
    # (threading.Thread(target=calc_performance, args=(rootdir, 'similarity-func-labac05-0002'))).start()
    # (threading.Thread(target=calc_performance, args=(rootdir, 'similarity-func-labac07-0002'))).start()
    # (threading.Thread(target=calc_performance, args=(rootdir, 'similarity-func-labac08-0002'))).start()
    # (threading.Thread(target=calc_performance, args=(rootdir, 'similarity-func-labac09-0002'))).start()
except:
    print "Error: unable to start thread"


