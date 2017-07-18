def logplus( x, y ):
	import numpy as np
	# z = logplus( x, y )
	# This function performs the addition of two logarithmic values of the
	# form log(exp(x) + exp(y)). It avoids problems of dynamic range when the
	# exponentiated values of x or y are very large or small. If x and y are
	# vectors then adjacent values in each will be add
	z = np.inf
	# deal with both values being -infinity
	if np.isinf(x) & np.isinf(y) & (x < 0) & (y < 0):
		z = -np.inf
	else:
		if x > y:
			z = x + np.log1p(np.exp(y - x))
		else:
			z = y + np.log1p(np.exp(x - y))
	return z
