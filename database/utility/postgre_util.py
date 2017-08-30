# postgre_util.py

def delete(tables,csr):
  for t,seq in tables:
    print 'deleting rows of table= '+t
    q = 'DELETE FROM '+t
    csr.execute(q)

    if seq is not None:
      print 'restarting seq= '+seq
      q = 'ALTER SEQUENCE '+seq+' RESTART WITH 1;'
      csr.execute(q)

def insert(table,cols,vals,csr,debug=False):
  q = 'INSERT INTO '+table+' '+bracket(','.join(cols))
  q+= ' VALUES '+bracket(','.join([quote(i) for i in vals]))
  if debug: print q
  csr.execute(q)

def select(col,table,colCond,cond,csr):
  q = 'SELECT '+col+' FROM '+table
  q+= ' WHERE '+colCond+'='+quote(cond)
  csr.execute(q)
  rows = csr.fetchall()
  return rows

def selectMax(col,table,csr):
  q = "SELECT MAX("+col+") FROM "+table
  csr.execute(q)
  rows = csr.fetchall()
  return rows[0][0]

def getID(col,table,colCond,cond,csr):
  q = 'SELECT '+col+' FROM '+table
  q+= ' WHERE '+colCond+'='+quote(cond)
  csr.execute(q)
  rows = csr.fetchall();
  if len(rows)==1:
    ids = rows[0][0]
  else:
    ids = -1 # not found
  return int(ids)

def quote(v):
  s = str(v)
  if not( isinstance(v, (int, long, float)) ):
    s = s.replace("'","''") # escape any single quote
    s = "'"+s+"'"
  return s

def bracket(s):
  return '('+s+')'