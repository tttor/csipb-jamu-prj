import numpy as np
import util as utl
import threading
import time

def otu_pairwise(path, datakind):
    dataset = path
    rootdir = '/media/banua/Data/Kuliah/Destiny/Tesis/Program/csipb-jamu-prj.20160613.fixed/similarity-func/data/'

    data = np.loadtxt(rootdir+dataset, delimiter=",")
    data = data[:, 1:]
    otu_tuple = ()

    for i in range(0, len(data)):
        for j in range(i+1, len(data)):
            x1 = data[i, :]
            x2 = data[j, :]

            a = utl.getFeatureA(x1,x2); b = utl.getFeatureB(x1,x2)
            c = utl.getFeatureC(x1,x2); d = utl.getFeatureD(x1,x2)

            otu_tuple += ( (a, b, c, d) ),
            print 'pasangan {}  dan {}'.format(i, j)

    print len(data)

    otu_tuple = np.asarray(otu_tuple)

    np.savetxt(datakind+'-otu.csv', otu_tuple, delimiter="\t", fmt="%s")


try:
    (threading.Thread(target=otu_pairwise, args=('jamu/jamu_clean.csv', 'jamu'))).start()
    (threading.Thread(target=otu_pairwise, args=('stahl-maccs/stahl-maccs.csv', 'maccs'))).start()
    (threading.Thread(target=otu_pairwise, args=('zoo/zoo.csv', 'zoo'))).start()
except:
   print "Error: unable to start thread"