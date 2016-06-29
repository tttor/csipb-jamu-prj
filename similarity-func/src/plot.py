import numpy as np
import matplotlib.pyplot as plt

# evenly sampled time at 200ms intervals
t = np.arange(0., 0.5, 1.0, 1.5, 2.0)


# red dashes, blue squares and green triangles
plt.plot(t, t, 'r--', t, t**2, 'bs', t, t**3, 'g^')
plt.show()

# x = np.array([[0.1, 0.04],
#               [0.2, 0.08],
#               [0.3, 0.12],
#               [0.4, 0.16],
#               [0.5, 0.2]])
#
# y = np.array([[0.5, 01]])
#
# for i in range(0, len(y)):
#     tmp = np.matrix(np.loadtxt('/media/banua/Data/Kuliah/Destiny/Tesis/Program/hasil/syahid/Fitness -Tan-GP-10-100-stats.csv', delimiter=','))
#     #  /home/banua/csipb-jamu-prj/dist-func/src/stat-20-500.csv
#     data = tmp[0, :]
#
#     y = np.max(data)
#
#
#     lines = plt.plot(range(0,101), np.transpose(data), range(0,101), 3*(np.transpose(data)))
#
#     # plt.axhline(y = 1, linewidth=0.5, color='r')
#     plt.ylim(0.5, int(y)+1)
#
#     plt.xlabel('Generasi')
#     plt.ylabel('Nilai Fitness')
#     plt.title('Genetic Programming. \n #Gen : 100; #Pop : 10; Pc = 0.5; Pm = 0.1')
#
#     plt.show()
