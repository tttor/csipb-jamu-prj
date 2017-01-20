import numpy as np
import json
import matplotlib.pyplot as plt


from sklearn import svm
# from sklearn.cross_validation import KFold
# from sklearn.cross_validation import StratifiedKFold

from sklearn.metrics import precision_recall_curve
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import average_precision_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score

from sklearn.preprocessing import MinMaxScaler

from scipy import interp

#from scoop import futures as fu

######################## The BLM-NII Procedue ########################

def BLM_NII(adjMatrix,sourceSim,targetSim,sourceIndex,targetIndex,mode):
#The Params :
# - DataTraining(Adjecency Matrix, source x target)
# - DataTesting(Source_Index and Target_index)
# - BothSimMatrix
# - alpha=1Later
# - mode (0 if drug->protein, 1 if protein->drug)

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
    for i in range(nTarget):
        if i!=targetIndex:
            gramTest[i-boo] = targetSim[targetIndex][i]
        else:
            boo=1
    boo = 0

    #Make Kernel for Training
    for i in range(nTarget):
        if i!=targetIndex:
            for j in range(nTarget):
                if j!=targetIndex:
                    gramTrain[i-boo][j-foo] = targetSim[i][j]
                else:
                    foo = 1
        else:
            boo = 1
        foo = 0
    boo = 0
    foo = 0


    if (mode == 1):
        #transpose adjacency Matrix
        adjMatrix = [[row[i] for row in adjMatrix] for i in range(len(adjMatrix[0]))]

    #Since the current index is our testing data so we set current element to 0
    originalValue = adjMatrix[sourceIndex][targetIndex]
    adjMatrix[sourceIndex][targetIndex] = 0

    #Compute number interaction from the source
    for row in range(len(adjMatrix[0])):
        rowSum += adjMatrix[sourceIndex][row]

    if (rowSum == 0): #New Data use NII
        #Make an Interaction Profile Vector of Source (eq. 15)
        #--------PreComputeable.... Probably... Later
        for i in range(nSource):
            for j in range(nTarget):
                if (j!=targetIndex):
                    intProfileTemp[j-boo] += sourceSim [sourceIndex][i] * adjMatrix[i][j]
                else:
                    boo = 1

        #Scale I[0,1]
        scale = MinMaxScaler()
        intProfileTemp = intProfileTemp.reshape(-1,1)
        intProfileTemp = scale.fit_transform(intProfileTemp)

        #IntProfile still on Real number space, for SVM training we have to map it to {0,1}
        #### use rounding ####
        intProfileTemp = [int(round(intProfileTemp[i])) for i in range(len(intProfileTemp))]

        #### use threshold ####
        #-------- Using Fix Number --------#
        # threshold = 0.01
        #-------- Using Average --------#
        # sumIntProfile = 0.0
        # avgIntProfile = 0.0
        # for i in range(nTarget-1):
        #     sumIntProfile += intProfileTemp[i]
        # avgIntProfile = sumIntProfile/(nTarget-1)
        # threshold = avgIntProfile
        #-------- ############# --------#

        #-------- Using Median --------#
        # tempArr = np.zeros(nTarget-1,dtype=float)
        # tempArr = np.sort(intProfileTemp,axis=None)
        # mid = 0
        # if nTarget-1 and 1:
        #     mid = round((nTarget-1)/2)
        # else:
        #     mid = (nTarget-1)/2 + (nTarget)/2
        # median = tempArr[int(mid)]
        # threshold = median
        #-------- ##### ######  --------#

        # for i in range(nTarget-1):
        #     if intProfileTemp[i] >= threshold:
        #         intProfileTemp[i] = 1.0
        #     else:
        #         intProfileTemp[i] = 0.0


    else:
        for i in range(nTarget):
            if(i != targetIndex):
                intProfileTemp[i - foo] = adjMatrix[sourceIndex][i]
            else:
                foo = 1

#--------------------Later...--------------------#
#Calculate network Similarity Matrix (eq. 12)
    #for i in range(n):
        #for j in range(n):
            #NetSimMatrix[i][j]=exp(-SquareofByproduct(AdjMatrix[i][]-AdjMatrix[][j])/gamma) (?)

#Calculate total similarity matrix(eq. 14)
    #for i in range(n):
        #for j in range(n):
            #SimMatrixTotal[i][j]=alpha*SourceSim[i][j]+(1-alpha)*NetSimMatrix[i][j]
#--------------------Later...--------------------#


    ##### debugging section

    ######################
    if (len(set(intProfile)))>1:
        #Train SVM
        model = svm.SVC(kernel='precomputed')
        model.fit(gramTrain, intProfile)
#--------------------Later...--------------------#
    #if The sourceSide has 0/1 interaction Predict the edge using SimMatrixDrug/Target and SVM Model --> use sklearn Library
    #else Predict the edge using SimMatrix+SimilarityNetwork(Eq. 12) and Model
#--------------------Later...--------------------#
        #Predict
        prediction = model.predict(gramTest)
    else:
        prediction = 0
    #Return the original value (it somehow didn't revert to original value after returning prediction)
    adjMatrix[sourceIndex][targetIndex] = originalValue

    return prediction
##################################################################

def predictBLMNII(adjMatrix,compSimMat,protSimMat,compIndex,protIndex):
    #Make A prediction from DrugSide
    pComp = BLM_NII(adjMatrix,compSimMat,protSimMat,compIndex,protIndex,0)
    #Make A prediction form TargetSide
    pProt = BLM_NII(adjMatrix,protSimMat,compSimMat,protIndex,compIndex,1)
    #Merge Both prediction
    pred=max(pComp, pProt)

    return pred

if __name__ == '__main__':
######################## path and parse the data set ##########################
    #Pick data set
    # dataset = 'e'
    # dataset = 'gpcr'
    # dataset = 'ic'
    dataset = 'nr'

    #Set Path to Adj Mat
    adjPath='/home/ajmalkurnia/Dataset_skripsi/Adjacency/'+ dataset +'_admat_dgc.txt'
    #Set Path to Similarity Compund
    compSimPath='/home/ajmalkurnia/Dataset_skripsi/SimilarityMatrixCompound/'+ dataset +'_simmat_dc.txt'
    #set Path to Similarity Protein
    protSimPath='/home/ajmalkurnia/Dataset_skripsi/SimilarityMatrixProtein/'+ dataset +'_simmat_dg.txt'
    #set path where to out the files
    outPath='/home/ajmalkurnia/Dataset_skripsi/hasil'

    #index i = drugSide
    #index j = proteinSide

    #Parse Adjfrom files AdjMat to Adjecenncy Matrix
    lines = []
    with open(adjPath) as f:
        lines = f.readlines()

    drugList = [i.strip() for i in lines[0].split()]
    proteinList = []
    del lines[0]

    nDrugs = len(drugList); nProteins = len(lines)
    adjMat = np.zeros( (nDrugs,nProteins) )
    for i,line in enumerate(lines):
        cols = [c.strip() for c in line.split()]
        proteinList.append(cols[0])
        del cols[0]
        for j,c in enumerate(cols):
            adjMat[j][i] = int(c)
#######################################################

#Parse both kernel from similarity files
    with open(compSimPath) as f:
        content = f.readlines()

    compSimMatMeta = []
    compSimMat = None
    for idx,c in enumerate(content):
        if idx==0:
            compSimMatMeta = [i.strip() for i in c.split()]
            n = len(compSimMatMeta)
            compSimMat = np.zeros((n,n),dtype=float)
        else:
            valStr = [i.strip() for i in c.split()]
            assert(valStr[0]==compSimMatMeta[idx-1])
            del valStr[0]
            i = idx - 1
            for j,v in enumerate(valStr):
                compSimMat[i][j] = float(v)

#####################################################
    with open(protSimPath) as f:
        content = f.readlines()

    protSimMatMeta = []
    protSimMat = None
    for idx,c in enumerate(content):
        if idx==0:
            protSimMatMeta = [i.strip() for i in c.split()]
            n = len(protSimMatMeta)
            protSimMat = np.zeros((n,n),dtype=float)
        else:
            valStr = [i.strip() for i in c.split()]
            assert(valStr[0]==protSimMatMeta[idx-1])
            del valStr[0]
            i = idx - 1
            for j,v in enumerate(valStr):
                protSimMat[i][j] = float(v)

######################## main program #############################
    testData = np.zeros(nDrugs*nProteins,dtype=float)
    predictedData = np.zeros(nDrugs*nProteins,dtype=float)
    pComp = 0
    pProt = 0

    for i in range(nDrugs):
        for j in range(nProteins):
            print str(i)+' out of '+str(nDrugs)
            print str(j)+' out of '+str(nProteins)
            predictedData[i*nProteins+j] = predictBLMNII(adjMat,compSimMat,protSimMat,i,j)
#####################################################################

# Preparing Data For Plotting
# Calculation
    key = 'PredictionUsingBLM_NII' #<-- May use other method for comparison
    fpr, tpr, _ = roc_curve(testData, predictedData)
    rocAUC = roc_auc_score(testData, predictedData)
    precision, recall, _ = precision_recall_curve(testData, predictedData)
    prAUC = average_precision_score(testData, predictedData, average='micro')

    #### Debugging
    # print fpr
    # print rocAUC
    # print prAUC
    ####

    lineType = 'k-.'

    perf = {'fpr': fpr, 'tpr': tpr, 'rocAUC': rocAUC,
                 'precision': precision, 'recall': recall, 'prAUC': prAUC,
                 'lineType': lineType}
    perf2 = {'rocAUC': rocAUC,'prAUC': prAUC, 'nTest': nDrugs*nProteins}

    with open(outPath+'/'+ dataset +'_perf.json', 'w') as fp:
        json.dump(perf2, fp, indent=2, sort_keys=True)

    #printAUC
    plt.clf()
    plt.figure()
    #--- ISI DATA PLOT ---#
    plt.plot(perf['fpr'], perf['tpr'], perf['lineType'], label=key+' (area = %0.2f)' % perf['rocAUC'], lw=2)
    #--- ISI DATA PLOT ---#
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic (ROC) Curve')
    plt.legend(loc="lower right")
    plt.savefig(outPath+'/'+ dataset +'_roc_curve.png', bbox_inches='tight')

    #printAUPR
    plt.clf()
    plt.figure()
    #--- ISI DATA PLOT ---#
    plt.plot(perf['recall'], perf['precision'], perf['lineType'], label= key+' (area = %0.2f)' % perf['prAUC'], lw=2)
    #--- ISI DATA PLOT ---#
    plt.ylim([-0.05, 1.05])
    plt.xlim([-0.05, 1.05])
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curve')
    plt.legend(loc="lower left")
    plt.savefig(outPath+'/'+ dataset +'_pr_curve.png', bbox_inches='tight')
