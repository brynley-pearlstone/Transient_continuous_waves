def binary_structure(binary_number):
# Variables to be returned: block_length, block_numbers, n_breaks,n_changepoints
# This function deconstructs the binary number and determined how many
# blocks, how many changepoints, and where each block begins and ends.
	import numpy as np
	
	is_changepoint = np.abs(np.diff(binary_number))
	n_changepoints =  np.sum(is_changepoint)
	bookend_binary = np.append(binary_number, 0)
	bookend_binary = np.insert(bookend_binary,0,0)
	block_end = (np.diff(bookend_binary)<0) 
	n_breaks = sum(block_end) 
	block_start = (np.diff(bookend_binary)>0)

	block_number = np.zeros(len(bookend_binary))
	n_blocks = np.sum(block_start)
	block_length = []
	block = 0
	itt = 0
	for itt in range(len(binary_number)):
		if block_start[itt] == 1:
			count = 0
			while block_end[itt+count] == 0:
				count = count + 1
			
			block_length.append(count)
			block = block + 1
			
		block_number[itt+1] = block_number[itt] +  block_start[itt]
#                if binary_number[itt] ==0:
#                        block_number[itt+1] = 0

	block_numbers = block_number[1:-1]
	for i in range(len(block_numbers)):
		if binary_number[i] ==0:
			block_numbers[i] ='NAN'
		

	if block_length == []:
		block_length = 0
	retvars = {"block_length":block_length, "block_numbers":block_numbers, "n_breaks":n_breaks , "n_changepoints":n_changepoints}
	return retvars
