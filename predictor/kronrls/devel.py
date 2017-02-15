# devel.py
import yamanishi_data_util as yam
from kronrls import KronRLS

def main():
    # load development dataset, containing com-pro connectivity
    mode = 'nr'
    yamanishiData = yam.loadComProConn(mode)
    kernelData = yam.loadKernel(mode)

    # spit as training and testing data
    trData = yamanishiData[1:]
    teData = yamanishiData[0:1]

    # instantiate a KronRLS predictor
    kronrls = KronRLS(trData,kernelData)

    # test
    gamma = 1.0
    for com,pro in teData:
        ypred = kronrls.predict(com,pro,gamma)
        print 'ypred= ',ypred

if __name__ == '__main__':
    main()
