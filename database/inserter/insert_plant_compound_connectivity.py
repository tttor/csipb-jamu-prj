# insert_plant_compound_connectivity.py
import sys
import pickle

import yaml
import psycopg2

sys.path.append('../utility')
import postgre_util as pgu

with open('../config_database.json','r') as f:
   dcfg = yaml.load(f)

def main():
    conn = psycopg2.connect(database=dcfg['database'],
                          user=dcfg['user'], password=dcfg['password'],
                          host=dcfg['host'], port=dcfg['port'])
    csr = conn.cursor()

    ## conn source ##
    knapsack(csr)
    ################

    conn.commit()
    conn.close

def knapsack(csr):
    source = 'knapsack.kanaya.naist.jp'
    fpath = '../source/knapsack/20161003/knapsack_jsp_plant_vs_compound_2016-10-04_16:34:06.468234.pkl'

    print 'loading...'
    with open(fpath, 'rb') as f:
        plaComDict = pickle.load(f)

    plaIdx = 0
    comIdx = 0
    for plaName,comList in plaComDict.iteritems():
        plaIdx += 1
        plaID = 'PLA'+str(plaIdx).zfill(8)

        # insert pla
        pgu.insert('plant',['pla_id','pla_name'],[plaID,plaName],csr)

        for c,com in enumerate(comList):
            msg = 'inserting plaIdx='+str(plaIdx)+'/'+str(len(plaComDict))
            msg += ' and comIdx='+str(c+1)+'/'+str(len(comList))
            print msg

            comKnapsackID,comCAS,_,_ = com

            # insert com iff necessary
            rows = pgu.select('com_id','compound','com_cas_id',comCAS,csr)
            if len(rows)==0:
                comIdx += 1
                comID = 'COM'+str(comIdx).zfill(8)
                pgu.insert('compound',['com_id','com_cas_id','com_knapsack_id'],
                           [comID,comCAS,comKnapsackID],csr)
            else:
                comID = rows[0][0]

            # insert pla-com conn
            pgu.insert('plant_vs_compound',['pla_id','com_id','source'],[plaID,comID,source],csr)

if __name__ == '__main__':
    main()