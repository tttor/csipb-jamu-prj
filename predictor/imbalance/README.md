# imbalanced/skewed learning

## approaches
* problem-definition-level, redefining the problem
  * to focus on a subdomain or partition of the data,
    where the degree of imbalance is lessened
  * anomaly detection, one-class learning or novelty detection
* data-level
  * active learning
    * SVM-based: select samples near the classifier boundary
      * Ertekin, S (2007)
      * Ho, C (2011)
      * S. Tong (2002)
      * Schohn, G (2000)
  * sampling methods
    * random undersampling and random oversampling
    * synthetic minority oversampling technique (SMOTE)
* algorithm-level
  * ensemble classifiers
    * Bagging-Style Methods
      * SMOTEBagging
      * Over/under Bagging
      * Balanced Random Forests (BRF)
    * Boosting-Based Methods
      * RareBoost
      * SMOTEBoost
    * Hybrid Ensemble Methods
      * EasyEnsemble
      * BalanceCascade
  * cost-sensitive learners
    * AdaCost
  * skew-insensitive learners
    * naive bayes
    * hellinger distance decision trees (HDDTs)

## dealing with imbalance on drug-target prediction
* credible negative samples
  * Liu (2015)
* ensemble learners
  * Ezzat, A (2016): proposed ensemble learners
  * Niu, Y (2015): RandomForest
  * Kumari, P (2014): +SMOTE +ReliefF feature-selection
  * Li, Q (2009): granular-SVM repetitive under sampling method (GSVM-RU)
  * Radivojac, P (2004): ensembles of neural networks
* Weighted Tanimoto Extreme Learning Machine (T-WELM)
  * Czarnecki, W (2015)

## metrics:
* cohen-kappa score
* precision-recall curve, area under precision-recall (aupr)
* receiver operating characteristic, area under roc (auroc)
* F1-measure, F_{beta}-measure,

## web resources
* http://active-learning.net/
* http://contrib.scikit-learn.org/imbalanced-learn/auto_examples/index.html
* https://github.com/scikit-learn-contrib/imbalanced-learn

## dealing with large-scale samples
* Ensemble SVM: http://esat.kuleuven.be/stadius/ensemblesvm
* active learning + SVM
* SGD classifier (works on features, linear case)
* incremental (online) learning machines (with concept drift?)

## misc
* active learning for imbalanced and deceptive samples on drug-target prediction
* benchmarking methods for imbalanced and deceptive samples on drug-target prediction
* Ensembles of SMOTE-SVMs for imbalanced and large-scale drug-target prediction
* SVM-based active learning for imbalanced and large-scale drug-target prediction
