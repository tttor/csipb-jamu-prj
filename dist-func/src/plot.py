import numpy as np
import matplotlib.pyplot as plt

tmp = np.matrix(np.loadtxt('/home/banua/csipb-jamu-prj/dist-func/src/stat-20-500.csv', delimiter=','))

data = tmp[0, :]

lines = plt.plot(range(0,101), np.transpose(data))

plt.show()
