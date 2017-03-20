# imbalanced/skewed learning

## approaches
* problem-definition-level
  * Redefine the Problem
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
    * synthetic minority oversampling technique (smote)
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
    * Hellinger distance decision trees (HDDTs)

## metrics:
  * cohen-kappa score
  * precision-recall curve, area under precision-recall (aupr)
  * receiver operating characteristic, area under roc (auroc)
  * F1-measure, F_{beta}-measure,

## line of works (related to drug-target prediction):
* credible negative samples
  * Liu (2015)

## library:
  * https://github.com/scikit-learn-contrib/imbalanced-learn
