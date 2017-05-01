# cluster2.py
import os
import sys
import yaml
import time
import numpy as np
from collections import defaultdict

sys.path.append('../../utility')
import yamanishi_data_util as yam

DATASET_DIR = '../../dataset/connectivity/compound_vs_protein'
XPRMT_DIR = '../../xprmt/cluster'

def main():
    if len(sys.argv)!=4:
        print 'USAGE:'
        print 'python cluster2.py [metric] [comClusterDir] [proClusterDir]'
        return

    metric = sys.argv[1]
    comClusterDir = sys.argv[2]
    proClusterDir = sys.argv[3]

    if metric=='cal':
        metric = 'calinskiharabaz'
    elif metric=='sil':
        metric = 'silhouette'
    else:
        assert False

    dataset = comClusterDir.split('-')[2]
    assert dataset==proClusterDir.split('-')[2]

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
        clusterDir = (comClusterDir if mode=='compound' else proClusterDir)
        with open(os.path.join(XPRMT_DIR,clusterDir,fname),'r') as f:
            cluster = yaml.load(f)

        cluster2 = defaultdict(list)
        for k,v in cluster.iteritems(): cluster2[v].append(k)

        return (cluster,cluster2)

    comCluster,comCluster2 = _loadCluster('compound')
    proCluster,proCluster2 = _loadCluster('protein')
    comList = comCluster.keys()
    proList = proCluster.keys()

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
            if (i==-1)or(j==-1): continue #outlier label
            clusterConn[(i,j)] = _getClusterConnection(i,j)

    ##
    print 'getting connMat2...'
    connMat2 = np.copy(connMat)
    count = 0
    for i in range(connMat.shape[0]):
        for j in range(connMat.shape[1]):
            count += 1
            print 'count= '+str(count)+'/'+str(connMat.size)

            if connMat[i][j]==1: continue

            comLabel = comCluster[ comList[i] ]
            proLabel = proCluster[ proList[j] ]
            if (comLabel==-1)or(proLabel==-1): continue #outlier label

            clsConn = _getClusterConnection(comLabel,proLabel)
            if clusterConn[(comLabel,proLabel)]==0:
                connMat2[i][j] = -1 # negative

if __name__ == '__main__':
    tic = time.time()
    main()
    print "main took: "+str(time.time()-tic)+' seconds'
