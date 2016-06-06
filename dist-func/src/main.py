# import library
import time
import random
import operator
import numpy

import config as cfg
import similarity_calculation as sc
from collections import OrderedDict
from collections import defaultdict
from deap import tools, base, creator, gp, algorithms
from operator import itemgetter


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


pset = gp.PrimitiveSet("main", 3)
pset.addPrimitive(numpy.add, 2, name="add")
pset.addPrimitive(protectedDiv, 2)

# Renaming the Arguments to desire one
pset.renameArguments(ARG0="a")
pset.renameArguments(ARG1="b")
pset.renameArguments(ARG2="c")

# Settting up the fitness and the individuals
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin, pset=pset)

# register the generation functions into a Toolbox
toolbox = base.Toolbox()
toolbox.register("expr", gp.genFull, pset=pset, min_=1, max_=3)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)

'''
Section for setting Tanimoto Individu
'''
toolbox.register("exprTan", gp.genTan, pset=pset, min_=1, max_=3)
toolbox.register("indTan", tools.initIterate, creator.Individual, toolbox.exprTan)
toolbox.register("popTan", tools.initRepeat, list, toolbox.indTan)

'''
End Section for setting Tanimoto Individu
'''

toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

list_median = dict()
ranking_array = dict()

def pairwise_calculation(x, y):
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
            a = numpy.inner(y[i, 1:], x[j, 1:])
            b = numpy.inner(y[i, 1:], 1 - x[j, 1:])
            c = numpy.inner(1 - y[i, 1:], x[j, 1:])

            flg = 1 if (x[j, 0] == y[i, 0]) else 0

            # Making a pairwise_array
            if (i == 0) and (j == 0):
                pairwise_array = [flg, a, b, c, 0]
            else:
                tmp = numpy.vstack((pairwise_array, [flg, a, b, c, 0]))
                pairwise_array = tmp

    return pairwise_array

# Define function to calculate similarity
def calculate_similarities(pop, remaining_data, reference_data, pairwise_array):
    """
        This function to calculate similarities between object.

        :param toolbox : A tool set for Genetic Programming from DEAP.
        :param pop:  A list of candidate chromosome or individual.
        :param remaining_data: An array of remaining data.
        :param reference_data: An array of reference data.
        :param pairwise_array: An array of pairwise calculation.
        :return: ranking_dict_list : A dictionary list of ranking.
        """
    idx = 0
    for individual in pop:

        func = toolbox.compile(expr=individual)
        array_true_positive = numpy.array([])

        for i in range(0, pairwise_array.shape[0]):
            pairwise_array[i, 4] = func(pairwise_array[i, 1], pairwise_array[i, 2], pairwise_array[i, 3])

        for i in range(0, reference_data.shape[0]):
            similarities_array = numpy.array([0, 0])
            true_positive = 0

            similarities_array = pairwise_array[i*remaining_data.shape[0]:(i+1)*remaining_data.shape[0], :]

            # Descending order data
            similarities_array_desc = numpy.matrix(sorted(similarities_array, key=itemgetter(4), reverse=True))

            # Count True Positive (TP)
            for k in range(0, int(len(similarities_array_desc)*0.1)):
                if similarities_array_desc[k,0] == 1:
                    true_positive += 1

            if i == 0:
                array_true_positive = [reference_data[i, 0], true_positive]
            else :
                temp = numpy.vstack((array_true_positive, [reference_data[i, 0], true_positive]))
                array_true_positive = temp

        dict_true_positive = defaultdict(list)
        for k, v in array_true_positive:
            dict_true_positive[k].append(v)
        dict_true_positive = dict((k, tuple(v)) for k, v in dict_true_positive.iteritems())

        dict_median = defaultdict(list)
        for ss in range(0, len(dict_true_positive)):
            # d2[idx].append(sum(d.get(ss))/len(d.get(ss)))
            dict_median[idx].append(numpy.median(dict_true_positive.get(ss)))
            
        dict_median = dict((k, tuple(v)) for k, v in dict_median.iteritems())

        list_median[str(individual)] = dict_median.get(idx)
        idx += 1

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

def getData(path, n_class, n_ref, flag=None):
    """
        This function to split data into remaining data and reference data.

        :param path: A string where you store the dataset.
        :param n_class: number of class.
        :param n_ref: number of data to take in each class.
        :return: remaining_data : An array of Remmaining data after splitting.
                 reference_data : An array of reference data were chosen.
        """
    if flag == None:
        try:
            data = numpy.loadtxt(path, delimiter=',')
        except:
            data = numpy.loadtxt(path, delimiter="\t")
    elif flag:
        data = path

    data_per_class = defaultdict(list)
    ref_data = numpy.array([])
    remaining_data = numpy.array([])

    for i in range(n_class):
        for j in range(0, len(data)):
            if data[j, 0] == i:
                data_per_class[i].append(data[j, :])

        t = numpy.random.choice(len(data_per_class.values()[i]), size=(n_ref, 1), replace=False)
        ref_idx = list(t.flat)
        remaining_idx = [l for l in range(len(data_per_class.values()[i])) if l not in t]
        x = numpy.asarray(data_per_class.values()[i])

        if i == 0:
            ref_data = x[ref_idx, :]
            remaining_data = x[remaining_idx, :]
        else:
            tmp = ref_data
            ref_data = numpy.vstack((tmp, x[ref_idx, :]))
            tmp = remaining_data
            remaining_data = numpy.vstack((tmp, x[remaining_idx, :]))

    return remaining_data, ref_data


# Define fitness function detail
def evalRecall(individual):
    return numpy.mean(ranking_array.get(str(individual))),

# Setting up the operator of Genetic Programming such as Evaluation, Selection, Crossover, Mutation
toolbox.register("evaluate", evalRecall)
toolbox.register("select", tools.selRoulette)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=1, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))

# Define main function of program
def main():
    x, y = getData(cfg.DATASET, 6, 10)

    # x, y = getData(training_data, 6, 3, True)
    pair = pairwise_calculation(x, y)

    cx = 0.5
    mu = 0.1

    pop = toolbox.population(cfg.NPOP)
    calculate_similarities(pop, x, y, pair)

    hof = tools.HallOfFame(1)
    CXPB, MUTPB, NGEN = cx, mu, cfg.NGEN

    logpop = defaultdict(list)
    loghof = defaultdict(list)
    logstat = defaultdict(list)

    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)
    mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
    mstats.register("avg", numpy.mean)
    mstats.register("std", numpy.std)
    mstats.register("min", numpy.min)
    mstats.register("max", numpy.max)

    # Create a logbook
    logbook = tools.Logbook()
    logbook.header = ['gen', 'nevals'] + mstats.fields

    for iPop in pop:
        logpop[0].append(str(iPop))


    # Evaluate the entire population
    # invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    fitnesses = map(toolbox.evaluate, pop)
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    hof.update(pop)

    for iHof in hof:
        loghof[0].append(str(iHof))

    #
    record = mstats.compile(pop) if mstats else {}
    #
    logbook.record(gen=0, nevals=len(pop), **record)
    #

    print logbook.stream

    for g in range(1, NGEN + 1):
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = map(toolbox.clone, offspring)

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if numpy.random.binomial(1, CXPB):
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:

            if numpy.random.binomial(1, MUTPB):
                toolbox.mutate(mutant)
                del mutant.fitness.values

        for iPop in offspring:
            logpop[g].append(str(iPop))

        # Evaluate the individuals with an invalid fitness
        # invalid_ind = [ind for ind in offspring if not ind.fitness.valid]

        list_median.clear()
        ranking_array.clear()
        calculate_similarities(offspring, x, y, pair)

        fitnesses = map(toolbox.evaluate, offspring)
        #
        for ind, fit in zip(offspring, fitnesses):
            ind.fitness.values = fit

        hof.update(offspring)

        for iHof in hof:
            loghof[g].append(str(iHof))

        # The population is entirely replaced by the offspring
        pop[:] = offspring

        # # Append the current generation statistics to the logbook
        record = mstats.compile(pop) if mstats else {}
        #
        logbook.record(gen=g, nevals=len(offspring), **record)
        print logbook.stream

        if (logbook.chapters["fitness"].select("min")[g] <= 1.5) and (len(ranking_array)>1):
            break

    logstat["0"].append(logbook.chapters["fitness"].select("avg"))
    logstat["1"].append(logbook.chapters["fitness"].select("max"))
    logstat["2"].append(logbook.chapters["fitness"].select("min"))
    logstat["3"].append(logbook.chapters["fitness"].select("std"))

    logstat = OrderedDict(sorted(logstat.items(), key=lambda t: t[0]))
    logpop = OrderedDict(sorted(logpop.items(), key=lambda t: t[0]))
    loghof = OrderedDict(sorted(loghof.items(), key=lambda t: t[0]))

    numpy.savetxt("Logstat-"+cfg.LOGSTAT, numpy.array(logstat.values()),
                    fmt='%s',delimiter=",")
    numpy.savetxt("Fitness -" + cfg.LOGSTAT, logstat.values()[2],
                    fmt='%s', delimiter=",")
    numpy.savetxt("Logpop-"+cfg.LOGPOP, logpop.values(),
                    fmt='%s', delimiter=",")
    numpy.savetxt("Loghof-"+cfg.LOGHOF, loghof.values(),
                    fmt='%s', delimiter=",")


    # UJI KNN
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.metrics import accuracy_score

    def tanimoto(x, y):
        a = numpy.inner(x, y)
        b = numpy.inner(x, 1 - y)
        c = numpy.inner(1 - x, y)

        return 1 - (a / (a + b + c))

    def GP(x, y):
        func = toolbox.compile(expr=hof[len(hof)-1])
        a = numpy.inner(x, y)
        b = numpy.inner(x, 1 - y)
        c = numpy.inner(1 - x, y)

        return 1 - (func(a, b, c))

    X_train = x[:, 1:]
    y_train = x[:, 0]
    X_test = y[:, 1:]
    y_test = y[:, 0]

    n_neigh = [3, 5, 7, 9, 11]
    log = []

    log.append('KNN, KNN-Tanimoto, KNN-GP')

    for i in n_neigh:
        print "N-neighbours : ", i
        log.append('[N-neighbours = ' + str(i) + '],')
        
        neigh = KNeighborsClassifier(n_neighbors=i, p=2, metric='minkowski')
        neigh.fit(X_train, y_train)
        y_pred = neigh.predict(X_test)
        y_true = y_test
        print 'uji knn-default \n', accuracy_score(y_true, y_pred) * 100
        log.append('Akurasi KNN : ' + str(accuracy_score(y_true, y_pred) * 100))

        neigh2 = KNeighborsClassifier(n_neighbors=i, metric='pyfunc', func=tanimoto)
        neigh2.fit(X_train, y_train)
        y_pred2 = neigh2.predict(X_test)
        y_true2 = y_test
        print 'uji knn-tanimoto \n', accuracy_score(y_true2, y_pred2) * 100
        log.append('Akurasi KNN-Tanimoto : ' + str(accuracy_score(y_true2, y_pred2) * 100))

        neigh3 = KNeighborsClassifier(n_neighbors=i, metric='pyfunc', func=GP)
        neigh3.fit(X_train, y_train)
        y_pred3 = neigh3.predict(X_test)
        y_true3 = y_test
        print 'uji knn-gp \n', accuracy_score(y_true3, y_pred3) * 100, "\n"
        log.append('Akurasi KNN-GP : ' + str(accuracy_score(y_true3, y_pred3) * 100))

        print "============================================================================================================"
    numpy.savetxt("ujiknn-maccs.csv", log, fmt='%s', delimiter="\t")
    
    return pop, logbook, hof

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
