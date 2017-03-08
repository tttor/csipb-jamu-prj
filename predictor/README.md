# Compound-protein connectivity prediction

## Aliases and Keywords
* compound-protein/drug-target interaction/link prediction
* in-silico/virtual/computational drug screening

## Challenges
* imbalanced data, highly skewed datasets: small number of positive samples (known interactions)
    * current solution: use of local training data to help reduce irrelevant data,
      so each compound-protein has its own model/classifier, this is surely computationally expensive
* deceptive negative samples as they can be either trully negative or simply unknown (not yet clinically/chemically tested)
    * validated negative samples are not available;
      people never report negative results after clinical/chemical experiments
    * the learning machine may be confused as negative samples can actually be positive,
      they are negative because their true interactions are simply unknown/not tested
* handle 4 scenarios: (new: having no existing/known interaction)
    * Known drug, known target
    * New drug, known target
    * Known drug, new target
    * New drug, new target (hardest)
* features _and_ similarity (kernel) functions of compounds, proteins and their interactions
    * compound/chemical features/kernels
    * protein/biological/genomic features/kernels
    * compound-protein interaction/network/pharmacological features/kernels

## ML-based computational approaches
* supervised
    * BLM (Bipartite Local Model)
        * Original
            * Yamanishi (2008)
            * Bleakley (2009)
            * Yamanishi (2010)
        * BLM-NII (bipartite local model with neighbor-based inferring) or Globalized BLM
            * Mei (2012)
            * Mei (2013)
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
        * RBM
* semi-supervised
    * TODO
* skewed/imbalaced dataset
    * Liu (2015):  building up highly credible negative samples
* feature/representation
    * TODO
* similarity-function/kernel
    * see ../similarity/README.md

## Implementing predictor classes
* Each predictor class should implement:
    * predict(xTestList) returns (yPredList of xTestList)
    * close() returns (None)
