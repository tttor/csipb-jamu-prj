# anal.py
import os
import sys
import pickle
import json
from collections import defaultdict as ddict
from sklearn.metrics import matthews_corrcoef
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import fbeta_score

def main():
   if len(sys.argv)!=3:
      print 'USAGE:'
      print 'python anal.py [targetDir] [tag]'
      return

   tdir = sys.argv[1]
   tag = sys.argv[2]

   odir = os.path.join(tdir,'anal_'+tag)
   if not os.path.exists(odir): os.makedirs(odir)

   perfs = ddict(list); cms = []
   dirs = [i for i in os.listdir(tdir) if (tag in i)and('anal' not in i)]; assert len(dirs)>0
   print dirs
   for d in dirs:
      with open(os.path.join(tdir,d,'result.pkl'),'r') as f: result = pickle.load(f)
      ytrue = result['yte']; ypred = result['ypred']
      perfs['matthews_corrcoef'].append( matthews_corrcoef(ytrue,ypred) )
      perfs['cohen_kappa_score'].append( cohen_kappa_score(ytrue,ypred) )
      perfs['fbeta_score'].append( fbeta_score(ytrue,ypred,average='binary',beta=0.5) )
      cms.append( confusion_matrix(ytrue,ypred) )

   with open(os.path.join(odir,'perfs.json'),'w') as f: json.dump(perfs,f,indent=2,sort_keys=True)

if __name__ == '__main__':
   main()
