# cluster.py
import sys

import sklearn.metrics as met

sys.path.append('../../utility')
import yamanishi_data_util as yam

def main(argv):
	if len(argv)!=2:
		print 'USAGE:'
		print 'python cluster.py [method] [dataset] [dataDir] [outDir]'
		return

	method = argv[1]
	dataset = argv[2]
	dataDir = argv[3]
	outDir = argv[4]

	##
	cls = None
	if method=='kmedoid':
		from kmedoid import kmedoid
		cls = kmedoid
	elif method=='dbscan':
		from sklearn.cluster import DBSCAN
		cls = DBSCAN(eps=0.3, min_samples=10)
	else:
		assert False, 'FATAL: unknown cluster method'

	##
	yamDir=
	_,comList,proList = yam.loadComProConnMat(dataset,dataPath+"/Adjacency")
    kernel = yam.loadKernel(dataset,dataPath)

    nComp = len(comList)
    nProtein = len(proList)

    comSimMat = np.zeros((nComp,nComp), dtype=float)
    proSimMat = np.zeros((nProtein,nProtein), dtype=float)

    for row,i in enumerate(comList):
        for col,j in enumerate(comList):
            comSimMat[row][col] = kernel[(i,j)]

    for row,i in enumerate(proList):
        for col,j in enumerate(proList):
            proSimMat[row][col] = kernel[(i,j)]

    # convert similarity matrix to distance Matrix
    proDisMat = simToDis(proSimMat)
    comDisMat = simToDis(comSimMat)

if __name__ == '__main__':
	main(sys.argv)
