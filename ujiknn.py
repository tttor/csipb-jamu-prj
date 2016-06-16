import numpy
from sklearn.neighbors import KNeighborsClassifier
from sklearn import cross_validation
from sklearn.metrics import accuracy_score


# Define primitive set (pSet)
def protectedDiv(left, right):
    with numpy.errstate(divide='ignore',invalid='ignore'):
        x = numpy.divide(left, right)
        if isinstance(x, numpy.ndarray):
            x[numpy.isinf(x)] = 1
            x[numpy.isnan(x)] = 1
        elif numpy.isinf(x) or numpy.isnan(x):
            x = 1
    return x

idx = [3, 5, 6, 7, 9, 11]
log = []

for i in idx :
    """
    fx = a/2c
    """

    print 'N-neighbours = ', i, '\n'
    log.append('[N-neighbours = '+str(i)+']')

    try:
        data = numpy.loadtxt('/media/banua/Data/Kuliah/Destiny/Tesis/Program/csipb-jamu-prj.20160613.fixed/dist-func/data/zoo/zoo.csv', delimiter='\t')
    except:
        data = numpy.loadtxt('/media/banua/Data/Kuliah/Destiny/Tesis/Program/csipb-jamu-prj.20160613.fixed/dist-func/data/zoo/zoo.csv', delimiter=',')

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

        return 1-(eval(str(protectedDiv(a, c+c))))


    neigh = KNeighborsClassifier(n_neighbors=i, metric='pyfunc', func=mydist)
    neigh.fit(X_train, y_train)

    y_pred = neigh.predict(X_test)
    y_true = y_test

    print 'uji knn-GP \n', accuracy_score(y_true, y_pred)*100
    log.append('Akurasi KNN-GP : '+str(accuracy_score(y_true, y_pred)*100))

numpy.savetxt("/media/banua/Data/Kuliah/Destiny/Tesis/Program/hasil/syahid/ujiknn.csv", log, fmt='%s', delimiter="\t")