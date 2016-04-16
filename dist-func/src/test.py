import random
import operator
import numpy
from collections import OrderedDict, defaultdict


def pDiv(left, right):
    with numpy.errstate(divide='ignore', invalid='ignore'):
        x = numpy.divide(left, right)
        if isinstance(x, numpy.ndarray):
            x[numpy.isinf(x)] = 1
            x[numpy.isnan(x)] = 1
        elif numpy.isinf(x) or numpy.isnan(x):
            x = 1
    return x


# Load dataset
############################
# Dataset 1 : Voting Dataset
d1 = numpy.matrix(numpy.loadtxt('/home/banua/csipb-jamu-prj/dist-func/data/voting/dataset_new.csv', delimiter=','))

# Dataset 2 :  Dataset
d2 = 0

# Dataset 3 :  Dataset
d3 = 0

# Referensi 1 : Voting Dataset
t1 = numpy.matrix(numpy.loadtxt('/home/banua/csipb-jamu-prj/dist-func/data/voting/referensi_new.csv', delimiter=','))

# Referensi 2 :  Dataset
t2 = 0

# Referensi 3 : Dataset
t3 = 0
###############################

# Apply the calculation
# distFunc = ('a/(a+b+c)', '(((a+b+c+d)*a)-((a+b)*(a+c)))/(((a+b+c+d)*min(a+b, a+c))-((a+b)*(a+c)))')
# rotectedDiv(protectedDiv(add(c, c), protectedDiv(0.5, 0.5)), sub(protectedDiv(d, d), sub(c, d)))
distFunc = ('pDiv(a, a+b+c)', 'pDiv(((a+b+c+d)*a)-((a+b)*(a+c)), ((a+b+c+d)*min(a+b, a+c))-((a+b)*(a+c)))',
            'pDiv(pDiv(c+c, pDiv(0.5, 0.5)), (pDiv(d, d))-(c-d))')

kendall = dict()
rank = dict()


# Define function to calculate similarity
def calcSim(pop, x, y):
    idx = 0
    for ind in pop:
        sim = numpy.array([])
        for i in range(0, y.shape[0]):
            sm = numpy.array([0, 0])
            TP = 0
            for j in range(0, x.shape[0]):
                # Generate variabel a, b, c, d
                a = numpy.inner(y[i, 1:], x[j, 1:])
                b = numpy.inner(y[i, 1:], 1 - x[j, 1:])
                c = numpy.inner(1 - y[i, 1:], x[j, 1:])
                d = numpy.inner(1 - y[i, 1:], 1 - x[j, 1:])
                # Check if data and reference in same class
                if x[j, 0] == y[i, 0]:
                    flg = 1
                else:
                    flg = 0
                if (i == 0) and (j == 0):
                    sm = [flg, eval(ind)]
                else:
                    zz = numpy.vstack((sm, [flg, eval(ind)]))
                    sm = zz
            # Descending order data
            ls = numpy.matrix(sorted(sm, key=operator.itemgetter(1), reverse=True))
            cutoff = int(len(ls) * 0.1)
            # Count True Positive (TP)
            for k in range(0, cutoff):
                if ls[k, 0] == 1:
                    TP += 1

            if i == 0:
                sim = [y[i, 0], TP]
            else:
                xx = numpy.vstack((sim, [y[i, 0], TP]))
                sim = xx

        d1 = defaultdict(list)
        for k, v in sim:
            d1[k].append(v)
        d = dict((k, tuple(v)) for k, v in d1.iteritems())

        d2 = defaultdict(list)
        for ss in range(0, len(d)):
            # d2[idx].append(sum(d.get(ss)) / len(d.get(ss)))
            d2[idx].append(numpy.median(d.get(ss)))
        s = dict((k, tuple(v)) for k, v in d2.iteritems())

        kendall[str(ind)] = s.get(idx)
        idx += 1

    for individu in pop:
        ln = len(kendall.get(str(individu)))
        d3 = defaultdict(list)
        for i in range(0, ln):
            newOne = OrderedDict(sorted(kendall.items(), key=lambda t: t[1][i], reverse=True))
            urutan = 0
            for j, key in enumerate(newOne.keys()):
                if (key == str(individu)):
                    urutan = j + 1
                    break
            d3[str(individu)].append(urutan)
        rank[str(individu)] = d3.get(str(individu))

calcSim(distFunc, d1, t1)

# kArray = numpy.asarray(numpy.asarray(rank.keys()))
sArray = numpy.asarray(rank.keys())
rArray = numpy.asarray(rank.values())

# Write result to .csv file
numpy.savetxt("voting_data_keys.csv", numpy.transpose(sArray), fmt='%s', delimiter=",")
numpy.savetxt("voting_data_values.csv", rArray, fmt='%d', delimiter=",")
