import numpy as np
import otu_table as ot
import time

__author__ = 'andpromobile'
# This file is used to generate value of attribute (a, b, c, d) each molecule pairwise

start = time.time()
data = np.loadtxt('semeion_data.csv', delimiter=',')
x = np.matrix(data)

val = np.array([])

for k in range(0, x.shape[0]):
    for l in range(k+1, x.shape[0]):
        a = x[k, :]
        b = x[l, :]

        print('pasangan', k, 'dan', l)
        d = ot.mol_count(a, b)

        if l == 1:
            val = d
        else:
            zz = np.vstack((val, d))
            val = zz

np.savetxt('pairwise_semeion_data.csv', val, fmt='%u', delimiter=',', newline='\n')
print 'It took', time.time()-start, 'seconds.'


