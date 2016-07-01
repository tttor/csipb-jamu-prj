import sys
import os
import json
import yaml
import numpy as np
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.cross_validation import train_test_split

import util
import config as cfg

def main(argv):
    assert len(argv)==3
    xprmtDir = cfg.xprmtDir+'/'+argv[1]
    nTop = int(argv[2])
    assert os.path.isdir(xprmtDir)

    #
    X_train = np.genfromtxt(xprmtDir+'/data/X_train.csv', delimiter=',')
    X_test = np.genfromtxt(xprmtDir+'/data/X_test.csv', delimiter=',')
    y_train = np.genfromtxt(xprmtDir+'/data/y_train.csv', delimiter=',')
    y_test = np.genfromtxt(xprmtDir+'/data/y_test.csv', delimiter=',')

    #
    param = dict()
    with open(xprmtDir+'/log2.json') as f:
        param = yaml.load(f)

    hofFilepath = xprmtDir+'/gen-'+str(param['nGen']-1)+'/hofIndividual.csv'

    funcStrList = []
    with open(hofFilepath, 'r') as f:
        funcStrList = f.readlines()

    funcStrList = funcStrList[0:nTop] # take only the nTop best func/individual
    funcStrList.append( util.tanimotoStr() )

    funcStrList = [s.rstrip() for s in funcStrList]
    funcStrList = [util.expandFuncStr(s) for s in funcStrList]
    
    for f in funcStrList:
        # tune
        clf = svm.SVC(kernel='precomputed')

        # train
        gram_train = util.computeGram(X_train, X_train, f)
        clf.fit(gram_train, y_train)

        # test
        gram_test = util.computeGram(X_test, X_train, f)
        y_pred = clf.predict(gram_test)

        acc = accuracy_score(y_test, y_pred)
        print acc

if __name__ == '__main__':
    main(sys.argv)
