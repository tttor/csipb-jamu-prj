# devel.py
import sys
import numpy as np
import matplotlib.pyplot as plt
from kronrls import KronRLS
from sklearn.cross_validation import KFold
from sklearn.cross_validation import StratifiedKFold
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score
import yamanishi_data_util as yam

outDir = '../../xprmt'

def main(argv):
    if len(argv)!=2:
        print 'USAGE: python devel.py [valMode]'
        return

    valMode = argv[1]

    # load development dataset, containing com-pro connectivity
    mode = 'nr'
    connMat,comList,proList = yam.loadComProConnMat(mode)
    kernel = yam.loadKernel(mode)

    ##
    dataX = []
    dataY = []
    for i,ii in enumerate(comList):
        for j,jj in enumerate(proList):
            dataX.append( (ii,jj) )
            dataY.append( connMat[i][j] )
    nData = len(dataY)

    ## instantiate a KronRLS predictor
    kronrls = KronRLS(connMat,comList,proList,kernel)

    ##
    nFolds = None
    kfList = None
    if valMode=='loocv':
        nFolds = nData
        kfList = KFold(nData, n_folds=nFolds, shuffle=True)
    elif valMode=='kfcv':
        nFolds = 5
        kfList = StratifiedKFold(dataY, n_folds=nFolds, shuffle=True)
    else:
        assert(False)

    yTestList = []
    yPredList = []
    fold = 0
    for trIdxList, testIdxList in kfList:
        fold += 1
        print 'fold= ',fold,'of',nFolds,'######################################'

        xTest = [dataX[i] for i in testIdxList]
        yTest = [dataY[i] for i in testIdxList]
        # xTr = [dataX[i] for i in trIdxList]
        # yTr = [dataY[i] for i in trIdxList]

        # test
        gamma = 1.0
        yPred = kronrls.predict(xTest,gamma)

        yTestList += yTest
        yPredList += yPred


    ##
    precision, recall, _ = precision_recall_curve(yTestList, yPredList)
    prAUC = average_precision_score(yTestList, yPredList, average='micro')

    ##
    plt.clf()
    plt.figure()

    plt.plot(recall, precision, 'r-',
             label= '(area = %0.2f)' % prAUC, lw=2)

    plt.ylim([-0.05, 1.05])
    plt.xlim([-0.05, 1.05])
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curve')
    plt.legend(loc="lower left")

    fname = '/pr_curve_'+valMode+'.png'
    plt.savefig(outDir+fname, bbox_inches='tight')

if __name__ == '__main__':
    main(sys.argv)
