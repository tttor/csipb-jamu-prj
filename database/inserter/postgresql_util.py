# postgresql_util.py
import sys
import psycopg2

def getMax(csr,col,table):
    csr.execute("SELECT MAX("+col+") FROM "+table)
    _ = csr.fetchall(); assert len(_)==1
    maxv = _[0][0]
    return maxv

def doesExist(csr,table,col,val):
    csr.execute("SELECT * FROM "+table+" WHERE "+col+"="+"'"+val+"'")
    _ = csr.fetchall();
    return len(_)!=0

def main(argv):
    assert len(argv)==6

    db = argv[1]
    user = argv[2]; passwd = argv[3]
    host = argv[4]; port = argv[5]

    conn = psycopg2.connect(database=db, user=user, password=passwd,
                            host=host, port=port)
    csr = conn.cursor()

    ###
    # print getMax(csr,'com_id','compound')
    # print getMax(csr,'pla_id','plant')

    ###
    # print doesExist(csr,'compound','com_drugbank_id','DB08427')

    ###
    q = "select com_similarity_simcomp from compound where com_kegg_id='C07619';"
    q = "select pro_similarity_smithwaterman from protein where pro_uniprot_id='Q53R12'"
    csr.execute(q)
    resp = csr.fetchall()
    print len(resp)
    print resp[0]

if __name__ == '__main__':
    main(sys.argv)
