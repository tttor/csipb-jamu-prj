# anal.py
import os
import sys
import pickle
import json
import yaml
import h5py
import itertools
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict as ddict
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_auc_score
from sklearn.metrics import average_precision_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import fbeta_score
from sklearn.metrics import matthews_corrcoef

def main():
   if len(sys.argv)!=2:
      print 'USAGE:'
      print 'python anal.py [targetDevelDir]'
      return

   tdir = sys.argv[1]

   odir = os.path.join(tdir,'anal')
   if not os.path.exists(odir): os.makedirs(odir)

   perfs = ddict(list); cms = []
   tags = [i.split('.')[0].replace('result_','') for i in os.listdir(tdir) if 'result' in i]
   tags = sorted(tags)

   with open(os.path.join(tdir,'devLog_'+tags[0]+'.json'),'r') as f:
      labels = yaml.load(f)['labels']

   relDict = ddict(list)
   delim = '__'
   for i,tag in enumerate(tags):
      print 'anal on '+tag+' '+str(i+1)+'/'+str(len(tags))

      rfpath = os.path.join(tdir,'result_'+tag+'.h5')
      with h5py.File(rfpath,'r') as f:
         ytrue = f['yte'][:]; ypred = f['ypred'][:]; yscore = f['yscore'][:]
         yrel = f['yrel'][:]; yrelscore = f['yrelscore'][:]; xrelraw = f['xrelraw'][:]

      perfs['roc_auc_score'].append( roc_auc_score(ytrue,yscore,average='macro') )
      perfs['aupr_score'].append( average_precision_score(ytrue,yscore,average='macro') )
      perfs['accuracy_score'].append( accuracy_score(ytrue,ypred) )
      perfs['cohen_kappa_score'].append( cohen_kappa_score(ytrue,ypred) )
      perfs['fbeta_score'].append( fbeta_score(ytrue,ypred,average='macro',beta=0.5) )
      perfs['matthews_corrcoef'].append( matthews_corrcoef(ytrue,ypred) )
      cms.append( confusion_matrix(ytrue,ypred,labels) )

      for i,ii in enumerate(xrelraw):
         relDict[delim.join(ii)].append( str(yrel[i])+delim+str(yrelscore[i]) )

   print 'writing perfs...'
   perfAvg = {}
   for m,v in perfs.iteritems():
      perfAvg[m+'_avg'] = ( np.mean(v),np.std(v) )
   with open(os.path.join(odir,'perfAvg.json'),'w') as f:
      json.dump(perfAvg,f,indent=2,sort_keys=True)

   perfs['tags'] = tags
   with open(os.path.join(odir,'perfs.json'),'w') as f:
      json.dump(perfs,f,indent=2,sort_keys=True)

   print 'writing release...'
   relPosProbs = []; relNegProbs = []
   for k,v in relDict.iteritems():
      labels = [int(i.split(delim)[0]) for i in v]
      probs = [float(i.split(delim)[1]) for i in v]

      maxProb = max(probs)
      maxProbLabel = labels[ probs.index(maxProb) ]

      if maxProbLabel==1:
         vpos = (k,maxProb)
         vneg = (k,1.0-maxProb)
      else:
         vneg = (k,maxProb)
         vpos = (k,1.0-maxProb)
      relPosProbs.append(vpos)
      relNegProbs.append(vneg)

   with open(os.path.join(odir,'release.json'),'w') as f:
      json.dump(relDict,f,indent=2,sort_keys=True)
   with open(os.path.join(odir,'releaseMaxProbPos.json'),'w') as f:
      json.dump(relPosProbs,f,indent=2,sort_keys=True)
   with open(os.path.join(odir,'releaseMaxProbNeg.json'),'w') as f:
      json.dump(relNegProbs,f,indent=2,sort_keys=True)

   def plotHist(vals,normalized,tag):
      histRange = (0.0,1.0); histInc = 0.05
      histBins = np.arange(histRange[0],histRange[1]+histInc,histInc)
      weights = np.ones_like(vals)/float(len(vals))

      fig = plt.figure()
      plt.xlabel('probability')
      plt.xticks(np.arange(0.0,1.0+0.1,0.1))
      fname = tag
      if normalized:
         plt.hist(vals,weights=weights,normed=False,
                  bins=histBins,range=histRange)
         plt.ylabel('#data (normalized)')
         plt.yticks(np.arange(0.0,1.0+0.1,0.1))
         fname += '_norm'
      else:
         plt.hist(vals,normed=False,
                  bins=histBins,range=histRange)
         plt.ylabel('#data')
      plt.grid();
      plt.savefig(os.path.join(odir,fname+'.png'),
                dpi=300,format='png',bbox_inches='tight');
      plt.close(fig)

   for norm in [True,False]:
      plotHist([i[1] for i in relPosProbs],norm,'releaseMaxProbPosHist')
      plotHist([i[1] for i in relNegProbs],norm,'releaseMaxProbNegHist')

   print 'writing cm...'
   def _getBestIdx(metric):
      idx = perfs[metric].index( max(perfs[metric]) )
      return idx

   m = 'aupr_score'
   for n in ['normalized','unnormalized']:
      _plotCM(cms[_getBestIdx(m)],labels,n,os.path.join(odir,'cm_best_'+m+'_'+n+'.png'))

def _plotCM(cm,classes,normalized,fpath):
   """
   This function prints and plots the confusion matrix.
   Normalization can be applied by setting `normalize=True`.
   """
   fig = plt.figure()
   tick_marks = np.arange(len(classes))
   plt.xticks(tick_marks, classes, rotation=45)
   plt.yticks(tick_marks, classes)
   if normalized=='normalized': cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
   plt.imshow(cm, interpolation='nearest',cmap=plt.cm.Blues); plt.colorbar()
   thresh = cm.max() / 2.
   for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
     plt.text(j, i, cm[i, j], horizontalalignment="center",
              color="white" if cm[i, j] > thresh else "black")
   plt.ylabel('True label')
   plt.xlabel('Predicted label')
   plt.savefig(fpath,dpi=300,format='png',bbox_inches='tight')
   plt.close(fig)

if __name__ == '__main__':
   main()
