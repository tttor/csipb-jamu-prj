# esvm_config.py

config = dict(name='esvm',
              kernel='rbf',
              mode='soft',
              bootstrap=True,
              maxTestingSamplesPerBatch=100,
              maxTrainingSamplesPerBatch=10000,
              maxNumberOfTrainingBatches=1)
