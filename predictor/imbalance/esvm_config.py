# esvm_config.py

config = dict(name='esvm',
              kernel='rbf',
              mode='soft',
              bootstrap=True,
              maxTestingSamplesPerBatch=1000,
              maxTrainingSamplesPerBatch=3000,
              maxNumberOfTrainingBatches=0)
