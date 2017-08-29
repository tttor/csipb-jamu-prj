# insert_protein_disease_connectivity.py
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
    uniprot(csr)
    #################

    conn.commit()
    conn.close

def uniprot(csr):
    source = 'uniprot.org'
    fpath = '../source/uniprot/uniprot_human_dat_20160928/uniprot_sprot_human.pkl'

    print 'loading...'
    with open(fpath, 'rb') as f:
        proDict = pickle.load(f)

    proIdx = 0
    disIdx = 0
    for proAbbrv,proProp in proDict.iteritems():
        proUniprotID = proProp['access']
        proName = proProp['name']
        disList = proProp['disease']

        proIdx += 1
        proID = 'PRO'+str(proIdx).zfill(8)

        # insert pro
        proData = []
        proData.append(('pro_id',proID))
        proData.append(('pro_name',proName))
        proData.append(('pro_uniprot_id',proUniprotID))
        proData.append(('pro_uniprot_abbrv',proAbbrv))
        pgu.insert('protein',[i[0] for i in proData],[i[1] for i in proData],csr)

        for d,dis in enumerate(disList):
            msg = 'inserting proIdx='+str(proIdx)+'/'+str(len(proDict))
            msg += ' and disIdx='+str(d+1)+'/'+str(len(disList))
            print msg

            disName,disAbbrv,disOmimID = dis

            # insert dis iff necessary
            rows = pgu.select('dis_id','disease','dis_omim_id',disOmimID,csr)
            if len(rows)==0:
                disIdx += 1
                disID = 'DIS'+str(disIdx).zfill(8)

                disData = []
                disData.append(('dis_id',disID))
                disData.append(('dis_omim_id',disOmimID))
                disData.append(('dis_name',disName))
                disData.append(('dis_uniprot_abbrv',disAbbrv))
                pgu.insert('disease',[i[0] for i in disData],[i[1] for i in disData],csr)
            else:
                disID = rows[0][0]

            # insert pla-com conn
            connData = []
            connData.append(('pro_id',proID))
            connData.append(('dis_id',disID))
            connData.append(('source',source))
            pgu.insert('protein_vs_disease',[i[0] for i in connData],[i[1] for i in connData],csr)

if __name__ == '__main__':
    main()