# import library
import random
import operator
import numpy
import math

from deap import tools, base, creator, gp, algorithms
from operator import itemgetter

# Define primitive set (pSet)
def protectedDiv(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return 1

pset = gp.PrimitiveSet("main", 4)
pset.addPrimitive(max, 2)
pset.addPrimitive(min, 2)
pset.addPrimitive(operator.add, 2)
pset.addPrimitive(operator.mul, 2)
pset.addPrimitive(operator.sub, 2)
pset.addPrimitive(protectedDiv, 2)
pset.addTerminal(0.5)
pset.addEphemeralConstant("randConstant", lambda: random.randint(2,4))

# Renaming the Arguments to desire one
pset.renameArguments(ARG0="a")
pset.renameArguments(ARG1="b")
pset.renameArguments(ARG2="c")
pset.renameArguments(ARG3="d")

# Setting up the tree
expr = gp.genFull(pset, min_=1, max_=3)
tree = gp.PrimitiveTree(expr)

# Settting up the fitness and the individuals
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin, pset=pset)

# register the generation functions into a Toolbox
toolbox = base.Toolbox()
toolbox.register("expr", gp.genFull, pset=pset, min_=1, max_=3)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)


# Define function to calculate similarity
def calcSim(individual) :
    func = toolbox.compile(expr=individual)

    dataset = numpy.matrix(numpy.loadtxt('dataset.csv', delimiter=','))

    referensi = numpy.matrix(numpy.loadtxt('referensi.csv', delimiter=','))

    sm = numpy.array([])

    for i in range (0, dataset.shape[0]):
        for j in range (0, referensi.shape[0]):
            x = dataset[i, 1:]
            xAks = 1 - x
            y = referensi[j, 1:]
            yAks = 1 - y

    # Generate variabel a, b, c, d
            a = numpy.inner(x, y)
            b = numpy.inner(x, yAks)
            c = numpy.inner(xAks, y)
            d = numpy.inner(xAks, yAks)

            print [a, b, c, d]

            result = func(a, b, c, d)
    # Create sm variabel to save information row of dataset and referensi data
    # This variabel is an array which contain [rowDataset, rowReferensi, labelDataset, label, similarityValue]
            if (i == 0) and  (j == 0):
                sm = [i, j, dataset[i, 0], referensi[j, 0], result]
            else :
                zz = numpy.vstack((sm, [i, j, dataset[i, 0], referensi[j, 0], result]))
                sm = zz

    # Ranking the best similarity
    ls = numpy.matrix(sorted(sm, key=itemgetter(4), reverse=True))
    print ls
    print len(ls)

    TP = 0
    avg = []
    # Get 10% from each class calculation then count TP (True Positive) and save the similarity value
    # Count the average by mean
    for i in range(0, len(ls)):
        if ls[i, 2] == ls[i, 3] :
            TP += 1
            avg.append(ls[i,4])
    print TP
    print avg
    print sorted(avg)
    print numpy.median(sorted(avg))
    # # Collect the ranking value from Similarity Coefficient for each class


    return sm

# Define fitness function detail
def evalRecall(individual):
    result = ()
    print (individual)
    print ('\n')
    # # Transform the tree expression in a callable function
    func = toolbox.compile(expr=individual)
    #
    # # Call from dataset
    data = numpy.loadtxt('data.csv', delimiter=',')
    z = numpy.matrix(data)

    x = z[1, :]
    xAks = 1 - x
    y = z[2, :]
    yAks = 1 - y

    a = numpy.inner(x, y)
    b = numpy.inner(x, yAks)
    c = numpy.inner(xAks, y)
    d = numpy.inner(xAks, yAks)

    #P
    # for k in range(0, x.shape[0]):
    #    result += func(x[k, 0], x[k, 1], x[k, 2], x[k, 3])
   # assert False
    # print(func(x[1, 0], x[2, 1], x[3, 2], x[4, 3]))
    result += (func(a, b, c, d),)

    return result

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
    pop = toolbox.population(n=2)

    for individu in pop :
        hasil = calcSim(individu)
        print ('===========================')
        print hasil
        print ('===========================')
        print individu


    # pop = toolbox.population(n=2)
    # # hof = tools.HallOfFame(1)
    # CXPB, MUTPB, NGEN = 0.5, 0.2, 40
    #
    # # stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    # # stats_size = tools.Statistics(len)
    # # mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
    # # mstats.register("avg", numpy.mean)
    # # mstats.register("std", numpy.std)
    # # mstats.register("min", numpy.min)
    # # mstats.register("max", numpy.max)
    # #
    # # # Create a logbook
    # # # logbook = tools.Logbook()
    # # logbook.header = ['gen', 'nevals'] + (mstats.fields)
    #
    # # Evaluate the entire population
    # invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    # fitnesses = map(toolbox.evaluate, pop)
    # for ind, fit in zip(pop, fitnesses):
    #     ind.fitness.values = fit
    #
    # # hof.update(pop)
    # #
    # # record = mstats.compile(pop) if mstats else {}
    # # logbook.record(gen=0, nevals=len(invalid_ind), **record)
    # #
    # # print logbook.stream
    #
    # for g in range(1, NGEN+1):
    #     # Select the next generation individuals
    #     offspring = toolbox.select(pop, len(pop))
    #     # Clone the selected individuals
    #     offspring = map(toolbox.clone, offspring)
    #
    #     # Apply crossover and mutation on the offspring
    #     for child1, child2 in zip(offspring[::2], offspring[1::2]):
    #         if random.random() < CXPB:
    #             toolbox.mate(child1, child2)
    #             del child1.fitness.values
    #             del child2.fitness.values
    #
    #     for mutant in offspring:
    #         if random.random() < MUTPB:
    #             toolbox.mutate(mutant)
    #             del mutant.fitness.values
    #
    #     # Evaluate the individuals with an invalid fitness
    #     invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
    #     fitnesses = map(toolbox.evaluate, invalid_ind)
    #     for ind, fit in zip(invalid_ind, fitnesses):
    #         ind.fitness.values = fit
    #
    #     # hof.update(offspring)
    #
    #     # The population is entirely replaced by the offspring
    #     pop[:] = offspring
    #
    #     # # Append the current generation statistics to the logbook
    #     # record = mstats.compile(pop) if mstats else {}
    #     # logbook.record(gen=g, nevals=len(invalid_ind), **record)
    #     # print logbook.stream
    #
    return pop #, logbook, hof
# def main():
#     pop = toolbox.population(n=2)
#     hof = tools.HallOfFame(1)
#
#     stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
#     stats_size = tools.Statistics(len)
#     mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
#     mstats.register("avg", numpy.mean)
#     mstats.register("std", numpy.std)
#     mstats.register("min", numpy.min)
#     mstats.register("max", numpy.max)
#
# pop, log = algorithms.eaSimple(pop, toolbox, 0.5, 0.1, 40, stats=mstats, halloffame=hof, verbose=True)
#     # print log
#     return pop, log, hof

if __name__ == "__main__":
    main()



### Graphviz Section for plotting purpose ###
# expr = toolbox.individual()
# nodes, edges, labels = gp.graph(expr)
#
# g = pgv.AGraph()
# g.add_nodes_from(nodes)
# g.add_edges_from(edges)
# g.layout(prog="dot")
#
# for i in nodes:
#     n = g.get_node(i)
#     n.attr["label"] = labels[i]
#
# g.draw("tree.pdf")