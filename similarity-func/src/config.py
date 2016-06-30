# DEAP GP Config
nIndividual = 100
nMaxGen = 10 # not including the initial generation
pMut = 0.3
pCx = 0.5

treeMinDepth = 2
treeMaxDepth = 3
subtreeMinDepthMut = 1
subtreeMaxDepthMut = 1

convergenceThreshold = -0.1

# KendallTest Config
nRefPerClassInPercentage = 20
nTopInPercentage = 20
maxKendallTrial = 10
pValueAcceptance = 0.01

# Training Data Config
datasetName = 'zooMinim'

datasetDir = '../data'
datasetPath = datasetDir+'/'+datasetName+'/'+datasetName+'.csv'

# Experiment/Logging Config
seed = 0
xprmtTag = datasetName
xprmtDir = '/home/tor/robotics/prj/csipb-jamu-prj/xprmt/similarity-func'
nHOF = 3
