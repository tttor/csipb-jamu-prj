# esvm_config.py

config = dict(name='esvm',
              kernel='rbf',
              mode='soft',
              bootstrap=True,
              maxTrainingSamplesPerBatch=10000,
              maxTestingSamplesPerBatch=100,
              maxNumberOfSVM=1)
