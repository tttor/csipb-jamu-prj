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

## metrics on imbalanced learning:
* cohen-kappa score
* precision-recall curve, area under precision-recall (aupr)
* receiver operating characteristic, area under roc (auroc)
* F_{beta}-measure

## dealing with large-scale samples
* active learning + SVM
* incremental (online) learning machines (with concept drift?)
* ensembled/parallel SVM
  * http://esat.kuleuven.be/stadius/ensemblesvm
  * LIBIRWLS: https://robedm.github.io/LIBIRWLS/
  * http://scikit-learn.org/stable/modules/ensemble.html (`X: [n_samples, n_features]`)
    * VotingClassifier
    * Bagging classifier
    * AdaBoost classifier
* linear classifier (`X: [n_samples, n_features]`)
  * sklearn.linear_model.SGDClassifier
  * sklearn.svm.LinearSVC
  * LIBLINEAR: http://www.csie.ntu.edu.tw/~cjlin/liblinear/

## lib/tool/resources
#### imbalanced learning
* https://github.com/scikit-learn-contrib/imbalanced-learn
  * imblearn.over_sampling.SMOTE
    * mode:  regular, borderline1, borderline2, svm
    * fit_sample(X, y), where X : ndarray, shape (n_samples, n_features)
* scikit-learn SVC with weight setting
  * https://stackoverflow.com/questions/40568254/machine-learning-classification-on-imbalanced-data
* ROSE: Random Over-Sampling Examples
  * https://cran.r-project.org/web/packages/ROSE/index.html
* unbalanced: Racing for Unbalanced Methods Selection
  * https://cran.r-project.org/web/packages/unbalanced/index.html
  
#### active learning
* http://active-learning.net/
* https://github.com/ntucllab/libact
