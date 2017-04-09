# cluster.py
import sys

import sklearn.metrics as met
sys.path.append('../../../utility')
import yamanishi_data_util as yam

def main(argv):
	if len(argv)!=2:
		print 'USAGE:'
		print 'python cluster.py [method] [dataset]'
		return

	method = argv[1]

	clusterer = None
	if method=='kmedoid':
		pass
	elif method=='dbscan':
		pass
	else:
		assert False, 'FATAL: unknown cluster method'

if __name__ == '__main__':
	main(sys.argv)
