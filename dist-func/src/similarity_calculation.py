import numpy as np
from collections import OrderedDict
from collections import defaultdict
from deap import tools, base, creator, gp, algorithms
from operator import itemgetter

class pairwise(object):

    def __init__(self):
        return None

    def pairwise_calculation(self, x, y):
        """
        This function to calculate values of a, b, c pairwisely.

        Values a defined as numbers of bits ON (1) in both of object.
        Values b defined as numbers of bits ON (1) in first object and bits OFF (0) in second object.
        Values c defined as numbers of bits OFF (0) in first object and bits ON (1) in second object.

        :param x: An array of first object
        :param y: An array of second object
        :return: pairwise_array = An array containing result of pairwise calculation.
        """
        for i in range(0, y.shape[0]):
            for j in range(0, x.shape[0]):

                # Generate variabel a, b, c
                a = np.inner(y[i, 1:], x[j, 1:])
                b = np.inner(y[i, 1:], 1 - x[j, 1:])
                c = np.inner(1 - y[i, 1:], x[j, 1:])

                # Checking whether first and second object in same class or no.
                # Give 1 in same class, give 0 otherwise.
                flg = 1 if (x[j, 0] == y[i, 0]) else 0

                if (i == 0) and (j == 0):
                    pairwise_array = [flg, a, b, c, 0]
                else:
                    tmp = np.vstack((pairwise_array, [flg, a, b, c, 0]))
                    pairwise_array = tmp

        print "-"

        return pairwise_array


class similarities(object):

    def __init__(self):
        return None

    def calculate_similarities(self, toolbox, pop, remaining_data, reference_data, pairwise_array):
        """
        This function to calculate similarities between object.

        :param toolbox : A tool set for Genetic Programming from DEAP.
        :param pop:  A list of candidate chromosome or individual.
        :param remaining_data: An array of remaining data.
        :param reference_data: An array of reference data.
        :param pairwise_array: An array of pairwise calculation.
        :return: ranking_dict_list : A dictionary list of ranking.
        """

        list_median = dict()
        ranking_array = dict()

        idx = 0

        for individual in pop:
            func = toolbox.compile(expr=individual)

            for i in range(0, pairwise_array.shape[0]):
                pairwise_array[i, 4] = func(pairwise_array[i, 1], pairwise_array[i, 2], pairwise_array[i, 3])

            for i in range(0, reference_data.shape[0]):
                similarities_array = np.array([0, 0])
                true_positive = 0

                similarities_array = pairwise_array[i * remaining_data.shape[0]:(i + 1) * remaining_data.shape[0], :]

                # Descending order data
                similarities_array_desc = np.matrix(sorted(similarities_array, key=itemgetter(4), reverse=True))

                # Count True Positive (TP)
                for k in range(0, int(len(similarities_array_desc) * 0.1)):
                    if similarities_array_desc[k, 0] == 1:
                        true_positive += 1

                if i == 0:
                    array_true_positive = [reference_data[i, 0], true_positive]
                else:
                    tmp = np.vstack((array_true_positive, [reference_data[i, 0], true_positive]))
                    array_true_positive = tmp

            dict_true_positive = defaultdict(list)
            for k, v in array_true_positive:
                dict_true_positive[k].append(v)

            dict_true_positive = dict((k, tuple(v)) for k, v in dict_true_positive.iteritems())

            dict_median = defaultdict(list)
            for ss in range(0, len(dict_true_positive)):
                dict_median[idx].append(np.median(dict_true_positive.get(ss)))

            dict_median = dict((k, tuple(v)) for k, v in dict_median.iteritems())

            list_median[str(individual)] = dict_median.get(idx)
            idx += 1
            print idx

        for individu in pop:
            ln = len(list_median.get(str(individu)))
            ranking_array_ordered = defaultdict(list)

            for i in range(0, ln):
                list_median_ordered = OrderedDict(sorted(list_median.items(), key=lambda t: t[1][i], reverse=True))

                urutan = 0
                for j, key in enumerate(list_median_ordered.keys()):
                    if (key == str(individu)):
                        urutan = j + 1
                        break

                ranking_array_ordered[str(individu)].append(urutan)

            ranking_array[str(individu)] = ranking_array_ordered.get(str(individu))
        return ranking_array

def getData(path, n_class, n_ref):
    """
    This function to split data into remaining data and reference data.

    :param path: A string where you store the dataset.
    :param n_class: number of class.
    :param n_ref: number of data to take in each class.
    :return: remaining_data : An array of Remmaining data after splitting.
             reference_data : An array of reference data were chosen.
    """

    try:
        data = np.loadtxt(path, delimiter=',')
    except:
        data = np.loadtxt(path, delimiter="\t")

    data_per_class = defaultdict(list)
    ref_data = np.array([])
    remaining_data = np.array([])

    for i in range(n_class):
        for j in range(0, len(data)):
            if data[j, 0] == i:
                data_per_class[i].append(data[j, :])

        t = np.random.choice(len(data_per_class.values()[i]), size=(n_ref, 1), replace=False)
        ref_idx = list(t.flat)
        remaining_idx = [l for l in range(len(data_per_class.values()[i])) if l not in t]
        x = np.asarray(data_per_class.values()[i])

        if i == 0:
            ref_data = x[ref_idx, :]
            remaining_data = x[remaining_idx, :]
        else:
            tmp = ref_data
            ref_data = np.vstack((tmp, x[ref_idx, :]))
            tmp = remaining_data
            remaining_data = np.vstack((tmp, x[remaining_idx, :]))

    return remaining_data, ref_data


