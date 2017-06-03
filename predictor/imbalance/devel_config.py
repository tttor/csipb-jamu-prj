# devel_config.py
esvm_config =  dict(name='esvm',mode='soft',bootstrap=True,
                    maxTrainingSamplesPerBatch=10000,
                    maxTestingSamplesPerBatch=100)

svm_config = dict(name='psvm') # psvm: plain svm

config = dict(method=esvm_config,
              testSize=0.30,
              maxTestingSamples=0,
              smoteBatchSize=10000,
              datasetDir='../../dataset/connectivity/compound_vs_protein')
