# test.py
from scoop import futures as fu
from sklearn.cross_validation import KFold

def square(x):
	print('x')
	return x**2

def test(f):
	a,b = f
	# print a
	# print b
	return 1

def main():
	# d = range(5)
	# r = fu.map(square,d)

	# print(r)
	# for i in r:
	# 	print(i)

	kf = KFold(10, n_folds=5, shuffle=True) 
	# kfList = [f for f in kf]
	# r2 = fu.map(test,kfList)
	r2 = fu.map(test,kf)
	for i in r2:
		print i


if __name__ == '__main__':
	main()