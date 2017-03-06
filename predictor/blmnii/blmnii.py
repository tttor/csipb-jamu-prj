# blmnii.py
import numpy as np
from sklearn import svm
from sklearn.preprocessing import MinMaxScaler

########################BLM-NII########################
def BLM_NII(adjMatrix,sourceSim,targetSim,dataSplit,dataQuery):
    testIndex = dataSplit[0]
    trainIndex = dataSplit[1]
    sourceIndex = dataQuery[0]
    targetIndex = dataQuery[1]

    nTrain = len(trainIndex)
    nTest = len(testIndex)
    nSource = len(sourceSim)
    gramTest = targetSim[targetIndex]
    gramTrain = targetSim

    for i in reversed(testIndex):
        gramTest = np.delete(gramTest,i, 0)
        gramTrain = np.delete(gramTrain,i, 0)
        gramTrain = np.delete(gramTrain,i, 1)

    intProfile = np.zeros(nTrain,dtype=float)
    neighbors = [j for i,j in enumerate(adjMatrix[sourceIndex]) if i in trainIndex]

    if len(set(neighbors)) == 1: #New Data use NII
        for i in range(nSource):
            for jj,j in enumerate(trainIndex):
                intProfile[jj] += sourceSim [sourceIndex][i] * adjMatrix[i][j]

        #Scale I[0,1]
        scale = MinMaxScaler((0,1))
        intProfile = intProfile.reshape(-1,1)
        intProfile = scale.fit_transform(intProfile)
        intProfile = [i[0] for i in intProfile.tolist()]
        threshold = 0.5
        intProfile = [int(i>=threshold) for i in intProfile]

    else:
        for ii,i in enumerate(trainIndex):
            intProfile[ii] = adjMatrix[sourceIndex][i]

    if len(set(intProfile))==1:
        prediction = 0
    else:
        model = svm.SVC(kernel='precomputed', probability=True)
        model.fit(gramTrain, intProfile)
        prediction = model.predict_proba(gramTest.reshape(1,-1))

    return (prediction[0][1],sourceIndex,targetIndex)
