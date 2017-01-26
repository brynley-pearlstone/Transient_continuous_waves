def inner_loop(binary_number,block_length, block_numbers,each_h1):
	        each_h1 = -1*np.inf * np.ones(big_h_vals.shape)
        index = 0
        while index < len(binary_number)-1:
		exponent = 
                if binary_number[index] == 1 & binary_number[index+1] ==1:
                        # Sum the data from the start to the end of the block, 
                        # also marginalise over h define variable end_of_block 
                        # to define where coherent marginalisation ends
                        end_of_block = index + block_length[int(block_numbers[index])-1]-1
                        if end_of_block > len(data):
                                end_of_block = len(data)
			
                        each_h1[:,index:end_of_block] =  -((big_data[:,index:end_of_block] - big_h_vals[:,index:end_of_block])**2)/(2.0*sigma*sigma) + big_prior[:,index:end_of_block] + np.log((1/(np.sqrt(2.0*np.pi)*sigma)))
                        # P_gamma is the sum of these values, log10(sum(prior * gaussian)) 
                        # Calculate P_gamma chunk by chunk for each chunk in the block

                        for row in range(0,end_of_block-index):
                                P_gamma[config, index+row] = logaddexpvect(each_h1[:,index+row])

                        index = end_of_block # Progess the index to end of block  

                elif binary_number[index] == 1 & binary_number[index+1] ==0:
                        each_h1[:,index] = big_prior[:, index] + np.log(1/(np.sqrt(2*np.pi)*sigma)) - (((big_data[:,index] - big_h_vals[:,index])**2)/(2.0*sigma*sigma))
                        P_gamma[config,index] = logaddexpvect(each_h1[:,index])
			print(str(P_gamma[config,index]))

                elif binary_number[index] == 0:
                        P_gamma[config,index] =   np.log(1/(np.sqrt(2*np.pi)*sigma)) + (-((data[index])**2)/(2.0*sigma*sigma))
                index = index + 1
                l_likelihood[config] = np.sum(P_gamma[config,:])
 
