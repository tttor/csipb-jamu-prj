# insert_compound_metadata.py
import os
import yaml
import psycopg2
from config import databaseConfig as dcfg
from postgresql_util import quote

def main():
    ##
    conn = psycopg2.connect(database=dcfg['name'],
                            user=dcfg['user'],password=dcfg['passwd'],
                            host=dcfg['host'],port=dcfg['port'])
    csr = conn.cursor()

    ##
    dirpath = '../../dataset/metadata/compound/pubchem/pubchem_prop_20170301-1545'
    insertPubchemProps(dirpath)

    ##
    conn.commit()
    conn.close()

def insertPubchemProps(dirpath):
    ##
    cas2prop = {}
    for fname in os.listdir(dirpath):
        cas = fname.split('_')[1]
        if fname.endswith(".json"):
            fpath = os.path.join(dirpath,fname)
            prop = None
            with open(fpath,'r') as f:
                prop = yaml.load(f)
                prop = prop['PropertyTable']['Properties'][0]
            cas2prop[cas] = prop
        break

    ##
    propList = ['CID','InChIKey','IUPACName','IsomericSMILES','CanonicalSMILES']
    for cas,prop in cas2prop.iteritems():
        print cas

        qf = 'UPDATE compound SET '
        qm  = 'com_pubchem_id='+quote(str(prop['CID']))+','
        qm += 'com_inchikey='+quote(prop['InChIKey'])+','
        qm += 'com_iupac_name='+quote(prop['IUPACName'])+','
        qm += 'com_smiles_isomeric='+quote(prop['IsomericSMILES'])+','
        qm += 'com_smiles_canonical='+quote(prop['CanonicalSMILES'])
        qr = ' WHERE com_cas_id='+quote(cas)
        q = qf+qm+qr
        print q
        # csr.execute(q)

def insertPubchemSynonyms():
    pass

if __name__ == '__main__':
    main()
