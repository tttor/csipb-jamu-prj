# devel.py
import yamanishi_data_util as yam
import sys
from kronrls import KronRLS
from sklearn.cross_validation import KFold
from sklearn.cross_validation import StratifiedKFold

def main(argv):
    if len(argv)!=2:
        print 'USAGE: python devel.py [valType]'
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
        nFolds = 10
        kfList = StratifiedKFold(dataY, n_folds=nFolds, shuffle=True)
    else:
        assert(False)

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

if __name__ == '__main__':
    main(sys.argv)
