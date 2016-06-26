import numpy as np
from collections import defaultdict

import config as cfg

def inRange(simScore):
    return (simScore>0.0 and simScore<=1.0)

def computeGram(X, funcStr):
    print 'computeGram with ', funcStr
    shape = (len(X),len(X))
    gram = np.zeros(shape)

    for i, x1 in enumerate(X):
        for j,x2 in enumerate(X[i:]):
            a = getFeatureA(x1,x2); b = getFeatureB(x1,x2)
            c = getFeatureC(x1,x2); d = getFeatureD(x1,x2)

            simScore = eval(funcStr); 
            assert simScore>0.0 
            assert simScore<=1.0

            gram[i][j] = gram [j][i] = simScore

    return gram

def expandFuncStr(istr):
    expansionDict = {'add': 'np.add', 'sub': 'np.subtract', 'mul': 'np.multiply',
                     'pDiv': 'protectedDiv', 'min': 'np.minimum', 'max': 'np.maximum' }

    fstr = istr
    for key, d in expansionDict.iteritems():
        fstr = fstr.replace(key,d)

    return fstr

def tanimotoStr():
    return 'pDiv(a, add(a, add(b, c)))'

def forbesStr():
    return 'div(sub(mul(add(add(a, b), add(c, d)), a), mul(add(a, b), add(a, c)),sub(mul(add(add(a, b), add(c, d)), min(add(a, b), add(a, c)),mul(add(a, b), add(a, c)))'

def tanimoto(pset, min_, max_, type_=None):
    def condition(height, depth):
        return depth == height

    if type_ is None:
        type_ = pset.ret

    expr = []
    lsTerm = pset.terminals[type_]
    lsPrim = pset.primitives[type_]

    expr.append(lsPrim[3])
    expr.append(lsTerm[0])
    expr.append(lsPrim[0])
    expr.append(lsTerm[0])
    expr.append(lsPrim[0])
    expr.append(lsTerm[1])
    expr.append(lsTerm[2])

    return expr

def forbes(pset, min_, max_, type_=None):
    def condition(height, depth):
        return depth == height

    if type_ is None:
        type_ = pset.ret

    expr = []
    lsTerm = pset.terminals[type_]
    lsPrim = pset.primitives[type_]

    expr.append(lsPrim[3])
    expr.append(lsPrim[1])
    expr.append(lsPrim[2])
    expr.append(lsPrim[0])
    expr.append(lsPrim[0])
    expr.append(lsTerm[0])
    expr.append(lsTerm[1])
    expr.append(lsPrim[0])
    expr.append(lsTerm[2])
    expr.append(lsTerm[3])
    expr.append(lsTerm[0])
    expr.append(lsPrim[2])
    expr.append(lsPrim[0])
    expr.append(lsTerm[0])
    expr.append(lsTerm[1])
    expr.append(lsPrim[0])
    expr.append(lsTerm[0])
    expr.append(lsTerm[2])

    expr.append(lsPrim[1])
    expr.append(lsPrim[2])
    expr.append(lsPrim[0])
    expr.append(lsPrim[0])
    expr.append(lsTerm[0])
    expr.append(lsTerm[1])
    expr.append(lsPrim[0])
    expr.append(lsTerm[2])
    expr.append(lsTerm[3])
    expr.append(lsPrim[4])
    expr.append(lsPrim[0])
    expr.append(lsTerm[0])
    expr.append(lsTerm[1])
    expr.append(lsPrim[0])
    expr.append(lsTerm[0])
    expr.append(lsTerm[2])
    expr.append(lsPrim[2])
    expr.append(lsPrim[0])
    expr.append(lsTerm[0])
    expr.append(lsTerm[1])
    expr.append(lsPrim[0])
    expr.append(lsTerm[0])
    expr.append(lsTerm[2])

    return expr

# Define primitive set (pSet)
def protectedDiv(left, right):
    with np.errstate(divide='ignore',invalid='ignore'):
        x = np.divide(left, right)
        if isinstance(x, np.ndarray):
            x[np.isinf(x)] = 1
            x[np.isnan(x)] = 1
        elif np.isinf(x) or np.isnan(x):
            x = 1
    return x

def pow(x):
    return np.power(x, 2)

def powhalf(x):
    return np.power(x, 0.5)

def loadData(datapath):
    """
    :param datapath:
    :return: A dictionary, whose key is a class index (begins at 0)
            example: data[0] contain a matrix as follows
            Each dict elemet is a matrix where the i-th row indicates the ith-datum,
            and j-th column indicates j-th binary value except
            the last column that indicates the label (class)
    """

    data_dict = defaultdict(list)
    try:
        data = np.loadtxt(datapath, delimiter=',')
    except:
        data = np.loadtxt(datapath, delimiter="\t")

    for i in range(0, len(data)):
        data_dict[int(data[i, 0])].append(data[i, 1:])

    return data_dict

def loadDataJamu():
    pass

def getFeatureA(s1,s2):
    return np.inner(s1, s2)

def getFeatureB(s1,s2):
    return np.inner(s1, 1-s2)

def getFeatureC(s1,s2):
    return np.inner(1-s1, s2)

def getFeatureD(s1,s2):
    return np.inner(1-s1, 1-s2)

def isConverged(pop):
    minFitnessVal = np.min([ind.fitness.values[0] for ind in pop])
    
    converged = False
    if minFitnessVal<cfg.convergenceThreshold:
        converged = True

    return converged
