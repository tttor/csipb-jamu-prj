# import library
import time
import random
import operator
import numpy
import config as cfg
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
pset.addPrimitive(numpy.subtract, 2, name="sub")
# pset.addPrimitive(numpy.multiply, 2, name="mul")
pset.addPrimitive(protectedDiv, 2)
# pset.addTerminal(0.5)
# pset.addEphemeralConstant("randConstant", lambda: random.randint(2, 4))

# Renaming the Arguments to desire one
pset.renameArguments(ARG0="a")
pset.renameArguments(ARG1="b")
pset.renameArguments(ARG2="c")
# pset.renameArguments(ARG3="d")

# Setting up the tree
expr = gp.genFull(pset, min_=1, max_=3)
tree = gp.PrimitiveTree(expr)

# Settting up the fitness and the individuals
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin, pset=pset)


def funcTanimoto():
    return ('protectedDiv(a, add(a, add(b, c)))')

# register the generation functions into a Toolbox
toolbox = base.Toolbox()
toolbox.register("expr", gp.genFull, pset=pset, min_=1, max_=3)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)

toolbox.register("exprTanimoto", funcTanimoto)
toolbox.register("indTanimoto", tools.initIterate, creator.Individual, toolbox.exprTanimoto)
toolbox.register("popTanimoto", tools.initRepeat, list, toolbox.indTanimoto)

toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

kendall = dict()
rank = dict()

mxpair = numpy.array([])
def calcpair(x, y):
    for i in range(0, y.shape[0]):
        for j in range(0, x.shape[0]):
            # Generate variabel a, b, c, d
            a = numpy.inner(y[i, 1:], x[j, 1:])
            b = numpy.inner(y[i, 1:], 1 - x[j, 1:])
            c = numpy.inner(1 - y[i, 1:], x[j, 1:])
            # d = numpy.inner(1 - y[i,1:], 1 - x[j, 1:])

            if x[j, 0] == y[i, 0]:
                flg = 1
            else:
                flg = 0

            if (i == 0) and (j == 0):
                mxpair = [flg, a, b, c, 0]
            else:
                tmp = numpy.vstack((mxpair, [flg, a, b, c, 0]))
                mxpair = tmp

    return mxpair

# Define function to calculate similarity
def calcSim(pop, m, n, p):
    idx = 0
    for individual in pop:
        func = toolbox.compile(expr=individual)
        sim = numpy.array([])

        for i in range(0, p.shape[0]):
            p[i, 4] = func(p[i, 1], p[i, 2], p[i, 3])

        for i in range(0, n.shape[0]):
            sm = numpy.array([0, 0])
            TP = 0

            sm = p[i*m.shape[0]:(i+1)*m.shape[0], :]

            # Descending order data
            ls = numpy.matrix(sorted(sm, key=itemgetter(1), reverse=True))

            # Count True Positive (TP)
            for k in range(0, len(ls)):
                if ls[k,0] == 1:
                    TP += 1

            if i == 0:
                sim = [n[i, 0], TP]
            else :
                xx = numpy.vstack((sim, [n[i, 0], TP]))
                sim = xx

        d1 = defaultdict(list)
        for k, v in sim:
            d1[k].append(v)
        d = dict((k, tuple(v)) for k, v in d1.iteritems())

        d2 = defaultdict(list)
        for ss in range(0, len(d)):
            # d2[idx].append(sum(d.get(ss))/len(d.get(ss)))
            d2[idx].append(numpy.median(d.get(ss)))
        s = dict((k, tuple(v)) for k, v in d2.iteritems())

        kendall[str(individual)] = s.get(idx)
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


# Define fitness function detail
def evalRecall(individual):
    ln = len(rank.get(str(individual)))
    sm = sum(rank.get(str(individual)))
    result = sm / ln
    return result,

# Setting up the operator of Genetic Programming such as Evaluation, Selection, Crossover, Mutation
toolbox.register("evaluate", evalRecall)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))

# Define main function of program
def main():
    # Dataset
    x = numpy.matrix(
        numpy.loadtxt( cfg.DATASET, delimiter=','))
    # Referensi
    y = numpy.matrix(
        numpy.loadtxt( cfg.REFERENSI, delimiter=','))

    pair = calcpair(x, y)

    pop = toolbox.population(cfg.nPOP)
    calcSim(pop, x, y, pair)

    hof = tools.HallOfFame(1)
    CXPB, MUTPB, NGEN = 0.5, 0.2, cfg.nGEN

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

        kendall.clear()
        rank.clear()
        calcSim(offspring, x, y, pair)

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

    logstat["0"].append(logbook.chapters["fitness"].select("avg"))
    logstat["1"].append(logbook.chapters["fitness"].select("max"))
    logstat["2"].append(logbook.chapters["fitness"].select("min"))
    logstat["3"].append(logbook.chapters["fitness"].select("std"))

    logstat = OrderedDict(sorted(logstat.items(), key=lambda t: t[0]))
    logpop = OrderedDict(sorted(logpop.items(), key=lambda t: t[0]))
    loghof = OrderedDict(sorted(loghof.items(), key=lambda t: t[0]))

    numpy.savetxt(cfg.LOGSTAT, logstat.values(), fmt='%s',delimiter="\t")
    numpy.savetxt(cfg.LOGPOP, logpop.values(), fmt='%s', delimiter="\t")
    numpy.savetxt(cfg.LOGHOF, loghof.values(), fmt='%s', delimiter="\t")

    return pop, logbook, hof

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))