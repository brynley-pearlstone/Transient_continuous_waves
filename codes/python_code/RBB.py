from __future__ import division
import numpy as np
import matplotlib as mpl
from argparse import ArgumentParser
import inspect
import os
import datetime
mpl.rcParams['agg.path.chunksize'] = 10000
import matplotlib.pyplot as plt

parser = ArgumentParser()


parser.add_argument("-N", "--N_chunks", dest = "n_chunks",
                  help = "Number of chunks in the data.", metavar = "NUMBER", default=len(data))
parser.add_argument("-T", "--Signal_type", dest = "signal_type",
                  help = "Signal model for input, , Transient, One segment, Noise or Signal", metavar ="STRING", default = 'Transient')
parser.add_argument("-O", "--Odds_prior", dest = "ref",
                  help = "Prior on odds/ h vals", metavar = "STRING", default = 'Flat')
parser.add_argument("-S", "--Chunk_SNR", dest  = "chunk_SNR",
                  help = "SNR in each cunk of fake data tested for this code.", metavar = "NUMBER", default = 6)
parser.add_argument("-m", "--output_mode", dest = "mode",
                  help = "Output mode of likelihood_only, normal or prior_only.", metavar = "STRING")
parser.add_argument("-P", "--CP_Prior", dest = "CP_prior",
                  help = "Prior on the number of changepoints.", metavar = "NUMBER")
parser.add_argument("-n", "--Noise_seed", dest = "noise_seed",
                  help = "Prior on the number of changepoints.", metavar = "NUMBER")
parser.add_argument("-s", "--seg_seed", dest = "seg_seed",
                  help = "Seed settings for generating segments.", metavar = "NUMBER")



function [  data,sorted_binaries, sorted_odds_all, sorted_n_CP , sorted_evidence, P_gamma, sorted_priors, sanity_check, noise_settings, seg_settings] = RBB_func(n_chunks, signal_type, h_prior, chunk_SNR , mode, CP_prior, noise_seed, seg_seed)



# This script is to find the probability of obtaining any one of the 256
# 8-bit binary unmbers which could constitute a changepoint configuration.
# We define \Gamma as the 8 bit number, and \gamma_i as each bimary element
# of \Gamma.
# We can define the probability of \gamma_i as
# P_gamma = (1/(((2*pi)^-0.5)*sigma))*exp((-(D-gamma_i*h)^2)/(2*sigma^2));
# Now we can define some other things. for example, D is fed forward from
# the CW analysis. Sigmma may be given (look into feed forward from CW
# analysis), h fed forward from CW analysis
# We compute the probability for each of the 256 8-bit numbers

h_sd = 1*10**(-24)
h =  0.8* h_sd
sigma = h /chunk_SNR
hs = np.linspace(0, h_sd, 1001)
[offset, h_loc] = np.amin(np.abs(hs - h))

if h_prior == 'delta':
     l_prior = np.log(zeros(1000, 1))
     l_prior(h_loc) =0

h_vals = np.linspace(h_sd/1001.0,h_sd,num=1000)
log_dh = np.log(h_vals(6) - h_vals(5))

if signal_type == 'Noise':
    [data, true_binary, noise_settings ] = make_all_noise(n_chunks, sigma, h, noise_seed)
    seg_settings = 'NAN';
elif signal_type == 'Signal':
    [data, true_binary, noise_settings] = make_all_signal(n_chunks, sigma, h, noise_seed)
    seg_settings = 'NAN';
elif signal_type == 'Transient':
    [data, true_binary, noise_settings, seg_settings] = make_data(n_chunks, sigma, h, noise_seed, seg_seed)
elif signal_type == 'One segment':
    [data, true_binary, seg_settings, noise_settings] = make_one_segment(n_chunks, sigma, h, seg_seed, noise_seed)

#create a list of binary numbers of length len(data)

numlist = np.linspace(0, (2**len(data))-1, num=2**len(data))
bin_list = []
for itt in range(len(numlist)):
	number = bin(int(numlist[int(itt)]))
	x = []
	for item in number[2:]:
		x.append(int(item))
	while len(x)<len(data):
		x = [0] + x	
	bin_list.append(x)

bin_array = np.array(bin_list)

l_likelihood =  zeros(size(bin_list,1),1)  # We would work in log10-space

big_h_vals = np.matlib.repmat(h_vals, data.shape[0], data.shape[1])
big_prior = np.matlib.repmat(l_prior, data.shape[0], data.shape[1])
big_data = np.matlib.repmat(data, h_vals.shape[0],  h_vals.shape[1])
P_gamma = np.zeros(bin_list.shape)
l_evidence = np.zeros(size(bin_list,1),1)
config = 0

for binary_number in bin_array:
	# binary_number = bin_list[config] # The binary configuration that we are considering now   
!!!	[block_length, block_numbers, n_breaks, n_changepoints(config) ] = binary_structure( binary_number )
	binary_number = binary_number.append(0)
	each_h1 = -1*np.inf * np.ones(big_h_vals.shape)
	index = 1
	while index < len(binary_number):
		if binary_number[index] == 1 && binary_number[index+1] ==1:	
			# Sum the data from the start to the end of the block, also marginalise over h define variable end_of_block to define where coherent marginalisation ends
			end_of_block = index + block_length[block_numbers[index]-1]-1
			if end_of_block > len(data):
				end_of_block = len(data)
	     		each_h1[:,index:end_of_block] =  -((big_data[:,index:end_of_block] - big_h_vals[:,index:end_of_block])**2)/(2.0*sigma*sigma) + big_prior[:,index:end_of_block] + np.log((1/(sqrt(2.0*np.pi)*sigma)))
			# P_gamma is the sum of these values, log10(sum(prior * gaussian)) Calculate P_gamma chunk by chunk for each chunk in the block
			for row in range(0,end_of_block-index):
!!!!				P_gamma[config, index+row] = logaddexpvect(each_h1[:,index+row]) # sum using logaddexpvect for each bit
			index = end_of_block # Progess the index to end of block  
		elif binary_number[index] == 1 && binary_number[index+1] ==0:
			each_h1[:,index] = big_prior[:, index] + np.log(1/(sqrt(2*np.pi)*sigma)) - (((big_data[:,index] - big_h_vals[:,index])**2)/(2.0*sigma*sigma))
		    	P_gamma[config,index] = logaddexpvect(each_h1[:,index])
		elif binary_number[index] == 0:
		    	P_gamma[config,index] =   np.log(1/(sqrt(2*np.pi)*sigma)) + (-((data[index])**2)/(2.0*sigma*sigma))
		index = index + 1
		l_likelihood[config] = np.sum(P_gamma[config,:])
	
	if CP_prior == 'Flat':
		l_norm[config] = np.log((1/(len(binary_number)-1))*(nchoosek(len(data)-1,n_changepoints[config])))
	elif CP_prior == 'exp':
		l_norm[config] = np.log((1/(len(binary_number)-1))*(nchoosek(len(data)-1,n_changepoints[config]))) - n_changepoints
	else:
		l_norm[config] = np.log((1/(len(binary_number)-1))*(nchoosek(len(data)-1,n_changepoints[config])))
     
	if mode == 'prior_only':
		l_evidence[config] = - l_norm[config]
	elif mode == 'normal':
		l_evidence[config] = l_likelihood[config] - l_norm[config]
	elif mode == 'likelihood_only':
		l_evidence[config] = l_likelihood[config]
	config += 1
#     [ l_evidence(config), P_gamma(config) ] = index_loop(binary_number,big_h_vals, big_prior, big_data, P_gamma, l_evidence, data , sigma, n_changepoints(config) , block_length   )

l_odds = l_evidence - l_evidence[1]
sorted_evidence = sorted(np.exp(l_evidence))
evidence_index = [i[0] for i in sorted(enumerate(l_evidence), key=lambda x:x[1])]

sorted_n_CP = n_changepoints(evidence_index)


# Define the odds of one config vs all other configs
# Denominator is sum of all that are not that index
odds_all = np.zeros(len(l_evidence));
evidence = np.ma.array(np.exp(l_evidence), mask=False)

for index in range(len(l_evidence)):
	evidence.mask[index] = True
	odds_all_denom np.sum(evidence)
	evidence.mask = False
	odds_all[index] = evidence[index]/odds_all_denom;

sorted_odds_all = sorted(odds_all)
odds_index = [i[0] for i in sorted(enumerate(odds_all), key=lambda x:x[1])]

sorted_odds = sorted(np.exp(l_odds))
sort_index = [i[0] for i in sorted(enumerate(l_odds), key=lambda x:x[1])]

sorted_binaries = [bin_list[i] for i in odds_index] #bin_list(flipud(sort_index),:);

sorted_priors = [l_norm[i] for i in sort_index]

sanity_check = odds_index - sort_index

#figure
#plot(log10(sorted_odds))
#title('Sorted odds of a configuration vs Gaussian noise')

#figure
#plot(log10(sorted_odds_all))
#title('Sorted odds of a configuration vs all other configurations')

#[  scale, scaled_binaries] = plot_barcode( 25,  flipud(log10(sorted_odds_all)) , sorted_binaries);


