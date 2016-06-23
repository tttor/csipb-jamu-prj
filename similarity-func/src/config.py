# DEAP GP Config
nIndividual = 100
nMaxGen = 10
pMut = 0.1
pCx = 0.5

treeMinDepth = 1
treeMaxDepth = 3
subtreeMinDepthMut = 1
subtreeMaxDepthMut = 1

convergenceThreshold = 0.05

# KendallTest Config
nRefPerClassInPercentage = 10
nTopInPercentage = 10
maxKendallTrial = 100
pValueAcceptance = 0.01

# Training Data Config
# dataPath = {'../data/jamu/jamu-dataset.csv',
#             '../data/stahl-kr/stahl-all.csv',
#             '../data/stahl-pubchem/stahl-all.csv',
#             '../data/stahl-maccs/stahl-all.csv',
#             '../data/zoo/zoo.csv'}
datasetPaths = {'zoo': '../data/zoo/zoo.csv', 
				'zooMinim': '../data/zoo/zooMinim.csv'}

# Logging Config
xprmtDir = '/home/tor/robotics/prj/csipb-jamu-prj/xprmt/similarity-func'
nHOF = 1
