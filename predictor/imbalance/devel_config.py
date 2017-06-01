# devel_config.py
esvm_config =  dict(name='esvm',mode='soft',bootstrap=True,
                    maxTrainingSamplesPerBatch=10000,
                    maxTestingSamplesPerBatch=100)

config = dict(method=esvm_config,
              testSize=0.30,
              maxTestingSamples=0,
              datasetDir='../../dataset/connectivity/compound_vs_protein')
