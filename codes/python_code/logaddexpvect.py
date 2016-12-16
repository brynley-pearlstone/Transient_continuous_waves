def logaddexpvect( x )
	# Summary of this function goes here
	# Input 2 log values to be summed. Output double precision
	# output which is the sum of the inputs.
	running_answer = -1*np.inf
	for itteration in range(len(x)):
		running_answer = logplus(running_answer, x[itteration])
	return y = running_answer

