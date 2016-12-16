def binary_structure(binary_number):
# Variables to be returned: block_length, block_numbers, n_breaks,n_changepoints
# This function deconstructs the binary number and determined how many
# blocks, how many changepoints, and where each block begins and ends.
	is_changepoint = np.abs(np.diff(binary_number))
	n_changepoints =  np.sum(is_changepoint)
	bookend_binary = cat(2, 0,binary_number, 0)
	block_end = (np.diff(bookend_binary)<0) # Compare where thhe number is not to where it used to be to determine if a block has ended
	n_breaks = sum(block_end) # If there is a break, we add in the normalisation for the marginalisation over h
	block_start = (np.diff(bookend_binary)>0)
	block_number = np.ones(len(binary_number))
	n_blocks = np.sum(block_start)
	block_length = []
	block = 0
	itt = 0
	for itt in range(len(binary_number)-1):
		if block_start[itt] == 1:
			count = 0
			while block_end[itt+count] == 0:
				count = count + 1
			block_length.append(count)
			block = block + 1
		block_number[itt+1] = block_number[itt] +  block_start[itt]
	block_numbers = block_number[1:]
	if block_length == []:
		block_length = 0
	return {"block_length":block_length, "block_numbers":block_numbers, "n_breaks":n_breaks , "n_changepoints":n_changepoints}

