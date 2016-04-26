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
# Dataset 1 - Voting
d1 = numpy.matrix(numpy.loadtxt('/home/banua/csipb-jamu-prj/dist-func/data/voting/dataset_new.csv', delimiter=','))
t1 = numpy.matrix(numpy.loadtxt('/home/banua/csipb-jamu-prj/dist-func/data/voting/referensi_new.csv', delimiter=','))

# Dataset 2 - Jamu
tmp2 = numpy.matrix(numpy.loadtxt('/home/banua/csipb-jamu-prj/dist-func/data/jamu/jamu-dataset.csv', delimiter=','))
d2 = numpy.vstack((tmp2[11:72, :], tmp2[84:321, :], tmp2[333:343, :], tmp2[355:1323, :], tmp2[1335:1721, :],
                   tmp2[1733:2561, :], tmp2[2573:2872, :], tmp2[2884:2979, :], tmp2[2991:3138, :]))
t2 = numpy.vstack((tmp2[1:10, :], tmp2[73:83, :], tmp2[322:332, :], tmp2[344:354, :], tmp2[1324:1334, :],
                   tmp2[1722:1732, :], tmp2[2562:2572, :], tmp2[2873:2883, :], tmp2[2980:2990, :]))

# Dataset 3 - Zoo
d3 = numpy.matrix(numpy.loadtxt('/home/banua/csipb-jamu-prj/dist-func/data/zoo/zoo_dataset.csv', delimiter=','))
t3 = numpy.matrix(numpy.loadtxt('/home/banua/csipb-jamu-prj/dist-func/data/zoo/zoo_referensi.csv', delimiter=','))


#Dataset 4 - Stahl-Maccs
tmp4 = numpy.matrix(numpy.loadtxt('/home/banua/csipb-jamu-prj/dist-func/data/stahl-maccs/stahl-all.csv', delimiter=','))
d4 = numpy.vstack((tmp4[11:28, :], tmp4[140:183, :], tmp4[195:226, :], tmp4[238:243, :], tmp4[255:267, :],
                   tmp4[279:334, :]))
t4 = numpy.vstack((tmp4[1:10, :], tmp4[129:139, :], tmp4[184:194, :], tmp4[227:237, :], tmp4[244:254, :],
                   tmp4[268:278, :]))

# Dataset 5 - Stahl-Pubchem
tmp5 = numpy.matrix(numpy.loadtxt('/home/banua/csipb-jamu-prj/dist-func/data/stahl-pubchem/stahl-all.csv', delimiter=','))
d5 = numpy.vstack((tmp5[11:28, :], tmp5[140:183, :], tmp5[195:226, :], tmp5[238:243, :], tmp5[255:267, :],
                   tmp5[279:334, :]))
t5 = numpy.vstack((tmp5[1:10, :], tmp5[129:139, :], tmp5[184:194, :], tmp5[227:237, :], tmp5[244:254, :],
                   tmp5[268:278, :]))

# Dataset 6 - Stahl-KR
tmp6 = numpy.matrix(numpy.loadtxt('/home/banua/csipb-jamu-prj/dist-func/data/stahl-kr/stahl-all.csv', delimiter='\t'))
d6 = numpy.vstack((tmp6[11:28, :], tmp6[140:183, :], tmp6[195:226, :], tmp6[238:243, :], tmp6[255:267, :],
                   tmp6[279:334, :]))
t6 = numpy.vstack((tmp6[1:10, :], tmp6[129:139, :], tmp6[184:194, :], tmp6[227:237, :], tmp6[244:254, :],
                   tmp6[268:278, :]))

# Apply the calculation
# distFunc = ('a/(a+b+c)', '(((a+b+c+d)*a)-((a+b)*(a+c)))/(((a+b+c+d)*min(a+b, a+c))-((a+b)*(a+c)))')
# rotectedDiv(protectedDiv(add(c, c), protectedDiv(0.5, 0.5)), sub(protectedDiv(d, d), sub(c, d)))
distFunc = ('pDiv(a, a+b+c)',
            'pDiv(((a+b+c+d)*a)-((a+b)*(a+c)), ((a+b+c+d)*min(a+b, a+c))-((a+b)*(a+c)))',
            '(c*0.5)+(a-0.5)',
            '0.5+c',
            '(c*d)-pDiv(d, 3)',
            '(pDiv((a-c), (a-c))) + (b+c+b+c)',
            'c-c',
            '(pDiv(a, b))-(b+b)',
            '(a+b)-(c+c)',
            '((b-c)-(a+c))+((b+b)-pDiv(b, c))')

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
            if i==(ln-1) :
                mn = numpy.mean(d3.get(str(individu)))
                d3[str(individu)].append(mn)

        rank[str(individu)] = d3.get(str(individu))


fName = "Voting"
calcSim(distFunc, d1, t1)

sArray = numpy.asarray(rank.keys())
rArray = numpy.asarray(rank.values())

# Write result to .csv file
numpy.savetxt(fName+"_data_keys.csv", numpy.transpose(sArray), fmt='%s', delimiter=",")
numpy.savetxt(fName+"_data_values.csv", rArray, fmt='%f', delimiter=",")


fName = "Jamu"
kendall.clear()
rank.clear()

calcSim(distFunc, d2, t2)

sArray = numpy.asarray(rank.keys())
rArray = numpy.asarray(rank.values())

# Write result to .csv file
numpy.savetxt(fName+"_data_keys.csv", numpy.transpose(sArray), fmt='%s', delimiter=",")
numpy.savetxt(fName+"_data_values.csv", rArray, fmt='%f', delimiter=",")


fName = "Zoo"
kendall.clear()
rank.clear()

calcSim(distFunc, d3, t3)

sArray = numpy.asarray(rank.keys())
rArray = numpy.asarray(rank.values())

# Write result to .csv file
numpy.savetxt(fName+"_data_keys.csv", numpy.transpose(sArray), fmt='%s', delimiter=",")
numpy.savetxt(fName+"_data_values.csv", rArray, fmt='%f', delimiter=",")


fName = "Stahl-Maccs"
kendall.clear()
rank.clear()

calcSim(distFunc, d4, t4)

sArray = numpy.asarray(rank.keys())
rArray = numpy.asarray(rank.values())

# Write result to .csv file
numpy.savetxt(fName+"_data_keys.csv", numpy.transpose(sArray), fmt='%s', delimiter=",")
numpy.savetxt(fName+"_data_values.csv", rArray, fmt='%f', delimiter=",")


fName = "Stahl-Pubchem"
kendall.clear()
rank.clear()

calcSim(distFunc, d5, t5)

sArray = numpy.asarray(rank.keys())
rArray = numpy.asarray(rank.values())

# Write result to .csv file
numpy.savetxt(fName+"_data_keys.csv", numpy.transpose(sArray), fmt='%s', delimiter=",")
numpy.savetxt(fName+"_data_values.csv", rArray, fmt='%f', delimiter=",")


fName = "Stahl-KR"
kendall.clear()
rank.clear()

calcSim(distFunc, d6, t6)

sArray = numpy.asarray(rank.keys())
rArray = numpy.asarray(rank.values())

# Write result to .csv file
numpy.savetxt(fName+"_data_keys.csv", numpy.transpose(sArray), fmt='%s', delimiter=",")
numpy.savetxt(fName+"_data_values.csv", rArray, fmt='%f', delimiter=",")