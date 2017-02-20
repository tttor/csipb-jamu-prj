# Compound-protein connectivity prediction

## Aliases and Keywords
* drug-target prediction
* drug-target interactions (DTI) prediction
* compound-protein interaction (CPI) prediction
* drug discovery
* drug-target network
* in-silico drug screening
* virtual drug screening
* computational screening
* compound-protein link prediction

## Challenges
* imbalanced data, highly skewed datasets: small number of positive samples (known interactions)
    * validated negative samples are not available, so negative samples can be either trully negative or unknown
    * current solution: use of local training data to help reduce irrelevant data,
      so each compound-protein has its own model/classifiser, this is surely computationally expensive
* accomodating 4 scenarios: (new: having no existing/known interaction)
    * Known drug, known target
    * New drug, known target
    * Known drug, new target
    * New drug, new target (hardest)
* features of compound-protein interaction (on chemical, genomic and pharmacological spaces)
    * which features are mostly relevant, sufficient, ...
    * feature extraction
* similarity (kernel) functions (on chemical, genomic and pharmacological spaces)

# ML-based computational approaches
* supervised
    * BLM (Bipartite Local Model)
        * Original
            * Yamanishi (2008)
            * Bleakley (2009)
            * Yamanishi (2010)
        * BLM–NII or Globalized BLM or bipartite local model with neighbor-based inferring (BLMN)
           *  Mei (2012)
            * Mei (2013)
    * Kernel
        * Gaussian Interaction Profile Kernel+ Kronecker regularized least squares approach (KronRLS)
            * Laarhoven (2011): GIP
            * Laarhoven (2013): WNN-GIP (for handling new drugs/new targets
            * Nascimento (2016): KronRLS+Multiple Kernel Learning
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
* feature/representation
    * protein/biological/genomic features
    * compound/chemical features
    * network features
* skewed/unbalanced dataset
    * Liu (2015):  building up highly credible negative samples
