import numpy as np
from sklearn import svm

X = np.array([[0, 0], [1, 1]])
y = [0, 1]

X_te = np.array([[0, 1]])

clf = svm.SVC(kernel='precomputed')

# linear kernel computation
gram = np.dot(X, X.T)
print gram

clf.fit(gram, y) 

# predict on training examples
gram_te = np.dot(X_te, X_te.T)
print gram_te

y_te = clf.predict(gram_te)
print y_te
