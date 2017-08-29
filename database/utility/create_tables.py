#!/usr/bin/python
import sys

import yaml
import psycopg2

with open('../config_database.json','r') as f:
   dcfg = yaml.load(f)
   
def main(argv):
    conn = psycopg2.connect(database=dcfg['database'],
                          user=dcfg['user'], password=dcfg['password'],
                          host=dcfg['host'], port=dcfg['port'])
    csr = conn.cursor()

    csr.execute('DROP TABLE IF EXISTS plant;')
    csr.execute('''
                CREATE TABLE plant (
                pla_id varchar(12) PRIMARY KEY,
                pla_name varchar(256) NOT NULL UNIQUE,
                pla_idr_name varchar(256)
                );
                ''')

    csr.execute('DROP TABLE IF EXISTS compound;')
    csr.execute('''
                CREATE TABLE compound (
                com_id varchar(12) PRIMARY KEY,
                com_drugbank_id varchar(128) UNIQUE,
                com_knapsack_id varchar(128) UNIQUE,
                com_kegg_id varchar(128) UNIQUE,
                com_cas_id varchar(128) UNIQUE,
                com_pubchem_name varchar(512),
                com_iupac_name varchar(16384),
                com_inchikey varchar(2048),
                com_pubchem_id varchar(128),
                com_smiles_canonical varchar(32768),
                com_smiles_isomeric varchar(32768),
                com_pubchem_synonym text
                );
                ''')

    csr.execute('DROP TABLE IF EXISTS protein;')
    csr.execute('''
                CREATE TABLE protein (
                pro_id varchar(12) PRIMARY KEY,
                pro_name varchar(512) NOT NULL UNIQUE,
                pro_uniprot_id varchar(8) NOT NULL UNIQUE,
                pro_uniprot_abbrv varchar(64) NOT NULL UNIQUE,
                pro_pdb_id text
                );
                ''')

    csr.execute('DROP TABLE IF EXISTS disease;')
    csr.execute('''
                CREATE TABLE disease (
                dis_id varchar(12) PRIMARY KEY,
                dis_omim_id varchar(8) NOT NULL UNIQUE,
                dis_name varchar(16384) NOT NULL UNIQUE,
                dis_uniprot_abbrv varchar(256) NOT NULL
                );
                ''')

    csr.execute('DROP TABLE IF EXISTS plant_vs_compound;')
    csr.execute('''
                CREATE TABLE plant_vs_compound (
                pla_id varchar(12) NOT NULL,
                com_id varchar(12) NOT NULL,
                source varchar(128) NOT NULL,
                weight float(16) DEFAULT 1.00000,
                time_stamp timestamp DEFAULT now()
                );
                ''')

    csr.execute('DROP TABLE IF EXISTS compound_vs_protein;')
    csr.execute('''
                CREATE TABLE compound_vs_protein (
                com_id varchar(12) NOT NULL,
                pro_id varchar(12) NOT NULL,
                source varchar(256) NOT NULL,
                weight float(16) DEFAULT 1.00000,
                time_stamp timestamp DEFAULT now()
                );
                ''')

    csr.execute('DROP TABLE IF EXISTS protein_vs_disease;')
    csr.execute('''
                CREATE TABLE protein_vs_disease (
                pro_id varchar(12) NOT NULL,
                dis_id varchar(12) NOT NULL,
                source varchar(256) NOT NULL,
                weight float(16) DEFAULT 1.00000,
                time_stamp timestamp DEFAULT now()
                );
                ''')

    csr.execute('DROP TABLE IF EXISTS user_msg;')
    csr.execute('''
                CREATE TABLE user_msg (
                id SERIAL PRIMARY KEY,
                name varchar(32),
                email varchar(32),
                affiliation varchar(128),
                subject varchar(16),
                msg text,
                time_stamp timestamp DEFAULT now()
                );
                ''')

    csr.execute('DROP TABLE IF EXISTS compound_similarity;')
    csr.execute('''
                CREATE TABLE compound_similarity (
                com_id_i varchar(12) NOT NULL,
                com_id_j varchar(12) NOT NULL,
                method varchar(64) NOT NULL,
                value float(16) NOT NULL,
                time_stamp timestamp DEFAULT now()
                );
                ''')

    csr.execute('DROP TABLE IF EXISTS protein_similarity;')
    csr.execute('''
                CREATE TABLE protein_similarity (
                pro_id_i varchar(12) NOT NULL,
                pro_id_j varchar(12) NOT NULL,
                method varchar(64) NOT NULL,
                value float(16) NOT NULL,
                time_stamp timestamp DEFAULT now()
                );
                ''')

    csr.execute('DROP VIEW IF EXISTS total_view;')
    csr.execute('''create view total_view as select
                (select count (*) from plant) as plant_total,
                (select count (*) from compound) as compound_total,
                (select count (*) from protein) as protein_total,
                (select count (*) from disease) as disease_total;
                ''')

    conn.commit()
    conn.close()
    print "Tables and views have been created successfully"

if __name__ == '__main__':
    main(sys.argv)
