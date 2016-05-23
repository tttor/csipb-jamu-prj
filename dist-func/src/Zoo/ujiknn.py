import numpy
import config as cfg
from sklearn.neighbors import KNeighborsClassifier
from sklearn import cross_validation
from sklearn.metrics import accuracy_score


idx = [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29]
log = []

for i in idx :
    """
    Uji KNN Data ZOO

    protectedDiv(a, add(a, add(add(b, c), c)))
    """

    print 'N-neighbours = ', i, '\n'
    log.append('[N-neighbours = '+str(i)+']')

    try:
        data = numpy.loadtxt(cfg.DATASET, delimiter='\t')
    except:
        data = numpy.loadtxt(cfg.DATASET, delimiter=',')

    X_train, X_test, y_train, y_test = cross_validation.train_test_split(
        data[:, 1:], data[:, 0], test_size=0.4, random_state=0)

    neigh = KNeighborsClassifier(n_neighbors=i, p=2, metric='minkowski')
    neigh.fit(X_train, y_train)

    y_pred= neigh.predict(X_test)
    y_true = y_test

    print 'uji knn-default \n', accuracy_score(y_true, y_pred)*100
    log.append('Akurasi KNN : '+str(accuracy_score(y_true, y_pred)*100))


    # KNN-test with Tanimoto function
    def mydist(x, y):
        a = numpy.inner(x, y)
        b = numpy.inner(x, 1 - y)
        c = numpy.inner(1 - x, y)

        return 1-(a/(a+b+c))


    neigh = KNeighborsClassifier(n_neighbors=i, metric='pyfunc', func=mydist)
    neigh.fit(X_train, y_train)

    y_pred = neigh.predict(X_test)
    y_true = y_test

    print 'uji knn-Tanimoto \n', accuracy_score(y_true, y_pred)*100
    log.append('Akurasi KNN-Tanimoto : '+str(accuracy_score(y_true, y_pred)*100))


    # KNN-test with GP function
    def mydist(x, y):
        a = numpy.inner(x, y)
        b = numpy.inner(x, 1 - y)
        c = numpy.inner(1 - x, y)

        return 1-(a/(a+b+c+c))


    neigh = KNeighborsClassifier(n_neighbors=i, metric='pyfunc', func=mydist)
    neigh.fit(X_train, y_train)

    y_pred = neigh.predict(X_test)
    y_true = y_test

    print 'uji knn-GP \n', accuracy_score(y_true, y_pred)*100
    log.append('Akurasi KNN-GP : '+str(accuracy_score(y_true, y_pred)*100))

numpy.savetxt("ujiknn-zoo.csv", log, fmt='%s', delimiter="\t")
