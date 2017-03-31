# Clustering on compound and protein sets

## Notes
* **no** ground-truth cluster-label is available
* traning-phase only, no testing phase

## Methods
* K-medoid
  * Keum, J (2017)
* agglomerative hierarchical clustering
  * Shi, J. Y. (2015)

## Performance metrics
* Silhouette Coefficient
* Calinski-Harabaz Index

## Web references
* http://scikit-learn.org/stable/modules/clustering.html
* http://stats.stackexchange.com/questions/21807/evaluation-measure-of-clustering-without-having-truth-labels
* plotting dendogram
  * https://joernhees.de/blog/2015/08/26/scipy-hierarchical-clustering-and-dendrogram-tutorial/
  * http://seaborn.pydata.org/examples/structured_heatmap.html
  * https://github.com/scikit-learn/scikit-learn/blob/70cf4a676caa2d2dad2e3f6e4478d64bcb0506f7/examples/cluster/plot_hierarchical_clustering_dendrogram.py
  * https://github.com/scikit-learn/scikit-learn/pull/3464
