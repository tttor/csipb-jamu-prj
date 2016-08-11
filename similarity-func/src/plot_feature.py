import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# mpl.rcParams['font.size'] = 24.0


rootdir = '/home/banua/xprmt/xprmt-icacsis16/'
savedir = '/home/banua/Dropbox/similarity-metric/fig/'

print 'Loading Data....'
zoodata = np.loadtxt(rootdir+'zoo/zoo-otu.csv', delimiter='\t', dtype=float)
maccsdata = np.loadtxt(rootdir+'maccs/maccs-otu.csv', delimiter='\t', dtype=float)
jamudata = np.loadtxt(rootdir+'jamu/jamu-otu.csv', delimiter='\t', dtype=float)

print 'Sum Data'
zoodata = [np.sum(zoodata[:, i]) for i in range(0, zoodata.shape[1])]
maccsdata = [np.sum(maccsdata[:, i]) for i in range(0, maccsdata.shape[1])]
jamudata = [np.sum(jamudata[:, i]) for i in range(0, jamudata.shape[1])]

def plotpie(data, dataset):
    print 'Making Pie Chart.....'
    plt.clf()
    labels = 'a', 'b', 'c', 'd'

    sizes = data
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
    explode = (0, 0, 0, 0)  # only "explode" the 2nd slice

    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90)
    # # Set aspect ratio to be equal so that pie is drawn as a circle.
    plt.axis('equal')

    plt.show()
    # plt.savefig(savedir+dataset+'_pie.png')
    print 'Done !!!'



# plotpie(zoodata, 'ZOO')
# plotpie(maccsdata, 'MACCS')
plotpie(jamudata, 'JAMU')

#
# width = 1      # the width of the bars
#
# def plotbar(data, dataset):
#     fig, ax = plt.subplots()
#     rects1 = ax.bar([1, 2, 3, 4], data, width, color='w')
#     maxval = np.max(data)
#
#
#     # add some text for labels, title and axes ticks
#     ax.set_ylabel('number of features')
#     ax.set_xticks([1.5, 2.5, 3.5, 4.5])
#     ax.set_xticklabels(('a', 'b', 'c', 'd'))
#
#     autolabel(rects1, ax)
#
#     plt.xlabel(dataset+' DATASET')
#     plt.xlim(0, 6)
#     plt.grid(axis='y', which='major', alpha=0.5)
#     plt.show()
#     # plt.savefig(savedir+dataset+'.csv')
#
# def autolabel(rects, ax):
#     # attach some text labels
#     for rect in rects:
#         height = rect.get_height()
#         ax.text(rect.get_x() + rect.get_width()/2., 1.0001*height,
#                 '%d' % height,
#                 ha='center', va='bottom')
#
# print 'Making Bar Plot'
# plotbar(zoodata, 'ZOO')
# plotbar(maccsdata, 'COMPOUND')
# plotbar(jamudata, 'JAMU')
#
#
#

# fig, ax = plt.subplots()
# rects1 = ax.bar([1, 3, 5, 7], zoodata, width, color='w')
# rects2 = ax.bar([11, 13, 15, 17], maccsdata, width, hatch = '////', color='w')
# rects3 = ax.bar([21, 23, 25, 27], jamudata, width, hatch = '+++++', color='w')
#
# # add some text for labels, title and axes ticks
# ax.set_ylabel('number of features')
# ax.set_xticks([5, 15, 25])
# ax.set_xticklabels(('Zoo', 'Compound', 'Jamu'))
#
# # ax.legend((rects1[0], rects2[0], rects3[0]),
# #           ('GP-Scenario1', 'GP-Scenario2', 'Tanimoto'), ncol=3)
#
# #
# def autolabel(rects):
#     # attach some text labels
#     for rect in rects:
#         height = rect.get_height()
#         ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
#                 '%d' % height,
#                 ha='center', va='bottom')
#
# autolabel(rects1)
# autolabel(rects2)
# autolabel(rects3)
#
# # plt.ylim(0, 120)
# # plt.xlim(0, 4)
# plt.xlabel('DATASET')
# plt.grid(axis='y', which='major', alpha=0.5)
# plt.show()
# # plt.savefig(savedir+'feature_bar.png')
#
