# insert_protein.py

def main():
    insertProtein(proteinList)

def insertProtein(proteinList):
    db = MySQLdb.connect("localhost","root","123","ijah" )
    cursor = db.cursor()

    for i,p in enumerate(proteinList):
        proId = str(i+1)
        proId = proId.zfill(8)
        proId = 'PRO'+proId
        print 'inserting ', proId, 'of', str(len(proteinList))

        proName, proUniprotId, proUniprotAbbrv = p
        pro = [proId, proName, proUniprotId, proUniprotAbbrv]
        pro = ['"'+i+'"' for i in pro]

        # Prepare SQL query to INSERT a record into the database.
        qf = 'INSERT INTO protein (pro_id,pro_name,pro_uniprot_id,pro_uniprot_abbrv) VALUES ('
        qm = pro[0]+','+pro[1]+','+pro[2]+','+pro[3]
        qr = ')'
        sql = qf+qm+qr
        # print sql

        try:
            cursor.execute(sql)
            db.commit()
        except:
            assert False, 'dbErr'
            db.rollback()

    db.close()

if __name__ == '__main__':
    main()
