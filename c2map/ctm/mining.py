import sys
import os
import glob
import json
from lxml import etree

sys.path.append('/home/tor/jamu/ws/csipb-jamu-prj/c2map/util')
import util

def read_article_set(article_set_filepath):
	article_set = {}

	# read the meta of this article set: db, query, ...
	article_set['meta'] = {'db':'pubmed'}

	# read the data
	article_set['data'] = []

	if os.stat(article_set_filepath).st_size == 0:
		return article_set

	tree = etree.parse(article_set_filepath)
	root = tree.getroot()

	for sub in root:
		article_datum = {}
		for sub2 in sub:
			if sub2.tag == 'MedlineCitation':
				for sub3 in sub2:
					if sub3.tag == 'PMID':
						# print sub3.text
						article_datum['pmid'] = sub3.text
					if sub3.tag == 'Article':
						for sub4 in sub3:
							if sub4.tag == 'ArticleTitle':
								# print sub4.text
								article_datum['title'] = sub4.text
							if sub4.tag == 'Abstract':
								for sub5 in sub4:
									# print sub5.text
									article_datum['abstract'] = sub5.text
		article_set['data'].append(article_datum)

	return article_set

def read_article_sets(article_set_filepaths):
	article_sets = []
	for i in article_set_filepaths:
		article_set = read_article_set(i)
		article_sets.append(article_set)

	return article_sets

def main(argv):
	article_set_dir = '/home/tor/jamu/xprmnt/abstact-pubmed/01'
	ori_compound_data_dir = '/home/tor/jamu/xprmnt/compound-data/ori'
	ori_protein_data_dir = '/home/tor/jamu/xprmnt/protein-data/ori'
	compound_data_dir = '/home/tor/jamu/xprmnt/compound-data/searched'
	protein_data_dir = '/home/tor/jamu/xprmnt/protein-data/searched'

	# get articles
	article_filepaths = []
	for filepath in glob.glob(os.path.join(article_set_dir, '*.xml')):
		article_filepaths.append(filepath)
    
	article_sets = read_article_sets(article_filepaths)
	print '#article-sets=', len(article_sets)

	n_articles = sum([len(i['data']) for i in article_sets])
	print '#articles=', n_articles

	# search for compounds
	compounds = util.load_json_from_dir(ori_compound_data_dir)
	print '#compounds=', len(compounds)

	for c in compounds:
		c['n_search_abstracts'] = [n_articles]
	
		for article_set in article_sets:
			for article_datum in article_set['data']:
				abstract = article_datum['abstract'].lower()

				c['pmid_of_containing_abstracts'] = []
				if abstract.find(c['name'][0]) is not -1:
					c['pmid_of_containing_abstracts'].append(article_datum['pmid'])

		compound_filepath = compound_data_dir+'/'+c['id']+'.json';
		with open(compound_filepath,'w') as f:
			json.dump(c, f)  

	# search for proteins
	proteins = util.load_json_from_dir(ori_protein_data_dir)
	print '#proteins=', len(proteins)

	for p in proteins:
		p['n_search_abstracts'] = [n_articles]
	
		for article_set in article_sets:
			for article_datum in article_set['data']:
				abstract = article_datum['abstract'].lower()

				p['pmid_of_containing_abstracts'] = []
				if abstract.find(p['description'][0]) is not -1:
					p['pmid_of_containing_abstracts'].append(article_datum['pmid'])
				if abstract.find(p['symbol'][0]) is not -1:
					p['pmid_of_containing_abstracts'].append(article_datum['pmid'])

		p['pmid_of_containing_abstracts'] = list(set(p['pmid_of_containing_abstracts']))

		protein_filepath = protein_data_dir+'/'+p['id']+'.json';
		with open(protein_filepath,'w') as f:
			json.dump(p, f)  

if __name__ == '__main__':
	main(sys.argv)
