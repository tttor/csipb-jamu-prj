'''
This construct a c2map following 
Hui Huang, Xiaogang Wu, Ragini Pandey, Jiao Li, Guoling Zhao, Sara Ibrahim, Jake Y. Chen (2012) C2Maps: A network pharmacology database
with comprehensive disease-gene-drug connectivity relationships BMC Genomics. Vol. 13, Supplement 6, S17, 2012
'''
import os
import numpy as np 
import pylab
import scipy.cluster.hierarchy as sch
import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt

def save_graph(c2map, filepath):
	graph = c2map['graph']

	X, Y = bipartite.sets(graph)
	pos = dict()
	pos.update( (n, (1, i)) for i, n in enumerate(X) ) # put nodes from X at x=1
	pos.update( (n, (2, i)) for i, n in enumerate(Y) ) # put nodes from Y at x=2
	nx.draw(graph, pos=pos,with_labels=True)
	plt.savefig(filepath)

def save_mat(c2map, filepath):
	mat = c2map['mat']
	fig = pylab.figure(figsize=(8,8))
	
	# Compute and plot first dendrogram.
	ax1 = fig.add_axes([0.09,0.1,0.2,0.6])
	Y = sch.linkage(mat, method='centroid')
	Z1 = sch.dendrogram(Y, orientation='right')
	ax1.set_xticks([])
	ax1.set_yticks([])

	# Compute and plot second dendrogram.
	ax2 = fig.add_axes([0.3,0.71,0.6,0.2])
	Y = sch.linkage(mat, method='single')
	Z2 = sch.dendrogram(Y)
	ax2.set_xticks([])
	ax2.set_yticks([])

	# Plot distance matrix.
	axmatrix = fig.add_axes([0.3,0.1,0.6,0.6])
	idx1 = Z1['leaves']
	idx2 = Z2['leaves']
	mat = mat[idx1,:]
	mat = mat[:,idx2]
	im = axmatrix.matshow(mat, aspect='auto', origin='lower', cmap=pylab.cm.YlGnBu)
	axmatrix.set_xticks([])
	axmatrix.set_yticks([])

	# Plot colorbar.
	axcolor = fig.add_axes([0.91,0.1,0.02,0.6])
	pylab.colorbar(im, cax=axcolor)

	fig.savefig(filepath)

'''
p for a single protein,
d for a single (syntetic) drug, equivalent to a compound, 
  	e.g natural compounds from Jamu plants
'''
def get_score_pd(p, d):
	# df_x: the total number of document in which x is mentioned
	df_p = len(p['doc'])
	df_d = len(d['doc'])

	# the total number of documents in which 
	# p and d are co-mentioned
	comentioning_docs = [i for i in p['doc'] if i in d['doc']]
	df_pd = len(comentioning_docs)

	# N is the size of the entire PubMed abstract collection
	assert p['n_searched_docs']==d['n_searched_docs'], \
		   "p['n_searched_docs']!=d['n_searched_docs']"
	N = int(p['n_searched_docs'][0])

	# a regularized log-odds function:
	lamda = 1 # to avoid out-of-bound errors

	first = np.log(df_pd * N + lamda)
	second = np.log(df_p * df_d + lamda)

	score = first - second

	return score

def construct(proteins, compounds):
	print('constructing c2map ...')

	c2map = dict()
	c2map['proteins'] = proteins
	c2map['compounds'] = compounds
	
	# Construct the matrix
	shape = (len(proteins),len(compounds))
	mat = np.zeros(shape)

	for i in range(mat.shape[0]):
		for j in range(mat.shape[1]):
			score = get_score_pd(proteins[i],compounds[j])
			mat[i,j] = score

	c2map['mat'] = mat
	
	# Construct the graph (bipartite) of proteins vs compounds
	p_ids = [p['id'][0] for p in proteins]
	c_ids = [c['id'][0] for c in compounds]

	graph = nx.Graph()
	graph.add_nodes_from(p_ids, bipartite=0)
	graph.add_nodes_from(c_ids, bipartite=1)
	graph.add_edges_from([(i,j) for i in p_ids for j in c_ids])

	c2map['graph'] = graph

	return c2map

def main():
	pass

if __name__ == '__main__':
	main()
