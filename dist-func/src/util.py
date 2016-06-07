import numpy

# Define primitive set (pSet)
def protectedDiv(left, right):
    with numpy.errstate(divide='ignore',invalid='ignore'):
        x = numpy.divide(left, right)
        if isinstance(x, numpy.ndarray):
            x[numpy.isinf(x)] = 1
            x[numpy.isnan(x)] = 1
        elif numpy.isinf(x) or numpy.isnan(x):
            x = 1
    return x

def loadData(datapah):
	'''
	\return A dictionary, whose key is a class index (begins at 0)
			example: data[0] contain a matrix as follows
			Each dict elemet is a matrix where the i-th row indicates the ith-datum,
			and j-th column indicates j-th binary value except
			the last column that indicates the label (class)
	'''
	pass

def loadDataJamu():
	pass

def getFeatureA(s1,s2):
	#TODO
	pass

def getFeatureB(s1,s2):
	#TODO
	pass

def getFeatureC(s1,s2):
	#TODO
	pass

def getFeatureD(s1,s2):
	#TODO
	pass

def converge():
	#TODO
	pass
