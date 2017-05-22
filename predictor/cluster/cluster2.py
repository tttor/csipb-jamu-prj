# cluster2.py
import os
import sys
import yaml
import time
import json
import pickle
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from scoop import futures as fu
from scoop import shared as sh

sys.path.append('../../utility')
import yamanishi_data_util as yam
import util

DATASET_DIR = '../../dataset/connectivity/compound_vs_protein'
XPRMT_DIR = '../../xprmt/cluster'

def main():
    if len(sys.argv)!=3:
        print 'USAGE:'
        print 'python cluster2.py [metric] [targetDir]'
        print '/param metric: cal, sil'
        print '/param targetDir: dir containing compound and protein clustering results'
        return

    metric = sys.argv[1]
    tDir = sys.argv[2]

    dirs = os.listdir(tDir); clusterDirs = {}
    clusterDirs['compound'] = [i for i in dirs if ('compound' in i)and('cluster' in i)]
    clusterDirs['protein'] = [i for i in dirs if ('protein' in i)and('cluster' in i)]

    # For now, take only the first cluster dir
    clusterDirs['compound'] = clusterDirs['compound'][0]
    clusterDirs['protein'] = clusterDirs['protein'][0]

    dataset = clusterDirs['compound'].split('-')[2]
    assert dataset==clusterDirs['protein'].split('-')[2]

    if metric=='cal': metric = 'calinskiharabaz'
    elif metric=='sil': metric = 'silhouette'
    else: assert False

    ##
    print 'loading connMat...'
    dParam = dataset.split('#')
    dpath = os.path.join(DATASET_DIR,dParam[0],'ground-truth')
    connMat,comList,proList = yam.loadComProConnMat(dParam[1],dpath)
    nCom = len(comList); nPro = len(proList)

    ##
    print 'loading cluster...'
    def _loadCluster(mode):
        fname = '_'.join(['cluster',mode,metric,'bestlabels.json'])
        with open(os.path.join(tDir,clusterDirs[mode],fname),'r') as f:
            cluster = yaml.load(f)

        cluster2 = defaultdict(list)
        for k,v in cluster.iteritems(): cluster2[v].append(k)

        return (cluster,cluster2)

    comCluster,comCluster2 = _loadCluster('compound')
    proCluster,proCluster2 = _loadCluster('protein')

    ##
    print 'get clusterConn...'
    def _getClusterConnection(comLabel,proLabel):
        nConn = 0
        for i in comCluster2[comLabel]:
            for j in proCluster2[proLabel]:
                conn = int( connMat[comList.index(i)][proList.index(j)])
                if conn == 1: nConn += 1
        return nConn

    clusterConn = dict()
    for i in comCluster2.keys():
        for j in proCluster2.keys():
            if (i==-1)or(j==-1): continue #outlier
            clusterConn[(i,j)] = _getClusterConnection(i,j)

    ##
    print 'getting connMat2...'
    connMat2 = np.copy(connMat)
    count = 0
    for i in range(connMat.shape[0]):
        for j in range(connMat.shape[1]):
            count += 1
            if (count%10000)==0:
                print 'count= '+str(count)+'/'+str(connMat.size)

            if connMat[i][j]==1: continue
            comLabel = comCluster[ comList[i] ]
            proLabel = proCluster[ proList[j] ]
            if (comLabel==-1)or(proLabel==-1): continue #outlier label

            if clusterConn[(comLabel,proLabel)]==0:
                connMat2[i][j] = -1 # negative

    connDict = defaultdict(list); connDict2 = {}
    connDictRaw = util.connMat2Dict(connMat2,comList,proList)
    for k,v in connDictRaw.iteritems(): connDict[int(v)].append(k)
    for k,v in connDict.iteritems(): connDict2[k] = len(v)

    ##
    print 'writing...'
    fpath = os.path.join(tDir,metric+'_connMat.csv')
    np.savetxt(fpath,connMat2,delimiter=',')

    with open(os.path.join(tDir,metric+"_connDict.json"),'w') as f:
        json.dump(connDict,f,indent=2,sort_keys=True)
    with open(os.path.join(tDir,metric+"_connDict.pkl"),'w') as f:
        pickle.dump(connDict,f)
    with open(os.path.join(tDir,metric+"_connDict2.json"),'w') as f:
        json.dump(connDict2,f,indent=2,sort_keys=True)

    fig = plt.figure()
    _ = [(k,v) for k,v in connDict2.iteritems()]
    plt.pie([i[1] for i in _], explode=[0.3 if (i[0]==0) else 0.0 for i in _],
         labels=[i[0] for i in _], autopct='%1.2f%%',
         shadow=False, startangle=90)
    plt.axis('equal')
    plt.savefig(os.path.join(tDir,metric+'_conn_pie.png'),
                dpi=300,format='png',bbox_inches='tight')
    plt.close(fig)

if __name__ == '__main__':
    tic = time.time()
    main()
    print "main took: "+str(time.time()-tic)+' seconds'
