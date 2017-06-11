# esvm_config.py

config = dict(name='esvm',
              kernel='rbf',
              mode='soft',
              bootstrap=True,
              dimred='pca',
              dimredNComponents=0.99,
              dimredSolver='full',
              dimredKernel='rbf',
              maxTestingSamplesPerBatch=1000,
              maxTrainingSamplesPerBatch=3000,
              maxNumberOfTrainingBatches=0)
