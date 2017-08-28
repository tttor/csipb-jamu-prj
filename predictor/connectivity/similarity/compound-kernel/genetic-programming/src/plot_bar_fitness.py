import numpy as np
import matplotlib.pyplot as plt


def plotBarFitness(data):
    rootDir = '/home/banua/xprmt/xprmt-icacsis16/'
    datasetName = data

    dataSc1 = np.loadtxt(rootDir+datasetName+'/matrixFitness-'+datasetName+'-100-1.csv')
    dataSc2 = np.loadtxt(rootDir+datasetName+'/matrixFitness-'+datasetName+'-100-2.csv')

    dataSc1 = [np.average(dataSc1[i, :]) for i in range(dataSc1.shape[0])]
    dataSc2 = [np.average(dataSc2[i, :]) for i in range(dataSc2.shape[0])]

    dataRankSc1 = dataSc1[0:100]
    dataRankSc2 = dataSc2[0:100]

    n = len(dataRankSc1)

    xval = np.arange(n)
    width = 4

    xticks = np.arange(2, 398, 36)
    xtickslabel = np.arange(0, 101, 10)
    xtickslabel[0] = 1

    xticks = xticks + [0, 0, 4, 8, 12, 16, 20, 24, 28, 32, 36]

    fig, ax = plt.subplots(figsize=(10000, 5))
    rects1 = ax.bar(xval*4, dataRankSc1, width, color='g')
    rects2 = ax.bar([i+(0.4*width) for i in xval*4], dataRankSc2, width*0.3, color='r')

    ax.set_ylabel('Fitness Values')
    ax.set_xlabel('i-th Individual Rank over the entire evolution')
    # ax.set_title('gen 0 : Random All')
    ax.set_xticks(xticks)
    ax.set_xticklabels(xtickslabel)

    ax.legend((rects1[0],rects2[0]),('GP-Scenario-1','GP-Scenario-2'), ncol=2)

    plt.ylim(380, 394)
    plt.grid(axis='y', which='major', alpha=0.5)
    plt.show()
    #plt.savefig('/home/banua/Dropbox/similarity-metric/fig/plot-bar-fitness-'+datasetName+'.png')
    # print '{} : Max Values ({}) and Min Values ({}) for scenario 1 \n Max Values ({}) and Min Values ({}) for scenario 2'.\
    #     format(datasetName, np.max(dataRankSc1), np.min(dataRankSc1), np.max(dataRankSc2), np.min(dataRankSc2))

plotBarFitness('zoo')
plotBarFitness('maccs')
plotBarFitness('jamu')
