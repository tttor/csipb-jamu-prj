import os
import json
import sys

import numpy as np


'''
    This file for get matrix accuracy to plot accuracy.
    Please check some parameter before your running this script :
    1. Rootdir param that contain path where your file exist.
    2. Dataset param that show where data you want to get.
    3. Path for your file .csv to save--this file come with format :
       TargetDirPath+'/matrixAccuracy-'+dataset+'-'+NumberGeneration+'-'+Scenario+'.csv'

    The result of this script is Matrix Accuracy with format :
    MatrixAccuracy-(dataset)-(#Running)-(TypeofExprmt).csv
'''

rootdir = '/home/banua/xprmt/xprmt-icacsis16/0008/'
dataset = 'jamu'
targetDir = '/home/banua/xprmt/xprmt-icacsis16/'+dataset

matrixAccuracy = np.array([])

for root, subFolders, files in os.walk(rootdir):
    if dataset in root:
        if 'perf_metrics.json' in files:
            print root
            try :
                with open(root + "/perf_metrics.json", 'r') as f:
                    data = json.loads(f.read())
                    print data["accuracy"]
                    print matrixAccuracy.shape
                    matrixAccuracy = np.vstack([matrixAccuracy, np.asarray(data["accuracy"])]) \
                        if matrixAccuracy.size else np.asarray(data["accuracy"])

                    print matrixAccuracy.shape
                print "Successfull loaded"
            except:
                print "Unable to load json"


    np.savetxt(targetDir+'/matrixAccuracy-'+dataset+'-100-2.csv', np.transpose(matrixAccuracy), fmt='%.5e', delimiter='\t')

