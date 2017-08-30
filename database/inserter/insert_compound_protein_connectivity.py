# insert_compound_protein_connectivity.py
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
    drugbank(csr)
    #################

    conn.commit()
    conn.close

def drugbank(csr):
    source = 'drugbank.ca'
    fpath = '../source/drugbank/drugbank_20161002/drugbank_drug_data_2016-10-05_10:16:42.860649.pkl'

    print 'loading...'
    with open(fpath, 'rb') as f:
        comDict = pickle.load(f)

    print 'getting last comID and proID'
    lastComIdx = int( pgu.selectMax('com_id','compound',csr)[3:] )
    lastProIdx = int( pgu.selectMax('pro_id','protein',csr)[3:] )
    comIdx = lastComIdx
    proIdx = lastProIdx

    comCounter = 0
    for comDrugbankID,comProp in comDict.iteritems():
        comCounter += 1
        comCAS = comProp['CAS number']
        proList = comProp['uniprotTargets']

        # insert com iff necessary
        rows = pgu.select('com_id','compound','com_cas_id',comCAS,csr)
        if len(rows)==0:
            comIdx += 1
            comID = 'COM'+str(comIdx).zfill(8)

            comData = []
            comData.append(('com_id',comID))
            comData.append(('com_drugbank_id',comDrugbankID))
            comData.append(('com_cas_id',comCAS))
            pgu.insert('compound',[i[0] for i in comData],[i[1] for i in comData],csr)
        else:
            comID = rows[0][0]

        for j,proUniprotID in enumerate(proList):
            msg = 'inserting com i='+str(comCounter)+'/'+str(len(comDict))
            msg += ' and pro j='+str(j+1)+'/'+str(len(proList))
            print msg

            rows = pgu.select('pro_id','protein','pro_uniprot_id',proUniprotID,csr)
            if len(rows)==0:
                # if a protein is NEW then, for now, we assume it is _not_ a human protein
                # therefore, (as we focus on human proteins) that new protein is simply ignored
                continue

                # proIdx += 1
                # proID = 'PRO'+str(proIdx).zfill(8)

                # proData = []
                # proData.append(('pro_id',proID))
                # proData.append(('pro_uniprot_id',proUniprotID));
                # pgu.insert('protein',[i[0] for i in proData],[i[1] for i in proData],csr)
            else:
                proID = rows[0][0]

            # insert com-pro conn
            connData = []
            connData.append(('com_id',comID))
            connData.append(('pro_id',proID))
            connData.append(('source',source))
            pgu.insert('compound_vs_protein',[i[0] for i in connData],[i[1] for i in connData],csr)

    #
    nCom = comIdx
    nPro = proIdx
    nNewCom = comIdx - lastComIdx
    nNewPro = proIdx - lastProIdx
    nMatchedCom = nCom - nNewCom
    nMatchedPro = nPro - nNewPro
    print 'nMatchedCom= '+str(nMatchedCom)+' ('+str( nMatchedCom/float(nCom) )+')'
    print 'nMatchedPro= '+str(nMatchedPro)+' ('+str( nMatchedPro/float(nPro) )+')'

if __name__ == '__main__':
    main()