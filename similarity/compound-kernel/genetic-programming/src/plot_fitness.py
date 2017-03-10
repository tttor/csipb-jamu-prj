import numpy as np
import matplotlib.pyplot as plt


figSaveDir = '/home/banua/Dropbox/similarity-metric/fig/'

datasetzoo = 'zoo'
datasetmaccs = 'maccs'
datasetjamu = 'jamu'

sce = '2'


fnameMaxZoo = '/home/banua/xprmt/xprmt-icacsis16/'+datasetzoo+'/matrixMax-zoo-'+sce+'.csv'
fnameMaxMaccs = '/home/banua/xprmt/xprmt-icacsis16/'+datasetmaccs+'/matrixMax-maccs-'+sce+'.csv'
fnameMaxJamu = '/home/banua/xprmt/xprmt-icacsis16/'+datasetjamu+'/matrixMax-jamu-'+sce+'.csv'

x = np.arange(101)

maxZoo = np.loadtxt(fnameMaxZoo, delimiter='\t')
maxzoostd = [np.std(maxZoo[i, :]) for i in range(0, maxZoo.shape[0])]
maxZoo = [np.average(maxZoo[i, :]) for i in range(0, maxZoo.shape[0])]


maxMaccs = np.loadtxt(fnameMaxMaccs, delimiter='\t')
maxMaccsstd = [np.std(maxMaccs[i, :]) for i in range(0, maxMaccs.shape[0])]
maxMaccs = [np.average(maxMaccs[i, :]) for i in range(0, maxMaccs.shape[0])]

maxJamu = np.loadtxt(fnameMaxJamu, delimiter='\t')
maxJamustd = [np.std(maxJamu[i, :]) for i in range(0, maxJamu.shape[0])]
maxJamu = [np.average(maxJamu[i, :]) for i in range(0, maxJamu.shape[0])]

fig, ax = plt.subplots()

plt.xlabel('i-th GENERATION')
plt.ylabel('MAXIMUM Fitness Values')


stdscale = 0.2
plt.fill_between(x, np.array(maxZoo) - (stdscale*np.array(maxzoostd)),
                 np.array(maxZoo) + (stdscale*np.array(maxzoostd)),
                 alpha = 0.5, edgecolor = 'r', facecolor = 'r',
                 linewidth = 2, linestyle = '-', antialiased = True)

plt.fill_between(x, np.array(maxMaccs) - (stdscale * np.array(maxMaccsstd)),
                 np.array(maxMaccs) + (stdscale * np.array(maxMaccsstd)),
                 alpha=0.5, edgecolor='g', facecolor='g',
                 linewidth=2, linestyle='-', antialiased=True)

plt.fill_between(x, np.array(maxJamu) - (stdscale * np.array(maxJamustd)),
                 np.array(maxJamu) + (stdscale * np.array(maxJamustd)),
                 alpha=0.5, edgecolor='b', facecolor='b',
                 linewidth=2, linestyle='-', antialiased=True)

plt.plot(x, maxZoo, color='r', ls='-', linewidth=1.5)
plt.plot(x, maxMaccs, color='g', ls='-', linewidth=1.5)
plt.plot(x, maxJamu, color='b', ls='-', linewidth=1.5)

plt.legend(['Zoo', 'Compound', 'Jamu'], loc='lower right')
plt.grid()

# plt.title('Genetic Programming on datasetzoo '+datasetzoo)
plt.ylim(355, 395)
# plt.show()
plt.savefig(figSaveDir+'plot_fitness_max_scenario_'+sce+'.png')


