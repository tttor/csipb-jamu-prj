# postgresql_util.py
import sys
import psycopg2

sys.path.append('../config')
from database_config import databaseConfig as dcfg

dbConn = psycopg2.connect(database=dcfg['name'],user=dcfg['user'],password=dcfg['passwd'],
                               host=dcfg['host'],port=dcfg['port'])
dbCsr = dbConn.cursor()

def drawKernel(idList):
    prefix = idList[0][0:3]
    tbl = None; col = None;
    if prefix=='COM':
        tbl = 'compound'
        col = 'com_similarity_simcomp'
    elif prefix=='PRO':
        tbl = 'protein'
        col = 'pro_similarity_smithwaterman'
    else:
        assert False, 'Unknown type'

    cond = ''
    for i,ii in enumerate(idList):
        if i>0:
            cond += " OR "
        cond += prefix.lower()+"_id="+quote(ii)

    q  = "SELECT "+col+" FROM "+tbl
    q += " WHERE "+cond
    dbCsr.execute(q)
    rows = dbCsr.fetchall()

    kernelDict = dict()
    for i,row in enumerate(rows):
        id1 = idList[i]

        row = row[0] # row initially is a 1-element tuple: (x,)
        if row!=None:
            comps = row.split(',')
            for comp in comps:
                subcomps = comp.split('=')
                id2 = subcomps[0].split(':')[0]
                sim = subcomps[1]
                kernelDict[ (id1,id2) ] = sim

    return kernelDict

def quote(s):
    s = s.replace("'","''") # escape any single quote
    s = "'"+s+"'"
    return s

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
