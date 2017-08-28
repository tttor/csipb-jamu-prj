# esvm_config.py

config = dict(name='esvm',
              kernel='rbf',
              mode='soft',
              bootstrap=True,
              dimred='pca',
              dimredNComponents=0.90,
              dimredSolver='full',
              dimredKernel='rbf', # iff dimred=='kpca'
              maxTestingSamplesPerBatch=1000,
              maxTrainingSamplesPerBatch=3000,
              maxNumberOfTrainingBatches=0)
