# import library
import time
import random
import operator
import numpy
import config as cfg
from deap import tools, base, creator, gp, algorithms
from collections import OrderedDict
from collections import defaultdict
from sklearn.metrics import roc_auc_score

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

''' Section for setting Tanimoto Individu '''
toolbox.register("exprTan", gp.genTan, pset=pset, min_=1, max_=3)
toolbox.register("indTan", tools.initIterate, creator.Individual, toolbox.exprTan)
toolbox.register("popTan", tools.initRepeat, list, toolbox.indTan)

''' End Section for setting Tanimoto Individu '''

toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

def calcpair(_data):
    mxpair = numpy.array([])
    for i in range(0, _data.shape[0]):
        for j in range(i+1, _data.shape[0]):
            # Generate variabel a, b, c
            a = numpy.inner(_data[i, 1:], _data[j, 1:])
            b = numpy.inner(_data[i, 1:], 1 - _data[j, 1:])
            c = numpy.inner(1 - _data[i, 1:], _data[j, 1:])

            if _data[j, 0] == _data[i, 0]:
                flg = 1
            else:
                flg = 0

            if (i == 0) and (j == 1):
                mxpair = [flg, a, b, c, 0]
            else:
                tmp = numpy.vstack((mxpair, [flg, a, b, c, 0]))
                mxpair = tmp

    return mxpair

auc_list = defaultdict(list)

def calcsim(pop, _x):

    for ind in pop:
        func = toolbox.compile(expr=ind)
        for i in range(0, _x.shape[0]):
            _x[i, 4] = func(_x[i, 1], _x[i, 2], _x[i, 3])

        y_true = _x[:, 0]
        y_scores = _x[:, 4]

        auc = roc_auc_score(y_true, y_scores)
        auc_list[str(ind)].append(auc)


# Define fitness function detail
def evalAuc(individual):
    getAUC = auc_list.get(str(individual))
    result = abs(getAUC[0] - 1)

    return result,

# Setting up the operator of Genetic Programming such as Evaluation, Selection, Crossover, Mutation
toolbox.register("evaluate", evalAuc)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))

# Define main function of program
def main():
    #rmData, refData = getData(cfg.DATASET, 9, 10)
    data = numpy.loadtxt(cfg.DATASET, delimiter=',')
    pair = calcpair(refData)

    cx = [0.1, 0.2, 0.3, 0.4, 0.5];
    mu = [0.04, 0.08, 0.12, 0.16, 0.2];
    for idx in range(1, 6):
        pop = toolbox.popTan(cfg.NPOP)
        calcsim(pop, pair)

        hof = tools.HallOfFame(1)
        CXPB, MUTPB, NGEN = cx[idx-1], mu[idx-1], cfg.NGEN

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
                if random.random() < CXPB:
                    toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values

            for mutant in offspring:
                if random.random() < MUTPB:
                    toolbox.mutate(mutant)
                    del mutant.fitness.values

            for iPop in offspring:
                logpop[g].append(str(iPop))

            # Evaluate the individuals with an invalid fitness
            # invalid_ind = [ind for ind in offspring if not ind.fitness.valid]

            calcsim(offspring, pair)
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
            if (logbook.chapters["fitness"].select("min")[g] <= 0.05):
                break

        logstat["0"].append(logbook.chapters["fitness"].select("avg"))
        logstat["1"].append(logbook.chapters["fitness"].select("max"))
        logstat["2"].append(logbook.chapters["fitness"].select("min"))
        logstat["3"].append(logbook.chapters["fitness"].select("std"))

        logstat = OrderedDict(sorted(logstat.items(), key=lambda t: t[0]))
        logpop = OrderedDict(sorted(logpop.items(), key=lambda t: t[0]))
        loghof = OrderedDict(sorted(loghof.items(), key=lambda t: t[0]))

        numpy.savetxt(str(idx)+"--"+cfg.LOGSTAT, logstat.values(),
                      fmt='%s',delimiter="\t")
        numpy.savetxt(str(idx)+"--"+cfg.LOGPOP, logpop.values(),
                      fmt='%s', delimiter="\t")
        numpy.savetxt(str(idx)+"--"+cfg.LOGHOF, loghof.values(),
                      fmt='%s', delimiter="\t")

    return pop, logbook, hof

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))

