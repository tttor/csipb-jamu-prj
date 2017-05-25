# devel_config.py
config = dict(method='esvm',mode='hard',bootstrap=True,
              nClone=3, testSize=0.20,
              maxTrainingSamplesPerBatch=100,
              maxTestingSamplesPerBatch=100,maxTestingSamples=100,
              dataset='yamanishi#e',clusterMetric='calinskiharabaz',
              clusterDir='../cluster/output/cluster-3',
              datasetDir='../../dataset/connectivity/compound_vs_protein'
              )
