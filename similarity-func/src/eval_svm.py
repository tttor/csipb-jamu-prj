import numpy as np
import sys
import os
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.cross_validation import train_test_split

import util
import config as cfg

def main(argv):
    assert len(argv)==3
    dataName = argv[1]
    xprmtDir = cfg.xprmtDir+'/'+argv[2]
    assert os.path.isdir(xprmtDir)

    #
    data,dataDict = util.loadData(cfg.datasetPaths[dataName])
    X = data[:, 1:]
    y = data[:, 0]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    #
    gpFuncFilepath = xprmtDir+'/summary/individualHOF.csv'
    contents = []
    with open(gpFuncFilepath, 'r') as f:
        contents = f.readlines()
    funcStrList = contents[-1].split(';') # take only the last generation
    funcStrList.append(util.tanimotoStr())

    funcStrList = [s.rstrip() for s in funcStrList]
    funcStrList = [util.expandFuncStr(s) for s in funcStrList]

    #
    for f in funcStrList:
        # tune
        clf = svm.SVC(kernel='precomputed')

        # train
        gram_train = util.computeGram(X_train, f)
        clf.fit(gram_train, y_train)

        # test
        gram_test = util.computeGram(X_train, f)
        y_pred = clf.predict(gram_test)
        acc = accuracy_score(y_train, y_pred)
        print acc

if __name__ == '__main__':
    main(sys.argv)
