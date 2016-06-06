import numpy as np
import matplotlib.pyplot as plt

x = np.array([[0.1, 0.04],
              [0.2, 0.08],
              [0.3, 0.12],
              [0.4, 0.16],
              [0.5, 0.2]])

for i in range(0, len(x)):
    tmp = np.matrix(np.loadtxt('/home/banua/Documents/hasil1Juni2016/zoo/'+str(i+1)+'- fitness - Tan-GP-100-100-stats.csv', delimiter=','))
    #  /home/banua/csipb-jamu-prj/dist-func/src/stat-20-500.csv
    data = tmp[0, :]

    y = np.max(data)


    lines = plt.plot(range(0,101), np.transpose(data))

    plt.axhline(y = 1, linewidth=0.5, color='r')
    plt.ylim(0.5, int(y)+1)

    plt.xlabel('Generasi')
    plt.ylabel('Nilai Fitness')
    plt.title('Genetic Programming. \n #Gen : 100; #Pop : 100; Pc = ' + str(x[i, 0]) + '; Pm = ' + str(x[i, 1]) + '')

    plt.show()
