import numpy as np
from sklearn import svm
from sklearn.metrics import accuracy_score

import util
import config as cfg

def protectedDiv(left, right):
    with np.errstate(divide='ignore',invalid='ignore'):
        x = np.divide(left, right)
        if isinstance(x, np.ndarray):
            x[np.isinf(x)] = 1
            x[np.isnan(x)] = 1
        elif np.isinf(x) or np.isnan(x):
            x = 1
    return x

dataPath = cfg.dataPath[4]
data = np.loadtxt(dataPath, delimiter=',')

x = data[:, 1:]

y = data[:, 0]

gram = np.zeros( (len(x), len(x)) )
clf = svm.SVC(kernel='precomputed')

for i in range(len(x)):
    for j in range(len(x)):
        a = util.getFeatureA(x[i, :], x[j, :])
        b = util.getFeatureB(x[i, :], x[j, :])
        c = util.getFeatureC(x[i, :], x[j, :])

        simValue = eval(str(protectedDiv(a, c+c)))

        gram[i, j] = simValue
        gram[j, i] = simValue

    i+=1

np.savetxt(cfg.xprmtDir + "gram matrix.csv", gram,
              fmt='%s', delimiter=",")

clf.fit(gram, y)

# predict on training examples
y_pred = clf.predict(gram)

print "Skor Akurasi : ", accuracy_score(y, y_pred)*100
