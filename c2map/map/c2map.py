'''
This construct a c2map following 
Hui Huang, Xiaogang Wu, Ragini Pandey, Jiao Li, Guoling Zhao, Sara Ibrahim, Jake Y. Chen (2012) C2Maps: A network pharmacology database
with comprehensive disease-gene-drug connectivity relationships BMC Genomics. Vol. 13, Supplement 6, S17, 2012
'''
import os
import numpy as np 
import pylab
import scipy.cluster.hierarchy as sch

def save_mat(c2map, filepath):
	fig = pylab.figure(figsize=(8,8))
	
	# Compute and plot first dendrogram.
	ax1 = fig.add_axes([0.09,0.1,0.2,0.6])
	Y = sch.linkage(c2map, method='centroid')
	Z1 = sch.dendrogram(Y, orientation='right')
	ax1.set_xticks([])
	ax1.set_yticks([])

	# Compute and plot second dendrogram.
	ax2 = fig.add_axes([0.3,0.71,0.6,0.2])
	Y = sch.linkage(c2map, method='single')
	Z2 = sch.dendrogram(Y)
	ax2.set_xticks([])
	ax2.set_yticks([])

	# Plot distance matrix.
	axmatrix = fig.add_axes([0.3,0.1,0.6,0.6])
	idx1 = Z1['leaves']
	idx2 = Z2['leaves']
	c2map = c2map[idx1,:]
	c2map = c2map[:,idx2]
	im = axmatrix.matshow(c2map, aspect='auto', origin='lower', cmap=pylab.cm.YlGnBu)
	axmatrix.set_xticks([])
	axmatrix.set_yticks([])

	# Plot colorbar.
	axcolor = fig.add_axes([0.91,0.1,0.02,0.6])
	pylab.colorbar(im, cax=axcolor)

	fig.savefig(filepath)

'''
p for a protein,
d for a (syntetic) drug, can be equivalent to a compound, e.g natural compounds from Jamu plants
'''
def get_score_pd(p, d):
	df_p = len(p['doc'])
	df_d = len(d['doc'])

	# the total number of documents in which 
	# p and d are co-mentioned
	comentioning_docs = [i for i in p['doc'] if i in d['doc']]
	df_pd = len(comentioning_docs)

	# the size of the entire PubMed abstract collection
	assert p['n_searched_docs']==d['n_searched_docs'], "p['n_searched_docs']!=d['n_searched_docs']"
	N = int(p['n_searched_docs'][0])

	# to avoid out-of-bound errors
	lamda = 1

	# a regularized log-odds function:
	first = np.log(df_pd * N + lamda)
	second = np.log(df_p * df_d + lamda)

	score = first - second

	return score

def construct(proteins, compounds):
	print('constructing c2map ...')
	shape = (len(proteins),len(compounds))
	c2map = np.zeros(shape)

	for i in range(c2map.shape[0]):
		for j in range(c2map.shape[1]):
			score = get_score_pd(proteins[i],compounds[j])
			c2map[i,j] = score

	return c2map

def main():
	pass

if __name__ == '__main__':
	main()
