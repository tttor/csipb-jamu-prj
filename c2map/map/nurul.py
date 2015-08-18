#!/usr/bin/python
import numpy as np

def main():
	# Set params	
	n_iter = 3

	# Load matrix
	n_rows = 3
	n_cols = 5
	mat =  np.random.uniform(0.0,1.0,(n_rows,n_cols))

	# filepath = 'some_path.csv'
	# mat = np.genfromtxt(filepath, delimiter=',')
	# (n_rows,n_cols) = mat.shape

	# Do the loop
	D = dict.fromkeys(range(n_cols-1))
	for i in range(n_cols-1):
		D[i] = dict.fromkeys(range(i+1, n_cols))
		for j in range(i+1, n_cols):
			print('Iterating columns: (%s, %s) ...' % (str(i),str(j)))
			D[i][j] = np.zeros(n_iter)
			for k in range(n_iter):
				print('Iteration %s-th' % (str(k)))

				# Shuffle the j-th column
				shuffled_col = mat[:,j]
				np.random.shuffle(shuffled_col)

				# Get distance
				d = 0
				for r in range(n_rows):
					d = d + (mat[r,i] - shuffled_col[r])**2
				D[i][j][k] = d

	# Print D-values of iterating cols (0,*)
	print D[0]

	# Print D-values of iterating cols (0,1)
	print D[0][1]

	# Print D-values of iterating cols (0,1) at iteration 2
	print D[0][1][2]

if __name__ == '__main__':
	main()
