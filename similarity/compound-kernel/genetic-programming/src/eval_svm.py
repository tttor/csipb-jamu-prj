import sys
import os
import json
import yaml
import numpy as np
from collections import defaultdict
from scoop import futures as fu

from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.cross_validation import train_test_split
from sklearn.metrics import precision_recall_fscore_support
from sklearn.preprocessing import minmax_scale

import util
import config as cfg

def scale(x):
    m, n = x.shape
    x = np.reshape(x, (m*n, 1))
    x = minmax_scale(x, feature_range=(0, 1), axis=0)
    data = np.reshape(x, (m, n))

    return data

def tuneTrainTest(f, X_train, y_train, X_test, y_test):
    print 'Evaluating ', f

    # tune
    clf = svm.SVC(kernel='precomputed')

    # train
    gram_train = util.computeGram(X_train, X_train, f)
    # gram_train = scale(gram_train)
    clf.fit(gram_train, y_train)

    # test
    gram_test = util.computeGram(X_test, X_train, f)
    # gram_test = scale(gram_test)
    y_pred = clf.predict(gram_test)
    # np.savetxt(xprmtDir+"/data/y_pred_"+f+".csv", y_pred, delimiter=",")

    acc = accuracy_score(y_test, y_pred)
    precision, recall, fscore, support = precision_recall_fscore_support(y_test, y_pred,
                                                                         average='micro')
    return (acc, precision, recall, fscore, support)

def main(argv):
    assert len(argv)==3
    xprmtDir = cfg.xprmtDir+'/'+argv[1]; print xprmtDir; assert os.path.isdir(xprmtDir)

    nTop = int(argv[2])
    metrics = defaultdict(list)

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
    funcStrList = [f for f in funcStrList if len(f)!=0]

    if nTop > len(funcStrList):
        nTop = len(funcStrList)

    funcStrList = funcStrList[0:nTop] # take only the nTop best func/individual
    funcStrList.append( util.tanimotoStr() )

    funcStrList = [s.rstrip() for s in funcStrList]
    funcStrList = [util.expandFuncStr(s) for s in funcStrList]
    metrics['funcStr'] = funcStrList

    nIndividual = len(funcStrList)
    perfList = fu.map (tuneTrainTest,funcStrList, [X_train]*nIndividual, [y_train]*nIndividual, [X_test]*nIndividual, [y_test]*nIndividual)

    for p in perfList:
        metrics['accuracy'].append( p[0])
        metrics['precision'].append(p[1])
        metrics['recall'].append(p[2])
        metrics['fscore'].append([3])
        metrics['support'].append([4])

    with open(xprmtDir+"/data/perf_metrics.json", 'wb') as f:
        json.dump(metrics, f, indent=2, sort_keys=True)

if __name__ == '__main__':
    main(sys.argv)
