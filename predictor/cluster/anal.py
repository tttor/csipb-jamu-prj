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

   _pie(tdir,odir)

def _pie(tdir,odir):
   for d in [i for i in os.listdir(tdir) if not('anal' in i)]:
      tag = d.split('-')[-1]; print d
      for m in metrics:
         with open(os.path.join(tdir,d,m+'_labels_stat.json')) as f:
            data = yaml.load(f)
            keys = sorted(data.keys())

            fig = plt.figure()
            plt.pie([data[k][0] for k in keys],
                     explode=[0.3 if (k=='0') else 0.0 for k in keys],
                     labels=keys, autopct='%1.2f%%', colors=['g','r','b'],
                     shadow=False, startangle=90)
            plt.axis('equal')
            plt.savefig(os.path.join(odir,tag+'_'+m+'_pie.png'),
                        dpi=300,format='png',bbox_inches='tight')
            plt.close(fig)

if __name__ == '__main__':
   main()
