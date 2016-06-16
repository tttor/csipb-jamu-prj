# DEAP GP Config
nPop = 10
nGen = 10
pMut = 0.1
pCx = 0.5

treeMinDepth = 1
treeMaxDepth = 3
subtreeMinDepthMut = 1
subtreeMaxDepthMut = 1

convergenceThreshold = 1.1

# Logggin Config
xprmtDir = '/media/banua/Data/Kuliah/Destiny/Tesis/Program/hasil/syahid/'
LOGSTAT = "Tan-GP-" + str(nPop) + "-" + str(nGen) + "-stats.csv"
LOGPOP = "Tan-GP-" + str(nPop) + "-" + str(nGen) + "-pop.csv"
LOGHOF = "Tan-GP-" + str(nPop) + "-" + str(nGen) + "-hof.csv"

# KendallTest Config
nRefPerClassInPercentage = 10
nTopInPercentage = 10
maxKendallTrial = 10
pValueAcceptance = 0.05

# Training Data Config
dataPath = ['../data/jamu/jamu-dataset.csv',
            '../data/stahl-kr/stahl-all.csv',
            '../data/stahl-pubchem/stahl-all.csv',
            '../data/stahl-maccs/stahl-all.csv',
            '../data/zoo/zoo.csv']