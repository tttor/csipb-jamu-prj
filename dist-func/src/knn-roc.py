import numpy as np
import configdataset as cfg
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.cross_validation import KFold
from sklearn import svm

try:
    data = np.loadtxt(cfg.JAMU, delimiter='\t')
except:
    data = np.loadtxt(cfg.JAMU, delimiter=',')

def tanimoto(x, y):
    a = np.inner(x, y)
    b = np.inner(x, 1 - y)
    c = np.inner(1 - x, y)

    return 1-(a/(a+b+c))


def GP(x, y):
    a = np.inner(x, y)
    b = np.inner(x, 1 - y)
    c = np.inner(1 - x, y)

    return 1 - (a / (b+c+b+a+b+b+c))

# protectedDiv(a, add(a, add(b, c)))
#
# protectedDiv(a, add(add(a, a), c))
#
# protectedDiv(a, add(add(a, add(b, c)), add(b, a)))
#
# protectedDiv(a, add(add(add(b, add(c, b)), a), add(b, add(b, c))))
#
# protectedDiv(a, add(c, a))

X = data[:, 1:]
y = data[:, 0]

idx = [3, 5, 7, 9, 11]
log = []

kf = KFold(len(y), n_folds=5, shuffle=True)
log.append('KNN, KNN-Tanimoto, KNN-GP')



for i in idx:
    print "N-neighbours : ", i
    log.append('[N-neighbours = ' + str(i) + '],')
    for train, test in kf:
        neigh = KNeighborsClassifier(n_neighbors=i, p=2, metric='minkowski')
        neigh.fit(X[train], y[train])
        y_pred= neigh.predict(X[test])
        y_true = y[test]
        print 'uji knn-default \n', accuracy_score(y_true, y_pred)*100
        log.append('Akurasi KNN : ' + str(accuracy_score(y_true, y_pred) * 100))

        neigh2 = KNeighborsClassifier(n_neighbors=i, metric='pyfunc', func=tanimoto)
        neigh2.fit(X[train], y[train])
        y_pred2 = neigh2.predict(X[test])
        y_true2 = y[test]
        print 'uji knn-tanimoto \n', accuracy_score(y_true2, y_pred2) * 100
        log.append('Akurasi KNN-Tanimoto : ' + str(accuracy_score(y_true2, y_pred2) * 100))

        neigh3 = KNeighborsClassifier(n_neighbors=i, metric='pyfunc', func=GP)
        neigh3.fit(X[train], y[train])
        y_pred3= neigh3.predict(X[test])
        y_true3 = y[test]
        print 'uji knn-gp \n', accuracy_score(y_true3, y_pred3)*100, "\n"
        log.append('Akurasi KNN-GP : ' + str(accuracy_score(y_true3, y_pred3) * 100))

#         # clf = svm.LinearSVC()
#         # clf.fit(X[train], y[train])
#         # y_pred = clf.predict(X[test])
#         # y_true = y[test]
#         # print 'svm : \n', accuracy_score(y_true, y_pred) * 100
#         #
#         # clf = svm.SVC(kernel=tanimoto)
#         # clf.fit(X[train], y[train])
#         # y_pred = clf.predict(X[test])
#         # y_true = y[test]
#         # print 'svm-tan : \n', accuracy_score(y_true, y_pred) * 100
#         #
#         # clf = svm.SVC(kernel=GP)
#         # clf.fit(X[train], y[train])
#         # y_pred = clf.predict(X[test])
#         # y_true = y[test]
#         # print 'svm-gp : \n', accuracy_score(y_true, y_pred) * 100
#
#
        print "============================================================================================================"


# print log
np.savetxt("Jamu/ujiknn-4-jamu.csv", log, fmt='%s', delimiter="\t")