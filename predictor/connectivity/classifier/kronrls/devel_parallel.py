# devel.py
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
from kronrls import KronRLS
from sklearn.cross_validation import KFold
from sklearn.cross_validation import StratifiedKFold
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score
from scoop import futures as fu
import yamanishi_data_util as yam

outDir = '../../xprmt'

def main(argv):
    if len(argv)!=3:
        print 'USAGE: python devel.py [dataMode] [valMode]'
        return

    dataMode = argv[1]
    valMode = argv[2]

    # load development dataset, containing com-pro connectivity
    connMat,comList,proList = yam.loadComProConnMat(dataMode)
    kernel = yam.loadKernel(dataMode)

    ##
    dataX = []
    dataY = []
    for i,ii in enumerate(comList):
        for j,jj in enumerate(proList):
            dataX.append( (ii,jj) )
            dataY.append( connMat[i][j] )
    nData = len(dataY)

    ##
    nFolds = None
    kfList = None
    if valMode=='loocv':
        nFolds = nData
        kfList = KFold(nData, n_folds=nFolds, shuffle=True)
    elif valMode=='kfcv':
        nFolds = 10
        kfList = StratifiedKFold(dataY, n_folds=nFolds, shuffle=True)
    else:
        assert(False)

    kronrls = KronRLS(connMat,comList,proList,kernel)

    ## prep for parallel
    xTestList = []
    yTestList = []
    for trIdxList, testIdxList in kfList:
        xTest = [dataX[i] for i in testIdxList]
        yTest = [dataY[i] for i in testIdxList]

        xTestList.append(xTest)
        yTestList.append(yTest)

    ##
    yPredList = fu.map(evalPerFold,xTestList,yTestList,[kronrls]*nFolds,
                       [connMat]*nFolds,[comList]*nFolds,[proList]*nFolds,[kernel]*nFolds)

    # ##
    # precision, recall, _ = precision_recall_curve(yTestList, yPredList)
    # aupr = average_precision_score(yTestList, yPredList, average='micro')

    # ##
    # plt.clf()
    # plt.figure()

    # plt.plot(recall, precision, 'r-',
    #          label= '(area = %0.2f)' % aupr, lw=2)

    # plt.ylim([-0.05, 1.05])
    # plt.xlim([-0.05, 1.05])
    # plt.xlabel('Recall')
    # plt.ylabel('Precision')
    # plt.title('Precision-Recall Curve')
    # plt.legend(loc="lower left")

    # fname = '/pr_curve_'+dataMode+'_'+valMode+'.png'
    # plt.savefig(outDir+fname, bbox_inches='tight')

def evalPerFold(xTest,yTest,kronrls,connMat,comList,proList,kernel):
    gamma = 1.0
    yPred = kronrls.predict(xTest,gamma)

if __name__ == '__main__':
    start_time = time.time()
    main(sys.argv)
    print("--- %s seconds ---" % (time.time() - start_time))
