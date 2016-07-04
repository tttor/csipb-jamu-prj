### Experiment/Logging Config
seed = 0
testSize = 0.25
datasetName = 'zoo'
nTanimotoIndividualInPercentage = 0
xprmtDir = '/home/tor/robotics/prj/csipb-jamu-prj/xprmt/similarity-func'

datasetDir = '../data'
datasetPath = datasetDir+'/'+datasetName+'/'+datasetName+'.csv'
xprmtTag = datasetName

### DEAP GP Config
nIndividual = 100
nMaxGen = 1 # not including the initial generation
pMut = 0.3
pCx = 0.5

treeMinDepth = 2
treeMaxDepth = 3
subtreeMinDepthMut = 1
subtreeMaxDepthMut = 1

nHOF = nIndividual
# convergenceThreshold = -0.1

### KendallTest Config
nRefPerClassInPercentage = 20
nTopInPercentage = 20
# maxKendallTrial = 10
pValueAcceptance = 0.01
