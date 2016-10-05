# util.py

import MySQLdb

def mysqlCommit(db, cursor, query):
    try:
        cursor.execute(query)
        db.commit()
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        db.rollback()
        assert False, 'mySQL Error: '+str(e)
        