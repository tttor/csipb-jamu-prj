# postgresql_util.py
import sys
import psycopg2

def getMax(csr,col,table):
    csr.execute("select max("+col+") from "+table)
    _ = csr.fetchall(); assert len(_)==1
    maxv = _[0][0]

    return maxv

def main(argv):
    assert len(argv)==6

    db = argv[1]
    user = argv[2]; passwd = argv[3]
    host = argv[4]; port = argv[5]

    conn = psycopg2.connect(database=db, user=user, password=passwd,
                            host=host, port=port)
    csr = conn.cursor()

    print getMax(csr,'com_id','compound')
    print getMax(csr,'pla_id','plant')

if __name__ == '__main__':
    main(sys.argv)
