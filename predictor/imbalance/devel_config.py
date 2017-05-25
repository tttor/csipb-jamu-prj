# devel_config.py
config = dict(method='esvm',mode='hard',bootstrap=True,
              nClone=3, testSize=0.30,
              maxTrainingSamplesPerBatch=10000,
              maxTestingSamplesPerBatch=100,maxTestingSamples=0,
              clusterMetric='calinskiharabaz',
              clusterDir='../cluster/output/cluster001-yamanishi#e',
              datasetDir='../../dataset/connectivity/compound_vs_protein'
              )
