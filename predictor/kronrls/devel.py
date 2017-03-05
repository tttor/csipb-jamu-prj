# devel.py
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
from kronrls import KronRLS
from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score

sys.path.append('../util')
import yamanishi_data_util as yam
sys.path.append('../../config')
from predictor_config import kronRLSConfig as cfg

outDir = '../../xprmt/kronrls/'

def main(argv):
    if len(argv)!=3:
        print 'USAGE: '
        print 'python devel.py [dataMode:e/nr/gpcr/ic] [valMode:loocv/kfcv]'
        return

    dataMode = argv[1]
    valMode = argv[2]

    # load development dataset, containing com-pro connectivity
    connMatDpath = '../../dataset/connectivity/compound_vs_protein/yamanishi/ground-truth'
    connMat,comList,proList = yam.loadComProConnMat(dataMode,connMatDpath)

    kernelDpath = '../../dataset/connectivity/compound_vs_protein/yamanishi/similarity-mat'
    kernel = yam.loadKernel(dataMode,kernelDpath)

    ##
    dataX = []
    dataY = []
    for i,ii in enumerate(comList):
        for j,jj in enumerate(proList):
            dataX.append( (ii,jj) )
            dataY.append( connMat[i][j] )
    nData = len(dataY)
    print 'nData= '+str(nData)

    ## instantiate a KronRLS predictor
    kronrls = KronRLS(cfg,connMat,comList,proList,kernel)

    ##
    nFolds = None
    kfList = None
    if valMode=='loocv':
        nFolds = nData
        kf = KFold(n_splits=nFolds)
        kfList = kf.split(dataX)
    elif valMode=='kfcv':
        nFolds = 10
        skf = StratifiedKFold(n_splits=nFolds)
        kfList = skf.split(dataX,dataY)
    else:
        assert(False)

    yTestList = []
    yPredList = []
    fold = 0
    for trIdxList, testIdxList in kfList:
        fold += 1
        print 'fold=',fold,'of',nFolds,'######################################'

        xTest = [dataX[i] for i in testIdxList]
        yTest = [dataY[i] for i in testIdxList]
        # xTr = [dataX[i] for i in trIdxList]
        # yTr = [dataY[i] for i in trIdxList]

        # test
        yPred = kronrls.predict(xTest)

        yTestList += yTest
        yPredList += yPred

    ##
    print 'calculating aupr...'
    precision, recall, _ = precision_recall_curve(yTestList, yPredList)
    aupr = average_precision_score(yTestList, yPredList, average='micro')

    ##
    print 'plotting ...'
    plt.clf()
    plt.figure()

    plt.plot(recall, precision, 'r-',
             label= '(area = %0.2f)' % aupr, lw=2)

    plt.ylim([-0.05, 1.05])
    plt.xlim([-0.05, 1.05])
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curve of '+dataMode+' '+valMode)
    plt.legend(loc="lower left")

    fname = 'pr_curve_'+dataMode+'_'+valMode+'.png'
    plt.savefig(outDir+fname, bbox_inches='tight')

if __name__ == '__main__':
    start_time = time.time()
    main(sys.argv)
    print("--- %s seconds ---" % (time.time() - start_time))
