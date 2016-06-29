# DEAP GP Config
nIndividual = 100
nMaxGen = 1 # not including the initial generation
pMut = 0.1
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

# Logging Config
xprmtTag = datasetName
xprmtDir = '/home/tor/robotics/prj/csipb-jamu-prj/xprmt/similarity-func'
nHOF = 1
