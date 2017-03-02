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
    # dirpath = '../../dataset/metadata/compound/pubchem/pubchem_prop_20170301-1545'
    # insertPubchemProps(csr,dirpath)

    ##
    dirpath = '../../dataset/metadata/compound/pubchem/pubchem_synonyms_20170301-1545'
    insertPubchemSynonyms(csr,dirpath)

    ##
    conn.commit()
    conn.close()

def insertPubchemProps(csr,dirpath):
    ##
    cas2prop = {}
    idx = 0
    for fname in os.listdir(dirpath):
        idx += 1
        print 'opening prop file i= '+str(idx)
        cas = fname.split('_')[1]
        if fname.endswith(".json"):
            fpath = os.path.join(dirpath,fname)
            with open(fpath,'r') as f:
                prop = yaml.load(f)
                prop = prop['PropertyTable']['Properties'][0] # take only the first!
                cas2prop[cas] = prop

    ##
    idx = 0
    n = len(cas2prop)
    for cas,prop in cas2prop.iteritems():
        idx += 1
        print 'updating prop on cas= '+cas+' => '+str(idx)+'/'+str(n)

        valList = []
        if 'CID' in prop:
            s = 'com_pubchem_id='+quote(str(prop['CID']))
            valList.append(s)
        if 'InChIKey' in prop:
            s = 'com_inchikey='+quote(prop['InChIKey'])
            valList.append(s)
        if 'IUPACName' in prop:
            s = 'com_iupac_name='+quote(prop['IUPACName'])
            valList.append(s)
        if 'IsomericSMILES' in prop:
            s = 'com_smiles_isomeric='+quote(prop['IsomericSMILES'])
            valList.append(s)
        if 'CanonicalSMILES' in prop:
            s = 'com_smiles_canonical='+quote(prop['CanonicalSMILES'])
            valList.append(s)

        qf = 'UPDATE compound SET '
        qm  = ','.join(valList)
        qr = ' WHERE com_cas_id='+quote(cas)
        q = qf+qm+qr
        csr.execute(q)

def insertPubchemSynonyms(csr,dirpath):
    ##
    sep = '~$~'
    cas2syn = {}
    cas2name = {}
    idx = 0
    for fname in os.listdir(dirpath):
        idx += 1
        print 'opening i= '+str(idx)+' => '+fname

        cas = fname.split('_')[1]
        if fname.endswith(".json"):
            fpath = os.path.join(dirpath,fname)
            with open(fpath,'r') as f:
                syn = yaml.load(f)
                syn = syn['InformationList']['Information'][0]
                syn = syn['Synonym']

                name = syn[0]
                name = name.capitalize()
                cas2name[cas] = name

                _ = ''.join(syn); assert not(sep in _)
                syn = sep.join(syn)
                cas2syn[cas] = syn

    ##
    idx = 0
    n = len(cas2syn)
    for cas,syn in cas2syn.iteritems():
        idx += 1
        print 'updating syn on cas= '+cas+' => '+str(idx)+'/'+str(n)

        ##
        qf = 'UPDATE compound SET '
        qm  = 'com_pubchem_synonym='+quote(syn)+','
        qm += 'com_pubchem_name='+quote( cas2name[cas] )
        qr = ' WHERE com_cas_id='+quote(cas)
        q = qf+qm+qr
        csr.execute(q)

if __name__ == '__main__':
    main()
