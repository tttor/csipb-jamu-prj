# util.py
import MySQLdb

def mysqlCommit(db, cursor, query, fetchall=False):
    try:
        cursor.execute(query)
        db.commit()

        if fetchall:
            return cursor.fetchall()
        else:
            return cursor.fetchone()
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        db.rollback()
        assert False, 'mySQL Error: '+str(e)

def mysqlExist(db,cursor,table,where):
    q = 'SELECT * FROM '+table+' WHERE ' + where
    exist = mysqlCommit(db, cursor,q)

    return (exist!=None)

def mysqlGetMax(db,cursor,table,col):
    q = 'SELECT MAX('+col+') AS m FROM '+table
    resp = mysqlCommit(db,cursor,q)
    resp = resp[0]

    if resp==None:
        resp = '0'

    return resp
