import os
import sys
import threading

import numpy as np

'''
This file for generate matrix avg, matrix max, matrix min for plotting fitness purpose
Before running this script, please checks some parameter below :
1. Rootdir          : Contain your root directory path
2. Dataset          : Dataset name that you want to use
3. SavedFileName    : Filename to save

The results of this script are matrix avg, max, & min with format :
- Matrix Avg : targetDir+'/matrixAvg-(#-Running)-(TypeofXprmt).csv'
- Matrix Max : targetDir+'/matrixMax-(#-Running)-(TypeofXprmt).csv'
- MAtrix Min : targetDir+'/matrixMin-(#-Running)-(TypeofXprmt).csv'
'''

def getfile(rootdir, dataset):
    #rootdir = '/home/banua/xprmt/xprmt-icacsis16/0008/'
    #dataset = 'jamu'
    targetDir = '/home/banua/xprmt/xprmt-icacsis16/'+dataset

    matrixMax = np.array([])

    matrixFitness = np.zeros((101, 1))
    # print 'Please Wait..'
    for i in os.listdir(rootdir):
        for j in os.listdir(rootdir+i):
            if dataset in j:
                tcounter = 0
                for x in os.listdir(rootdir+i+'/'+j):
                    # print '.'
                    if 'gen-' in x:
                        tcounter += 1

                        splitkata = x.split('-')
                        fname = rootdir+i+'/'+j+'/'+x+'/hofFitness.csv'

                        hof = np.loadtxt(fname, delimiter=',')

                        matrixFitness[int(splitkata[1])] = hof[0]


    #                     print matrixFitness
                status = False
                for k in range(0, 10):
                    if matrixFitness[k] < matrixFitness[k+1]:
                        status = False
                        print j, ' ', i
                        break
                    else :
                        status = True

                if status == False :
                    matrixMax = np.hstack([matrixMax, np.asarray(matrixFitness)]) if matrixMax.size else np.asarray(matrixFitness)
                # print matrixFitness




    print matrixMax.shape
    np.savetxt(targetDir + '/matrixMax-' + dataset + '-1.csv', matrixMax, fmt='%.5e', delimiter='\t')

try:
    # (threading.Thread(target=getfile, args=('/home/banua/xprmt/xprmt-icacsis16/0007/', 'jamu'))).start()
    (threading.Thread(target=getfile, args=('/home/banua/xprmt/xprmt-icacsis16/0001/', 'maccs'))).start()
    (threading.Thread(target=getfile, args=('/home/banua/xprmt/xprmt-icacsis16/0001/', 'zoo'))).start()
except:
   print "Error: unable to start thread"