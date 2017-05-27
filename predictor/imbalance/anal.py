# anal.py
import os
import sys
import pickle
import json
from collections import defaultdict as ddict
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_auc_score
from sklearn.metrics import average_precision_score

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
   for d in dirs:
      with open(os.path.join(tdir,d,'result.pkl'),'r') as f: result = pickle.load(f)
      ytrue = result['yte']; ypred = result['ypred']; yscore = result['yscore']
      perfs['roc_auc_score'].append( roc_auc_score(ytrue,yscore,average='macro') )
      perfs['average_precision_score'].append( average_precision_score(ytrue,yscore,average='macro') )
      cms.append( confusion_matrix(ytrue,ypred) )

   with open(os.path.join(odir,'perfs.json'),'w') as f: json.dump(perfs,f,indent=2,sort_keys=True)

if __name__ == '__main__':
   main()
