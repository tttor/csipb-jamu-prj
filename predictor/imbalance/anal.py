# anal.py
import os
import sys
import pickle
import json
import itertools
import numpy as np
from collections import defaultdict as ddict
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_auc_score
from sklearn.metrics import average_precision_score
import matplotlib.pyplot as plt

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
   for i,d in enumerate(dirs):
      print 'anal on '+d+' '+str(i+1)+'/'+str(len(dirs))
      with open(os.path.join(tdir,d,'result.pkl'),'r') as f: result = pickle.load(f)
      ytrue = result['yte']; ypred = result['ypred']; yscore = result['yscore']; labels = list(set(ytrue))
      perfs['roc_auc_score'].append( roc_auc_score(ytrue,yscore,average='macro') )
      perfs['aupr_score'].append( average_precision_score(ytrue,yscore,average='macro') )
      cms.append( confusion_matrix(ytrue,ypred) )

   perfAvg = {}
   for m,v in perfs.iteritems(): perfAvg[m+'_avg'] = ( np.mean(v),np.std(v) )
   with open(os.path.join(odir,'perfs.json'),'w') as f: json.dump(perfs,f,indent=2,sort_keys=True)
   with open(os.path.join(odir,'perfAvg.json'),'w') as f: json.dump(perfAvg,f,indent=2,sort_keys=True)

   def _getBestIdx(metric):
      idx = perfs[metric].index( max(perfs[metric]) )
      return idx

   for m in perfs.keys():
      for n in ['normalized','unnormalized']:
         _plotCM(cms[_getBestIdx(m)],labels,n,os.path.join(odir,'cm_best_'+m+'_'+n+'.png'))

def _plotCM(cm,classes,normalized,fpath):
   """
   This function prints and plots the confusion matrix.
   Normalization can be applied by setting `normalize=True`.
   """
   fig = plt.figure()
   plt.imshow(cm, interpolation='nearest',cmap=plt.cm.Blues)
   plt.colorbar()
   tick_marks = np.arange(len(classes))
   plt.xticks(tick_marks, classes, rotation=45)
   plt.yticks(tick_marks, classes)
   if normalized=='normalized': cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
   thresh = cm.max() / 2.
   for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
     plt.text(j, i, cm[i, j],
              horizontalalignment="center",
              color="white" if cm[i, j] > thresh else "black")
   plt.ylabel('True label')
   plt.xlabel('Predicted label')
   plt.savefig(fpath,dpi=300,format='png',bbox_inches='tight')
   plt.close(fig)

if __name__ == '__main__':
   main()
