import numpy as np
import matplotlib.pyplot as plt



# Scenario 1
zooAll = np.loadtxt('/home/banua/xprmt/xprmt-icacsis16/zoo/matrixAccuracy-zoo-100-1.csv',
                    delimiter='\t')
maccsAll = np.loadtxt('/home/banua/xprmt/xprmt-icacsis16/maccs/matrixAccuracy-maccs-100-1.csv',
                    delimiter='\t')
jamuAll = np.loadtxt('/home/banua/xprmt/xprmt-icacsis16/jamu/matrixAccuracy-jamu-100-1.csv',
                    delimiter='\t')

# Scenario 2
zooHalf = np.loadtxt('/home/banua/xprmt/xprmt-icacsis16/zoo/matrixAccuracy-zoo-100-2.csv',
                    delimiter='\t')
maccsHalf = np.loadtxt('/home/banua/xprmt/xprmt-icacsis16/maccs/matrixAccuracy-maccs-100-2.csv',
                    delimiter='\t')
jamuHalf = np.loadtxt('/home/banua/xprmt/xprmt-icacsis16/jamu/matrixAccuracy-jamu-100-2.csv',
                    delimiter='\t')


barGpAll = [np.average(zooAll[0,:]), np.average(maccsAll[0, :]), np.average(jamuAll[0, :])]
barGpHalf = [np.average(zooHalf[0,:]), np.average(maccsHalf[0, :]), np.average(jamuHalf[0, :])]

barTan = [np.average(np.hstack((zooAll[100, :], zooHalf[100, :]))),
          np.average(np.hstack((maccsAll[100, :], maccsHalf[100, :]))),
          np.average(np.hstack((jamuAll[100, :], jamuHalf[100, :])))]

stdDevGpAll = [np.std(zooAll[0,:]), np.std(maccsAll[0, :]), np.std(jamuAll[0, :])]
stdDevGpHalf = [np.std(zooHalf[0,:]), np.std(maccsHalf[0, :]), np.std(jamuHalf[0, :])]
stdDevTan = [np.std(np.hstack((zooAll[100, :], zooHalf[100, :]))),
             np.std(np.hstack((maccsAll[100, :], maccsHalf[100, :]))),
             np.std(np.hstack((jamuAll[100, :], jamuHalf[100, :])))]


width = 0.2      # the width of the bars


fig, ax = plt.subplots()
rects1 = ax.bar([0.1, 0.8, 1.5], [i*100 for i in barGpAll], width, color='w',
                yerr=[i*100 for i in stdDevGpAll])
rects2 = ax.bar([0.3, 1.0, 1.7], [i*100 for i in barGpHalf], width, hatch = '////', color='w',
                yerr=[i*100 for i in stdDevGpHalf])
rects3 = ax.bar([0.5, 1.2, 1.9], [i*100 for i in barTan], width, hatch = '+++++', color='w',
                yerr=[i*100 for i in stdDevTan])

# add some text for labels, title and axes ticks
ax.set_ylabel('Classification Accuracy (%) using SVM')
#ax.set_title('Accuracy Scores')
ax.set_xticks([0.4, 1.1, 1.8])
ax.set_xticklabels(('Zoo', 'Compound', 'Jamu'))

ax.legend((rects1[0], rects2[0], rects3[0]),
          ('GP-Scenario1', 'GP-Scenario2', 'Tanimoto'), ncol=3,
          fontsize=10)


def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%.2f' % round(height,2)+'%',
                ha='center', va='bottom', fontsize = 8)

autolabel(rects1)
autolabel(rects2)
autolabel(rects3)

plt.ylim(0, 120)
plt.xlim(0, 2.2)
plt.xlabel('DATASET')
plt.grid(axis='y', which='major', alpha=0.5)
plt.show()
#plt.savefig('/home/banua/Dropbox/similarity-metric/fig/plot_accuracy.png', dpi=200)
