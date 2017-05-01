# Clustering compounds and proteins

## Notes
* **no** ground-truth cluster-label is available
* large number of samples: >10K

## Methods
* DBSCAN
  * sklearn v0.17: metric precomputed to accept precomputed sparse matrix
* Spectral clustering
  * sklearn: operate on similarity
  * scalability: medium n_samples
* K-medoid
  * Keum, J (2017): operate on similarity
* agglomerative hierarchical clustering (with linkage= ward)
  * Shi, J. Y. (2015), operate on similarity
* (Mini Batch) K-Means
  * sklearn: operate on distances on feature space

## Performance metrics
* Silhouette Coefficient
  * The best value is 1 and the worst value is -1.
  * Values near 0 indicate overlapping clusters.
  * Negative values generally indicate that
    a sample has been assigned to the wrong cluster, as a different cluster is more similar.
  * only defined if number of labels is 2 <= n_labels <= n_samples - 1.
* Calinski-Harabaz Index
  * the ratio of the between-clusters dispersion mean and the within-cluster dispersion
  * higher when clusters are dense and well separated

## Libs
* pyclustering >= 0.6.6
* scikit-optimize >= 0.3

## Web references
* http://stats.stackexchange.com/questions/21807/evaluation-measure-of-clustering-without-having-truth-labels
* plotting dendogram
  * https://joernhees.de/blog/2015/08/26/scipy-hierarchical-clustering-and-dendrogram-tutorial/
  * http://seaborn.pydata.org/examples/structured_heatmap.html
  * https://github.com/scikit-learn/scikit-learn/blob/70cf4a676caa2d2dad2e3f6e4478d64bcb0506f7/examples/cluster/plot_hierarchical_clustering_dendrogram.py
  * https://github.com/scikit-learn/scikit-learn/pull/3464
