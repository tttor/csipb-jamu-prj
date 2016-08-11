import numpy as np
from scipy.stats.stats import pearsonr
import matplotlib.pyplot as plt

rootdir = "/home/banua/xprmt/xprmt-icacsis16/"
dataset = 'zoo'
fname = rootdir+dataset+"/"+dataset+"_table_True.csv"

data = np.loadtxt(fname, delimiter="\t", dtype=str, usecols=(1, 2))
data = np.array(data).astype(np.float)

x = data[:, 0]
y = data[:, 1]

pval = np.corrcoef(x, y)
r_row, p_value = pearsonr(x, y)

plt.scatter(x, y)
plt.show()

print pval
print r_row
print p_value


