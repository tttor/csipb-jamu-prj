# Compound-protein connectivity prediction

## Aliases and Keywords
* compound-protein/drug-target interaction/link prediction
* in-silico/virtual/computational drug screening

## Challenges
* imbalanced data, highly skewed datasets:
  * ratio of positiveSamples to negativeSamples is too small
* deceptive negative samples as they can be either trully negative or simply unknown (not yet clinically/chemically tested)
  * validated negative samples are not available;
    people never report negative results after clinical/chemical experiments
  * negative samples that actually positive may fool the learning machine;
    they are negative because their true interactions are simply unknown/not-tested
  * one solution: train locally
    in that the training data are drawn locally ``near'' the testing compound-protein pairs;
    * helps reducing irrelevant training data wrt the testing data
    * but, implies that each testing compound-protein pair has its own model/classifier,
      which is computationally expensive
* handle 4 scenarios: (new: having no existing/known interaction)
  * known drug, known target
  * new drug, known target
  * known drug, new target
  * new drug, new target (hardest)
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
  * SELF-BLM
    * Keum, J (2017)
* Kernel-based
  * kronecker regularized least squares (KronRLS)
    * Laarhoven (2011): KronRLS+GIP (_not_ handle new drugs/targets)
    * Laarhoven (2013): KronRLS+WNNGIP (for handling new drugs/targets)
    * Nascimento (2016): KronRLS+MKL (Multiple Kernel Learning)
  * matrix factorization
    * dual-network integrated logistic matrix factorization (DNILMF)
      * Hao, M (2017)
    * collaborative matrix factorization with multiple similarities (MSCMF)
      * Zheng (2013)
    * kernelized bayesian matrix factorization with twin kernels (KBMF2K)
      * Gonen (2012)
  * enhanced similarity measures and super-target clustering
    * Shi (2015)
* Learning to Rank (LTR)
    * Yuan (2016)
    * Zhang (2015)
* Deep-learning
    * Restricted Boltzmann machines (RBM)
      * Wang (2013)

## Standard datasets for development
* Yamanishi (2008):
  * 4 types: e, gpcr, ic, nr

## Standards in implementing predictor classes
* Each predictor class should implement:
  * predict(xTestList) returns (yPredList of xTestList)
  * close() returns (None)
