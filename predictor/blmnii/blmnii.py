# blmnii.py
import numpy as np
from sklearn import svm
from sklearn.preprocessing import MinMaxScaler

######################## The BLM-NII Procedue ########################
def BLM_NII(adjMatrix,sourceSim,targetSim,sourceIndex,targetIndex,mode):
    rowSum = 0 #Param for BLM/NII
    nSource = len(sourceSim)
    nTarget = len(targetSim)
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

    for row in range(len(adjMatrix[0])):
        rowSum += adjMatrix[sourceIndex][row]
    if (rowSum == 0):
        for i in range(nSource):
            for j in range(nTarget):
                if (j!=targetIndex):
                    intProfile[j-boo] += sourceSim [sourceIndex][i] * adjMatrix[i][j]
                else:
                    boo = 1
        
        scale = MinMaxScaler((0,1))
        intProfile = intProfile.reshape(-1,1)
        intProfile = scale.fit_transform(intProfile)
        intProfile = [i[0] for i in intProfile.tolist()]

        threshold = 0.5
        for i in range(nTarget-1):
            if intProfile[i] >= threshold:
                intProfile[i] = 1.0
            else:
                intProfile[i] = 0.0
    else:
        for i in range(nTarget):
            if(i != targetIndex):
                intProfile[i - foo] = adjMatrix[sourceIndex][i]
            else:
                foo = 1
    ##### debugging section
    ######################
    if sum(intProfile)>0 and sum(intProfile)<nTarget:
        model = svm.SVC(kernel='precomputed',probability=True)
        model.fit(gramTrain, intProfile)
        prediction = model.predict_proba(gramTest.reshape(1,-1)) # This is Slow

    else:
        prediction = np.random.randint(0,50)/1000.0 # TODO fix me!
    return prediction[0][1]
##################################################################

def predict(adjMatrix,compSimMat,protSimMat,compIndex,protIndex):
    pComp = BLM_NII(adjMatrix,compSimMat,protSimMat,compIndex,protIndex,0)
    pProt = BLM_NII(adjMatrix,protSimMat,compSimMat,protIndex,compIndex,1)
    pred=max(pComp, pProt)
    return pred
