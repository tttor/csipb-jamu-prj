# devel_config.py
config = dict(method='esvm',mode='soft',bootstrap=True,
              testSize=0.30,
              maxTrainingSamplesPerBatch=10000,
              maxTestingSamplesPerBatch=100,
              maxTestingSamples=0,
              datasetDir='../../dataset/connectivity/compound_vs_protein'
              )
