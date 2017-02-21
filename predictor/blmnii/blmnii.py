# blmnii.py
import numpy as np
from sklearn import svm
from sklearn.preprocessing import MinMaxScaler

######################## The BLM-NII Procedue ########################
def BLM_NII(adjMatrix,sourceSim,targetSim,sourceIndex,targetIndex,mode):
    rowSum = 0 #Param for BLM/NII
    nSource = len(sourceSim)
    nTarget = len(targetSim)
    originalValue = 0
    #Flag Variables
    foo = 0
    boo = 0
    #####

    intProfileTemp = np.zeros(nTarget-1,dtype=float)
    intProfile = np.zeros(nTarget-1,dtype=float)
    gramTrain = np.zeros((nTarget-1,nTarget-1))
    gramTest = np.zeros(nTarget-1)

    #Make Kernel For Testing
    gramTest = targetSim[targetIndex]
    gramTest = np.delete(gramTest, targetIndex, 0)

    #Make Kernel for Training
    gramTrain = targetSim
    gramTrain = np.delete(gramTrain,targetIndex, 0)
    gramTrain = np.delete(gramTrain,targetIndex, 1)

    if (mode == 1):
        #transpose adjacency Matrix
        adjMatrix = [[row[i] for row in adjMatrix] for i in range(len(adjMatrix[0]))]

    #Since the current index is our testing data so we set current element to 0
    originalValue = adjMatrix[sourceIndex][targetIndex]
    adjMatrix[sourceIndex][targetIndex] = 0

    #Compute number interaction from the source
    for row in range(len(adjMatrix[0])):
        rowSum += adjMatrix[sourceIndex][row]

    if (rowSum == 0):
        for i in range(nSource):
            for j in range(nTarget):
                if (j!=targetIndex):
                    intProfileTemp[j-boo] += sourceSim [sourceIndex][i] * adjMatrix[i][j]
                else:
                    boo = 1
        scale = MinMaxScaler()
        intProfileTemp = intProfileTemp.reshape(-1,1)
        intProfileTemp = scale.fit_transform(intProfileTemp)

        #### use threshold ####
        #-------- Using Fix Number --------#
        threshold = 0.01
        for i in range(nTarget-1):
            if intProfileTemp[i] >= threshold:
                intProfileTemp[i] = 1.0
            else:
                intProfileTemp[i] = 0.0


    else:
        for i in range(nTarget):
            if(i != targetIndex):
                intProfileTemp[i - foo] = adjMatrix[sourceIndex][i]
            else:
                foo = 1
    ##### debugging section

    ######################
    if (len(set(intProfile)))>1:
        #Train SVM
        model = svm.SVC(kernel='precomputed')
        model.fit(gramTrain, intProfile)
        #Predict
        prediction = model.predict(gramTest)
    else:
        prediction = 0.65*np.random.randint(0,50)/100.0 # TODO fix me!
    return prediction
##################################################################

def predict(adjMatrix,compSimMat,protSimMat,compIndex,protIndex):
    #Make A prediction from DrugSide
    pComp = BLM_NII(adjMatrix,compSimMat,protSimMat,compIndex,protIndex,0)

    #Make A prediction form TargetSide
    pProt = BLM_NII(adjMatrix,protSimMat,compSimMat,protIndex,compIndex,1)

    #Merge Both prediction
    pred=max(pComp, pProt)

    return pred
