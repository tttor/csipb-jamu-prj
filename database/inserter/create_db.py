#!/usr/bin/python
import psycopg2
import sys

def main(argv):
    assert len(argv)==6

    db = argv[1]
    user = argv[2]; passwd = argv[3]
    host = argv[4]; port = argv[5]
    conn = psycopg2.connect(database=db, user=user, password=passwd,
                            host=host, port=port)
    cur = conn.cursor()

    cur.execute('DROP TABLE IF EXISTS plant;')
    cur.execute('''CREATE TABLE plant (
                pla_id varchar(12) PRIMARY KEY,
                pla_name varchar(256) NOT NULL UNIQUE
                );
                ''')

    cur.execute('DROP TABLE IF EXISTS compound;')
    cur.execute('''CREATE TABLE compound (
                com_id varchar(12) PRIMARY KEY,
                com_cas_id varchar(128),
                com_drugbank_id varchar(128),
                com_inchikey varchar(1024),
                com_kegg_id varchar(128),
                com_knapsack_id varchar(128),
                com_pubchem_id varchar(128),
                com_smiles varchar(16384),
                com_simcomp varchar(128)
                );
                ''')

    cur.execute('DROP TABLE IF EXISTS protein;')
    cur.execute('''CREATE TABLE protein (
                pro_id varchar(12) PRIMARY KEY,
                pro_name varchar(300) NOT NULL,
                pro_uniprot_id varchar(6),
                pro_uniprot_abbrv varchar(50)
                );
                ''')

    cur.execute('DROP TABLE IF EXISTS disease;')
    cur.execute('''CREATE TABLE disease (
                dis_id varchar(12) PRIMARY KEY,
                dis_omim_id varchar(6) NOT NULL,
                dis_uniprot_abbrv varchar(30) NOT NULL
                );
                ''')

    cur.execute('DROP TABLE IF EXISTS plant_vs_compound;')
    cur.execute('''CREATE TABLE plant_vs_compound (
                pla_id varchar(12) NOT NULL,
                com_id varchar(12) NOT NULL,
                weight float(3) NOT NULL,
                source varchar(128) NOT NULL,
                time_stamp timestamp DEFAULT now()
                );
                ''')

    cur.execute('DROP TABLE IF EXISTS compound_vs_protein;')
    cur.execute('''CREATE TABLE compound_vs_protein (
                com_id varchar(12) NOT NULL,
                pro_id varchar(12) NOT NULL,
                weight float(3) NOT NULL,
                source varchar(256) NOT NULL,
                time_stamp timestamp DEFAULT now()
                );
                ''')

    cur.execute('DROP TABLE IF EXISTS protein_vs_disease;')
    cur.execute('''CREATE TABLE protein_vs_disease (
                pro_id varchar(12) NOT NULL,
                dis_id varchar(12) NOT NULL,
                weight float(3) NOT NULL,
                source varchar(256) NOT NULL,
                time_stamp timestamp DEFAULT now()
                );
                ''')

    conn.commit()
    print "Tables have created successfully"

    conn.close()

if __name__ == '__main__':
    main(sys.argv)
