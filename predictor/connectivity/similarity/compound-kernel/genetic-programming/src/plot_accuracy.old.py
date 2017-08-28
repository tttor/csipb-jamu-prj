import numpy as np
import matplotlib.pyplot as plt

dataset = 'maccs'
targetDir = '/home/banua/xprmt/xprmt-icacsis16/'+dataset
data = np.loadtxt(targetDir+'/matrixAccuracy-2.csv', delimiter='\t')


dataset2 = 'zoo'
targetDir2 = '/home/banua/xprmt/xprmt-icacsis16/'+dataset2
data2 = np.loadtxt(targetDir2+'/matrixAccuracy-2.csv', delimiter='\t')


N = data.shape[0]

stddev = [np.std(data[i, :]) for i in range(N)]
stddev2 = [np.std(data2[i, :]) for i in range(N)]
data = [np.average(data[i, :]) for i in range(N)]
data2 = [np.average(data2[i, :]) for i in range(N)]

# print data
# assert False

ind = np.arange(N)  # the x locations for the groups
width = 0.35      # the width of the bars

print data
print data2
print data

data3 = zip(data, data2, data)
stddev3 = zip(stddev, stddev2, stddev)

print data3
# data3 = np.asarray(data3)
# # #
# # #
# print data3
# # print data3.shape
#
# assert False

fig, ax = plt.subplots()
rects1 = ax.bar([0.2, 1.3, 2.3], [i*100 for i in data3[0]], width, color='w', yerr=[i*100 for i in stddev3[0]])
rects2 = ax.bar([0.55, 1.65, 2.65], [i*100 for i in data3[1]], width, hatch = '////', color='w', yerr=[i*100 for i in stddev3[1]])


# add some text for labels, title and axes ticks
ax.set_ylabel('Accuracy')
ax.set_title('Accuracy Scores')
ax.set_xticks([0.55, 1.65, 2.65])
ax.set_xticklabels(('Maccs', 'Zoo', 'Jamu'))

ax.legend((rects1[0], rects2[0]),
          ('GP', 'Tanimoto'), ncol=3)


def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%.2f' % round(height,2)+'%',
                ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)

plt.ylim(0, 120)
plt.xlim(0, 3.2)

plt.show()