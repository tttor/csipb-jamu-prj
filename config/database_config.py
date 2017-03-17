# database_config.py
from credential import *

databaseConfigServer = dict(name='ijah',user='ijah',passwd=DB_PASSWD,
                            host=DB_HOST,port='5432')
databaseConfigLocal = dict(name='ijah',user='ijah',passwd=DB_PASSWD_LOCAL,
                            host='localhost',port='5432')

databaseConfig = None
if DB_MODE=='server':
    databaseConfig = databaseConfigServer
elif DB_MODE=='local':
    databaseConfig = databaseConfigLocal
else:
    assert False,'FATAL: Unknown DB_MODE'
