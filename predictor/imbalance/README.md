# imbalanced/skewed learning

## approaches
* problem-definition-level
  * Redefine the Problem
    * to focus on a subdomain or partition of the data,
      where the degree of imbalance is lessened.
    * anomaly detection, one-class learning or novelty detection
* data-level
  * Active Learning and Other Information Acquisition Strategies
    * capable of preferentially sampling the rare classes
      by focusing the learning on the instances around the classification boundary
  * sampling methods
    * random undersampling and random oversampling
    * Synthetic minority oversampling technique (SMOTE)
* algorithm-level
  * ensemble classifiers
    * RareBoost
    * SMOTEBoost
  * cost-sensitive learners
    * AdaCost
  * skew-insensitive learners
    * naive bayes
    * Hellinger distance decision trees (HDDTs)
  * active learning

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
