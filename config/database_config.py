# database_config.py
from credential import *

DB_MODE = 'server'
DB_MODE = 'local'

DB_PASSWD = None
DB_HOST = None
if DB_MODE=='server':
    DB_PASSWD = DB_PASSWD_SERVER
    DB_HOST = DB_HOST_SERVER
elif DB_MODE=='local':
    DB_PASSWD = DB_PASSWD_LOCAL
    DB_HOST = DB_HOST_LOCAL
else:
    assert False,'FATAL: Unknown DB_MODE'

databaseConfig = dict(name='ijah',
                      user='ijah',passwd=DB_PASSWD,
                      host=DB_HOST,port='5432')
