# anal.py
import os
import sys
import pickle
import yaml
import matplotlib.pyplot as plt

metrics = ['calinskiharabaz','silhouette']

def main():
   if len(sys.argv)!=2:
      print 'USAGE:'
      print 'python anal.py [targetClusterDir]'
      return

   tdir = sys.argv[1]
   odir = os.path.join(tdir,'anal')
   if not os.path.exists(odir): os.makedirs(odir)

   # _pie(tdir,odir)
   _scatter(tdir,odir)

def _scatter(tdir,odir):
   odir = os.path.join(odir,'scatter')
   if not os.path.exists(odir): os.makedirs(odir)

   for d in [i for i in os.listdir(tdir) if not('anal' in i)]:
      fig = plt.figure()
      for d2 in [i for i in os.listdir(os.path.join(tdir,d)) if os.path.isdir(os.path.join(tdir,d,i))]:
         print d2
         dataset = d2.split('-')[2]
         c = 'r' if ('protein' in d2) else 'g'
         for fname in [i for i in os.listdir(os.path.join(tdir,d,d2)) if 'bestlabels_stat' in i]:
            m = '^' if 'silhouette' in fname else 'o'
            # tag = 'protein' if ('protein' in d2) else 'compound'
            # tag = '_silhouette' if 'silhouette' in fname else '_calinskiharabaz'
            with open(os.path.join(tdir,d,d2,fname),'r') as f:
               data = yaml.load(f)
               x = [int(i) for i in data.keys()]
               y = [i[0] for i in data.values()]
               plt.scatter(x,y,c=[c]*len(x),alpha=0.5,marker=m)
               plt.grid(True)
               plt.xlabel('class labels')
               plt.ylabel('#members')
               plt.savefig(os.path.join(odir,dataset+'_scatter.png'),
                           dpi=300,format='png',bbox_inches='tight')
      plt.close(fig)

def _pie(tdir,odir):
   for d in [i for i in os.listdir(tdir) if not('anal' in i)]:
      tag = d.split('-')[-1]; print d
      for m in metrics:
         with open(os.path.join(tdir,d,m+'_labels_stat.json')) as f:
            data = yaml.load(f); keys = data.keys()

            fig = plt.figure()
            plt.pie([data[k][0] for k in keys],
                     explode=[0.3 if (k=='0') else 0.0 for k in keys],labels=keys,autopct='%1.2f%%',
                     colors=['g' if (k=='1') else 'b' if (k=='-1') else 'r' for k in keys],
                     shadow=False, startangle=90)
            plt.axis('equal')
            plt.savefig(os.path.join(odir,tag+'_'+m+'_pie.png'),
                        dpi=300,format='png',bbox_inches='tight')
            plt.close(fig)

if __name__ == '__main__':
   main()
