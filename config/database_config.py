# database_config.py
from credential import *

databaseConfigServer = dict(name='ijah',user='ijah',passwd=DB_PASSWD,
                            host=DB_HOST,port='5432')
databaseConfigLocal = dict(name='ijah',user='ijah',passwd=DB_PASSWD_LOCAL,
                            host='localhost',port='5432')

databaseConfig = databaseConfigServer
# databaseConfig = databaseConfigLocal
