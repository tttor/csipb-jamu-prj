'''
This construct a c2map following 
Hui Huang, Xiaogang Wu, Ragini Pandey, Jiao Li, Guoling Zhao, Sara Ibrahim, Jake Y. Chen (2012) C2Maps: A network pharmacology database
with comprehensive disease-gene-drug connectivity relationships BMC Genomics. Vol. 13, Supplement 6, S17, 2012
'''
import os
import numpy as np 
import yaml
import glob

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

def load_json(dirpath):
	out_list = []
	for filepath in glob.glob(os.path.join(dirpath, '*.json')):
		print('opening: %s' % filepath)
		
		with open(filepath) as f:  
			i = yaml.load(f)
		out_list.append(i)

	return out_list

def construct(p_list, d_list):
	shape = (len(p_list),len(d_list))
	c2map = np.zeros(shape)

	for i in range(c2map.shape[0]):
		for j in range(c2map.shape[1]):
			score = get_score_pd(p_list[i],d_list[j])
			c2map[i,j] = score

	return c2map

def main():
	# load
	protein_data_dir = '/home/tor/jamu/xprmnt/protein-data'
	p_list = load_json(protein_data_dir)
	print('len(p_list)= %d' % len(p_list))

	drug_data_dir = '/home/tor/jamu/xprmnt/drug-data'
	d_list = load_json(drug_data_dir)
	print('len(d_list)= %d' % len(d_list))

	# construct
	c2map = construct(p_list, d_list)

	# write
	c2map_dir = '/home/tor/jamu/xprmnt/c2map'
	np.savetxt(c2map_dir+'/c2map.csv', c2map, delimiter=",")
	

if __name__ == '__main__':
	main()
