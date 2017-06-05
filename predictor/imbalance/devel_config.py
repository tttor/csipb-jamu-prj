# devel_config.py
esvm_config =  dict(name='esvm',kernel='rbf',mode='soft',bootstrap=True,
                    maxTrainingSamplesPerBatch=10000,
                    maxTestingSamplesPerBatch=100,
                    maxNumberOfSVM=1)

svm_config = dict(name='psvm',kernel='rbf') # psvm: plain svm

config = dict(method=esvm_config,
              testSize=0.30,
              maxTestingSamples=0,
              smoteBatchSize=10000,
              maxNumberOfSmoteBatch=0,
              comKernel='rbf',proKernel='rbf',
              datasetDir='../../dataset/connectivity/compound_vs_protein')
