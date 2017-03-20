# imbalanced/skewed learning

## approaches
* problem-definition-level
  * redefine the problem
    * to focus on a subdomain or partition of the data,
      where the degree of imbalance is lessened.
    * anomaly detection, one-class learning or novelty detection
* data-level
  * active learning
    * to preferentially sample the rare classes
      by focusing the learning on the instances around the classification boundary
    * to reduce, and potentially eliminate, any adverse effects that
      the class imbalance can have on the model's generalization performance.
    * to select informative examples both from the majority and minority classes for labeling,
      subject to the constraints of a given budget.
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

## related works on drug-target prediction
* credible negative samples
  * Liu (2015)
* ensemble learners
  * Ezzat, A (2016)
  * Niu, Y (2015) (RandomForest)
  * Kumari, P (2014) (+SMOTE +ReliefF feature-selection)
  * Li, Q (2009) (granular-SVM repetitive under sampling method (GSVM-RU))
  * Radivojac, P (2004)

## metrics:
  * cohen-kappa score
  * precision-recall curve, area under precision-recall (aupr)
  * receiver operating characteristic, area under roc (auroc)
  * F1-measure, F_{beta}-measure,

## depedencies
  * imbalanced-learn >=0.21
