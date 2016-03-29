from pyevolve import Util
from pyevolve import GTree
from pyevolve import GSimpleGA
from pyevolve import Consts
import math
import numpy as np

# Membaca data perhitungan molekul setiap pasangan dari file csv
data = np.matrix(np.loadtxt('pairwise.csv', delimiter=','))
# reader = csv.DictReader(csvFile)


# Mendefinisikan Node Fungsi
def gp_add(a, b): return a + b


def gp_mul(a, b): return a * b


def gp_sub(a, b): return a - b


def gp_div(a, b): return a / b


def gp_sqrt(a): return math.sqrt(abs(a))


# Fitness function
def eval_func(chromosome):
    # Inisialisasi variabel
    fpr = dict()
    tpr = dict()
    roc_auc = dict()

    # Mengubah ke dalam bytecode
    code_comp = chromosome.getCompiledCode()

    # Inisialisasi nilai node terminal
    a = 1
    b = 2
    c = 2
    d = 4

    # Label kesamaan kelompok (1/0)
    group = 1

    # Mengevaluasi setiap kromosom
    evaluated = eval(code_comp)

    # prediction += (group, evaluated)

    # # Compute ROC curve and ROC area for each class
    # fpr = dict()
    # tpr = dict()
    # roc_auc = dict()
    # for i in range(3):
    #     fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_score[:, i])
    #     roc_auc[i] = auc(fpr[i], tpr[i])
    #
    # nilai_auc = prediction.getAUC()

    return 3


# Menyimpan representasi tree ke dalam .jpg
def step_callback(gp_engine):
    if gp_engine.getCurrentGeneration() == 0:
        GTree.GTreeGP.writePopulationDot(gp_engine, "trees_2.jpg", start=0, end=3)


# Main method untuk menjalankan script program
def main_run():
    genome = GTree.GTreeGP()  # Inisialisasi kromosom
    genome.setParams(max_depth=4, method="ramped")  # Set parameter untuk generate populasi awal
    genome.evaluator.set(eval_func)  # Set fitness function ke dalam evaluator

    ga = GSimpleGA.GSimpleGA(genome)
    ga.setParams(gp_terminals=['a', 'b', 'c', 'd'], gp_function_prefix="gp")  # Set Node Fungsi dan Node Terminal

    ga.setMinimax(Consts.minimaxType["minimize"])
    ga.setGenerations(50)  # Set generasi pemrograman genetik
    ga.setCrossoverRate(1.0)  # Set peluang crossover
    ga.setMutationRate(0.25)  # Set peluang mutasi
    ga.setPopulationSize(800)  # Set populasi
    ga.stepCallback.set(step_callback)

    ga(freq_stats=10)
    best = ga.bestIndividual()  # Menampilkan individu (kromosom) terbaik
    print best


if __name__ == "__main__":
    main_run()
