# Compound-protein connectivity prediction

## Aliases and Keywords
* compound-protein/drug-target interaction/link prediction
* in-silico/virtual/computational drug screening

## Challenges
* imbalanced data, highly skewed datasets: small number of positive samples (known interactions)
    * current solution: train locally in that
    the training data are drawn locally ``near'' the testing compound-protein pairs.
    This helps reducing irrelevant training data wrt the testing data.
    This means that each testing compound-protein pair has its own model/classifier,
    which is computationally expensive
* deceptive negative samples as they can be either trully negative or simply unknown (not yet clinically/chemically tested)
    * validated negative samples are not available;
      people never report negative results after clinical/chemical experiments
    * negative samples that actually positive may fool the learning machine;
      they are negative because their true interactions are simply unknown/not-tested
* handle 4 scenarios: (new: having no existing/known interaction)
    * Known drug, known target
    * New drug, known target
    * Known drug, new target
    * New drug, new target (hardest)
* features _and_ similarity (kernel) functions of compounds, proteins and their interactions
    * compound/chemical features/kernels
    * protein/biological/genomic features/kernels
    * compound-protein interaction/network/pharmacological features/kernels

## Supervised ML-based approaches
* BLM (Bipartite Local Model)
  * Original
    * Yamanishi (2010)
    * Bleakley (2009)
    * Yamanishi (2008)
  * BLM-NII (bipartite local model with neighbor-based inferring) or Globalized BLM
    * Mei (2013)
    * Mei (2012)
* Kernel-based
  * Kronecker regularized least squares (KronRLS)
    * Laarhoven (2011): KronRLS+GIP (_not_ handle new drugs/targets)
    * Laarhoven (2013): KronRLS+WNNGIP (for handling new drugs/targets)
    * Nascimento (2016): KronRLS+MKL (Multiple Kernel Learning)
  * Enhanced similarity measures and super-target clustering
    * Shi (2015)
  * Collaborative Matrix Factorization with Multiple Similarities (MSCMF)
    * Zheng (2013)
  * Kernelized Bayesian matrix factorization with twin Kernels (KBMF2K)
    * Gonen (2012)
* Learning to Rank (LTR)
    * Yuan (2016)
    * Zhang (2015)
* Deep-learning
    * Restricted Boltzmann machines (RBM)
      * Wang (2013)

## Dealing with skewed/imbalanced dataset
* credible negative samples
  * Liu (2015)

* other approaches:
  * anomaly detection,
  * change detection,
  * ensemble classifier

* Metrics:
  * cohen-kappa score
  * area under precision-recall (aupr)
  * receiver operating characteristic (roc)

* library:
  * https://github.com/scikit-learn-contrib/imbalanced-learn

## Standard datasets for development
* Yamanishi (2008):
  * 4 types: e, gpcr, ic, nr

## Standards in implementing predictor classes
* Each predictor class should implement:
  * predict(xTestList) returns (yPredList of xTestList)
  * close() returns (None)
