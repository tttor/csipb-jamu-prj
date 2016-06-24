import numpy
from collections import defaultdict

import config as cfg

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
    with numpy.errstate(divide='ignore',invalid='ignore'):
        x = numpy.divide(left, right)
        if isinstance(x, numpy.ndarray):
            x[numpy.isinf(x)] = 1
            x[numpy.isnan(x)] = 1
        elif numpy.isinf(x) or numpy.isnan(x):
            x = 1
    return x

def pow(x):
    return numpy.power(x, 2)

def powhalf(x):
    return numpy.power(x, 0.5)

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
        data = numpy.loadtxt(datapath, delimiter=',')
    except:
        data = numpy.loadtxt(datapath, delimiter="\t")

    for i in range(0, len(data)):
        data_dict[int(data[i, 0])].append(data[i, 1:])

    return data_dict

def loadDataJamu():
    pass

def getFeatureA(s1,s2):
    return numpy.inner(s1, s2)

def getFeatureB(s1,s2):
    return numpy.inner(s1, 1-s2)

def getFeatureC(s1,s2):
    return numpy.inner(1-s1, s2)

def getFeatureD(s1,s2):
    return numpy.inner(1-s1, 1-s2)

def isConverged(pop):
    minFitnessVal = numpy.min([ind.fitness.values[0] for ind in pop])
    
    converged = False
    if minFitnessVal<cfg.convergenceThreshold:
        converged = True

    return converged
