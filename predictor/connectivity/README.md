# Compound-protein connectivity prediction

## Aliases and Keywords
* compound-protein/drug-target interaction/link prediction
* in-silico/virtual/computational drug screening/repurposing/repositioning/elucidation/identification

## Challenges
* imbalanced (highly skewed) datasets:
  * ratio of positiveSamples to negativeSamples is too small
  * solutions:
    * bipartite local model (BLM), to lessen the imbalance
      * the training data are drawn locally ``near'' the testing compound-protein pairs
      * each testing compound-protein pair has its own model/classifier, which is computationally expensive
* deceptive negative samples:
  * a negative sample is either _trully_ negative or _simply_ unknown
    (not yet clinically/chemically tested; potentially becomes positive)
  * validated negative samples are not available;
    people never report negative results after clinical/chemical experiments;
    negative results are rarely published (the positive results bias)
  * negative samples that actually positive may fool the learning machine;
    they are negative because their true interactions are simply unknown/not-tested
  * datasets used for analysis contain only true-positive interactions, and
    experimentally validated negative samples are unavailable.
  * solutions:
    * BLM, as above, to help reducing irrelevant training data wrt the testing data
    * unsupervised learning: positive vs unlabeled interactions
* handle 4 scenarios: (new: having no existing/known interaction)
  * known drug, known target
  * new drug, known target
  * known drug, new target
  * new drug, new target (hardest)
* features _and_ similarity (kernel) functions of compounds, proteins and their interactions
  * compound/chemical features/kernels
  * protein/biological/genomic features/kernels
  * compound-protein interaction/network/pharmacological features/kernels
* big data (large-scale dataset)
  * the number of compound-protein links is equal to `nCompound x nProtein`
  * requires large-scale learning

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
    * probabilistic matrix factorization
      * Cobanoglu, M (2013)
    * kernelized bayesian matrix factorization with twin kernels (KBMF2K)
      * Gonen (2012)
  * enhanced similarity measures and super-target clustering (DTI prediction as probabilistic events)
    * Shi, J. Y. (2015)
* Learning to Rank (LTR)
  * Yuan (2016)
  * Zhang (2015)
* Deep-learning
  * Min, W (2017)
  * Wang (2013): Restricted Boltzmann machines (RBM)
* Survey/review
  * Li, J (2016)
  * Jin, G (2014)

## Semi-supervised ML-based approaches
* NormMulInf
  * Peng, L (2016)
* PUCPI
  * Cheng, Z (2016)
* NetCBP
  * Chen, H (2013)
* NetLapRLS
  * Xia, Z (2010)

## Semi-supervised libs
* http://scikit-learn.org/stable/modules/label_propagation.html
* http://pages.cs.wisc.edu/~jerryzhu/ssl/software.html
* https://github.com/sslh/sslh/
* https://github.com/tmadl/semisup-learn
* https://github.com/jkrijthe/RSSL
* https://cran.r-project.org/web/packages/upclass/index.html

## Benchmarking datasets for development
* Yamanishi (2008):
  * 4 types: e, gpcr, ic, nr
  * http://web.kuicr.kyoto-u.ac.jp/supp/yoshi/drugtarget/
  * http://cbio.ensmp.fr/~yyamanishi/pharmaco/
* Ezzat (2016)
  * collected from the DrugBank database (version 4.3,released on 17 Nov. 2015)
  * 12674 drug-target interactions between 5877 drugs and 3348 proteins

## Standards in implementing predictor classes
* Each predictor class should implement:
  * predict(xTestList) returns (yPredList of xTestList)
  * close() returns (None)
