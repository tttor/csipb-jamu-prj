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
    if len(sys.argv)!=2:
        print 'USAGE:'
        print 'python cluster2.py [targetDir]'
        print '/param targetDir: dir containing one compound and one protein clustering results'
        return

    tdir = sys.argv[1]
    metrics = ['calinskiharabaz','silhouette']
    modes = ['compound','protein']

    ##
    print 'loading connMat...'
    dataset = tdir.split('/')[-1].split('-')[-1]
    dParam = dataset.split('#')
    dpath = os.path.join(DATASET_DIR,dParam[0],'ground-truth')
    connMat,comList,proList = yam.loadComProConnMat(dParam[1],dpath)
    nCom = len(comList); nPro = len(proList)

    ##
    print 'loading compound and protein clusters...'
    def _loadCluster(mode,metric):
        dname = [i for i in os.listdir(tdir) if (mode in i)][0]
        dpath = os.path.join(tdir,dname); assert os.path.isdir(dpath)
        item2clusterlabel = dict(); clusterlabel2item = defaultdict(list)
        fname = '_'.join(['cluster',mode,metric,'bestlabels.json'])
        with open(os.path.join(dpath,fname),'r') as f: item2clusterlabel = yaml.load(f)
        for k,v in item2clusterlabel.iteritems(): clusterlabel2item[v].append(k)
        return {'item2clusterlabel':item2clusterlabel,'clusterlabel2item':clusterlabel2item}

    clusterData = {}
    for mode in modes:
        for metric in metrics:
            clusterData[(mode,metric)] = _loadCluster(mode,metric)

    ##
    def _getNumberOfConnBetweenComProClusters(comMetric,proMetric):
        nConn = 0
        for comCluster in clusterData[('compound',comMetric)]['clusterlabel2item']:
            if (comCluster==-1): continue
            for proCluster in clusterData[('protein',proMetric)]['clusterlabel2item']:
                if (proCluster==-1): continue
                for com in clusterData[('compound',comMetric)]['clusterlabel2item'][comCluster]:
                    for pro in clusterData[('protein',proMetric)]['clusterlabel2item'][proCluster]:
                        conn = int( connMat[comList.index(com)][proList.index(pro)] )
                        if conn==1: nConn += 1
        return nConn

    connAmongComProClusters = dict()
    for comMet in metrics:
        for proMet in metrics:
            print 'get clusterConn of '+comMet+' and '+proMet
            connAmongComProClusters[(comMet,proMet)] =  _getNumberOfConnBetweenComProClusters(comMet,proMet)

    ##
    for comMet in metrics:
        for proMet in metrics:
            print 'getting connMat2 of '+comMet+' and '+proMet
            connMat2 = np.copy(connMat)
            for i in range(connMat.shape[0]):
                for j in range(connMat.shape[1]):
                    if connMat[i][j]==1: continue # because of known positive interaction
                    comCluster = clusterData[('compound',comMet)]['item2clusterlabel'][ comList[i] ]
                    proCluster = clusterData[('protein',proMet)]['item2clusterlabel'][ proList[i] ]
                    if (comCluster==-1)or(proCluster==-1): continue # because of outlier cluster label
                    if connAmongComProClusters[(comMet,proMet)]==0: connMat2[i][j] = -1

            connDict = defaultdict(list); connDict2 = defaultdict(list)
            connDictRaw = util.connMat2Dict(connMat2,comList,proList)
            for k,v in connDictRaw.iteritems(): connDict[int(v)].append(k)
            for k,v in connDict.iteritems(): connDict2[k].append(len(v))
            summ = sum([v[0] for v in connDict2.values()])
            for k,v in connDict2.iteritems(): connDict2[k].append(float(v[0])/summ)

            ##
            tag = '_'.join([comMet,proMet])
            # np.savetxt(os.path.join(tdir,tag+'_connMat.csv'),connMat2,delimiter=',')
            # with open(os.path.join(tdir,tag+"labels.json"),'w') as f:
            #     json.dump(connDict,f,indent=2,sort_keys=True)
            with open(os.path.join(tdir,tag+"_labels.pkl"),'w') as f:
                pickle.dump(connDict,f)
            with open(os.path.join(tdir,tag+"_labels_stat.json"),'w') as f:
                json.dump(connDict2,f,indent=2,sort_keys=True)

if __name__ == '__main__':
    tic = time.time()
    main()
    print "main took: "+str(time.time()-tic)+' seconds'
