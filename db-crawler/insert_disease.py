# insert_disease.py

def main():
    insertDisease(diseaseList)

def insertDisease(diseaseList):
    #
    db = MySQLdb.connect("localhost","root","123","ijah" )
    cursor = db.cursor()

    for i,d in enumerate(diseaseList):
        disId = str(i+1)
        disId = disId.zfill(8)
        disId = 'DIS'+disId
        print 'inserting ', disId, 'of', str(len(diseaseList))

        disName, disAbbrv, disOmimId = d
        dis = [disId,disName,disOmimId,disAbbrv]
        dis = ['"'+i+'"' for i in dis]

        # Prepare SQL query to INSERT a record into the database.
        qf = 'INSERT INTO disease (dis_id,dis_name,dis_omim_id,dis_uniprot_abbrv) VALUES ('
        qm = dis[0]+','+dis[1]+','+dis[2]+','+dis[3]
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
