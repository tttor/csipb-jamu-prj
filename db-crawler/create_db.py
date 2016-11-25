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
    print "Opened database successfully"

    cur = conn.cursor()

    cur.execute('DROP TABLE IF EXISTS plant;')
    cur.execute('''CREATE TABLE plant (
                pla_int_id serial NOT NULL,
                pla_id varchar(12) NOT NULL,
                pla_name varchar(256) NOT NULL,
                PRIMARY KEY(pla_int_id)
                );
                ''')

    cur.execute('DROP TABLE IF EXISTS compound;')
    cur.execute('''CREATE TABLE compound (
                com_int_id serial NOT NULL,
                com_id varchar(12) NOT NULL,
                com_cas_id varchar(128) NOT NULL,
                com_drugbank_id varchar(128) NOT NULL,
                com_inchikey varchar(1024) NOT NULL,
                com_kegg_id varchar(128) NOT NULL,
                com_knapsack_id varchar(128) NOT NULL,
                com_pubchem_id varchar(128) NOT NULL,
                com_simcomp varchar(128) NOT NULL,
                com_smiles varchar(16384) NOT NULL,
                PRIMARY KEY(com_int_id)
                );
                ''')

    cur.execute('DROP TABLE IF EXISTS protein;')
    cur.execute('''CREATE TABLE protein (
                pro_int_id serial NOT NULL,
                pro_id varchar(12) NOT NULL,
                pro_name varchar(300) NOT NULL,
                pro_uniprot_id varchar(6) NOT NULL,
                pro_uniprot_abbrv varchar(50) NOT NULL,
                PRIMARY KEY(pro_int_id)
                );
                ''')

    cur.execute('DROP TABLE IF EXISTS disease;')
    cur.execute('''CREATE TABLE disease (
                dis_int_id serial NOT NULL,
                dis_id varchar(12) NOT NULL,
                dis_omim_id varchar(6) NOT NULL,
                dis_uniprot_abbrv varchar(30) NOT NULL,
                PRIMARY KEY(dis_int_id)
                );
                ''')

    cur.execute('DROP TABLE IF EXISTS plant_vs_compound;')
    cur.execute('''CREATE TABLE plant_vs_compound (
                pla_id varchar(12) NOT NULL,
                com_id varchar(12) NOT NULL,
                weight float(3) NOT NULL,
                source varchar(128) NOT NULL,
                time_stamp timestamp  NOT NULL
                );
                ''')

    cur.execute('DROP TABLE IF EXISTS compound_vs_protein;')
    cur.execute('''CREATE TABLE compound_vs_protein (
                com_id varchar(12) NOT NULL,
                pro_id varchar(12) NOT NULL,
                weight float(3) NOT NULL,
                source varchar(256) NOT NULL,
                time_stamp timestamp  NOT NULL
                );
                ''')

    cur.execute('DROP TABLE IF EXISTS protein_vs_disease;')
    cur.execute('''CREATE TABLE protein_vs_disease (
                pro_id varchar(12) NOT NULL,
                dis_id varchar(12) NOT NULL,
                weight float(3) NOT NULL,
                source varchar(256) NOT NULL,
                time_stamp timestamp  NOT NULL
                );
                ''')

    conn.commit()
    print "Tables have created successfully"

    conn.close()

if __name__ == '__main__':
    main(sys.argv)
