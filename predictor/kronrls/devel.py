# devel.py
import yamanishi_data_util as yam
from kronrls import KronRLS

def main():
    # load development dataset, containing com-pro connectivity
    mode = 'bind_orfhsa_drug_e.txt'
    yamanishiData = yam.loadComProConn(mode)

    # spit as training and testing data
    trData = yamanishiData[1:]
    teData = yamanishiData[0:1]

    # instantiate a KronRLS predictor
    kronrls = KronRLS(trData)

    # # test
    # com = 'D00002'
    # pro = 'hsa:10'
    # gamma = 1.0
    # ypred = kronrls.predict(com,pro,gamma)

if __name__ == '__main__':
    main()
