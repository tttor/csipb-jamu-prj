# run_predict.py
import MySQLdb
import dbcrawler_util as util
from blm_core import BLM
from dummy_predictor import DummyPredictor

db = MySQLdb.connect("localhost","root","123","ijah" )
cursor = db.cursor()

def main():
    # TODO get comId and proId from DB
    maxComId = 1000 #21994
    comList = range(1,maxComId+1)
    comList = ['COM'+str(i).zfill(8) for i in comList]

    maxProId = 3334
    proList = range(1,maxProId+1)
    proList = ['PRO'+str(i).zfill(8) for i in proList]

    #
    predictor = DummyPredictor()

    #
    nCom = len(comList)
    nPro = len(proList)
    for i,c in enumerate(comList):
        for j,p in enumerate(proList):
            msg1 = 'search/predict for c= '+c+' ('+str(i+1)+'/'+str(nCom)+') '
            msg2 = ' vs p= '+p+' ('+str(j+1)+'/'+str(nPro)+') '
            msg = msg1+msg2
            print msg

            qf = 'SELECT source,timestamp FROM compound_vs_protein WHERE'
            qr = ' com_id='+'"'+c+'"'+' AND pro_id='+'"'+p+'"'
            q = qf+qr
            resp = util.mysqlCommit(db,cursor,q)

            needToPredict = True
            if resp!=None:
                src,stamp = resp
                if 'predictor' not in src:# then it is a fact
                    needToPredict = False

            if needToPredict:
                print 'predicting ...'
                # (re)predict
                # weight here is the confidence level that the link exists
                weight, srcs = predictor.predict(c,p)

                # insert
                if weight > 0.0:
                    print 'inserting the prediction ...'
                    insertVals = [c,p,str(weight),srcs]
                    insertVals = ['"'+j+'"' for j in insertVals]
                    qf = '''INSERT INTO compound_vs_protein (com_id,pro_id,
                                                             weight,source)
                            VALUES ('''
                    qm = ','.join(insertVals)
                    qr = ')'
                    q = qf+qm+qr
                    util.mysqlCommit(db,cursor,q)

if __name__ == '__main__':
    main()
    db.close()
