import os
import json
import sys

import numpy as np

rootdir = '/home/banua/xprmt/xprmt-icacsis16/0008/'
dataset = 'jamu'
keyword = 'gen-'
targetDir = '/home/banua/xprmt/xprmt-icacsis16/'+dataset
xprmt = '-100-2'

matrixFitness = np.array([])
matrixFitnessInd = np.array([])
matrixInd = np.asarray([])

for xprmtDir in os.listdir(rootdir):
    print xprmtDir
    if os.path.isdir(os.path.join(rootdir, xprmtDir)):
        for i in os.listdir(os.path.join(rootdir, xprmtDir)):
            if ('xprmt' in i) and (dataset in i):
                print 'i', i
                tcounter = 0

                dirGen = os.path.join(rootdir, xprmtDir, i)
                for j in os.listdir(dirGen):
                    if keyword in j:
                        tcounter += 1

                print 'tcounter', tcounter
                metricdir = rootdir+xprmtDir+"/"+i+"/data"

                try:
                    with open(metricdir + "/perf_metrics.json", 'r') as f:
                        dataindaccu = json.loads(f.read())

                        print matrixInd.shape
                        matrixInd = np.vstack([matrixInd, np.asarray(dataindaccu["accuracy"][0:100])]) \
                            if matrixInd.size else np.asarray(dataindaccu["accuracy"][0:100])

                        print matrixInd.shape

                    data = np.loadtxt(dirGen + "/" +keyword + str(tcounter-1)+ "/hofFitness.csv", delimiter='\t')
                    dataind = np.loadtxt(dirGen + "/" +keyword + str(tcounter-1)+ "/hofIndividual.csv", dtype=str, delimiter='\t')
                    print matrixFitness.shape
                    matrixFitness =  np.vstack([matrixFitness, data[0:100]]) \
                        if matrixFitness.size else data[0:100]
                    print matrixFitness.shape

                    print matrixFitnessInd.shape
                    matrixFitnessInd = np.vstack([matrixFitnessInd, dataind[0:100]]) \
                        if matrixFitnessInd.size else dataind[0:100]
                    print matrixFitnessInd.shape
                            #
                        # assert False
                    print "Successfully loaded"
                except:
                    print "Unable to load file"


    np.savetxt(targetDir+'/matrixFitness-'+dataset+xprmt+'.csv', np.transpose(matrixFitness), fmt='%.5e', delimiter='\t')
    np.savetxt(targetDir + '/matrixFitnessInd-'+dataset+xprmt+'.csv', np.transpose(matrixFitnessInd),  fmt='%s', delimiter='\t')
    np.savetxt(targetDir + '/matrixInd-'+dataset+xprmt+'.csv', np.transpose(matrixInd), fmt='%s', delimiter='\t')

