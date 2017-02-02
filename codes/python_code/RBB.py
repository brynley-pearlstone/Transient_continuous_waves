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

from __future__ import division
import numpy as np
import matplotlib as mpl
from argparse import ArgumentParser
import inspect
import os
import datetime
mpl.rcParams['agg.path.chunksize'] = 10000
import matplotlib.pyplot as plt
from binary_structure import binary_structure
from logaddexp import logaddexp
from logaddexpvect import logaddexpvect
import math
import matplotlib as mpl
import plot_functions

def nCr(n,r):
    f = math.factorial
    return f(n) / f(r) / f(n-r)
	#There should exist a scipy nCr function

parser = ArgumentParser()

parser.add_argument("-O", "--Odds_prior", dest = "Odds_prior",
                  help = "Prior on odds/ h vals", metavar = "STRING", default = 'Flat')
parser.add_argument("-S", "--Chunk_SNR", dest  = "chunk_SNR",
                  help = "SNR in each cunk of fake data tested for this code.", metavar = "NUMBER", default = 1)
parser.add_argument("-m", "--output_mode", dest = "mode",
                  help = "Output mode of likelihood_only, normal or prior_only.", metavar = "STRING", default = 'normal')
parser.add_argument("-P", "--CP_Prior", dest = "CP_prior",
                  help = "Prior on the number of changepoints.", metavar = "NUMBER")
parser.add_argument("-t", "--true_h", dest = "h",
                  help = "True h value, fo testing with delta prior.", metavar = "NUMBER", default = 0)
parser.add_argument("-d", "--data_list", dest = "data",
                  help = "List of data written as [x, x, x ...].", metavar = "LIST", default = [])
parser.add_argument("-i", "--input_file", dest = "infile",
		  help = "Location of the data file to be used as input, as a string.", metavar = "STRING")
parser.add_argument("-o", "--Output_path", dest = "outpath",
                  help = "Location of the data file to be used to print output.", metavar = "STRING")

args = parser.parse_args()

infile = args.infile
if not os.path.exists(infile):
        os.makedirs(infile)
        print('Please double check input file')

h = float(args.h)
data = args.data
CP_prior = args.CP_prior
mode = str(args.mode)
chunk_SNR = float(args.chunk_SNR)
Odds_prior = args.Odds_prior
output = args.outpath 

if output[-1] != '/':
        output += '/'
if not os.path.exists(output):
        os.makedirs(output)
        print(output + ' created.')


def read_data(infile):
	with open(infile, mode='r') as file: 
		content = file.read()
	both = content.split('\n')
	data_all = both[0]
	data_string = data_all.split(',')
	print(data_string)
	data = []
	for item in data_string[0:]:
		data.append(float(item))
	true_h = float(both[1])
	importvars = [data, true_h]
	return importvars

importvars = read_data(infile)
data = importvars[0]
data = np.asarray(data)
true_h = importvars[1]

h_sd = 1e-24
h =  0.8* h_sd
sigma = h /chunk_SNR
hs = np.linspace(0, h_sd, 1001)

offset = (np.abs(hs - h))
h_loc = np.argmin(offset)
# Delta function prior
#l_prior = -1*np.inf*np.ones(1000)
#l_prior[h_loc] =0
l_prior = 0.001*np.ones(1000)


h_vals = np.linspace(h_sd/1001.0,h_sd,num=1000)
log_dh = np.log(h_vals[6] - h_vals[5])

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

l_likelihood =  np.zeros(len(bin_list))

tile_var = [data.shape[0], 1]
big_h_vals = np.transpose(np.tile(h_vals, tile_var))
big_prior = np.transpose(np.tile(l_prior, tile_var))
big_data = np.tile(data, [1000,1]) #Need the tranpose of this!
P_gamma = np.zeros([len(bin_list), len(bin_list[0])])
l_evidence = []
config = 0
n_changepoints = []
l_norm = []

for binary_number in bin_array:
	binary_struc =  binary_structure( binary_number )
	block_length = binary_struc["block_length"]
	block_numbers = binary_struc["block_numbers"]
	n_breaks = binary_struc["n_breaks"]
	n_changepoints.append(binary_struc["n_changepoints"])
	binary_number = np.append(binary_number, 0)
	each_h1 = -1*np.inf * np.ones(big_h_vals.shape)
	prefactor = np.log(np.sqrt(2.0*np.pi)*sigma)
	index = 0
	used_index = []	

	while index < len(binary_number)-1:
		if binary_number[index] == 1 and binary_number[index+1] ==1:	
			# Sum the data from the start to the end of the block, 
			# also marginalise over h define variable end_of_block 
			# to define where coherent marginalisation ends
			end_of_block = index + block_length[int(block_numbers[index])-1] 
			exponent = -(((big_data[:,index:end_of_block] - big_h_vals[:,index:end_of_block])**2)/(2*sigma*sigma)) # -((D-h)/sqrt(2)*sigma)**2
					
			each_h1[:,index:end_of_block] = exponent + big_prior[:,index:end_of_block] + log_dh - prefactor
			# P_gamma is the sum of these values, log10(sum(prior * gaussian)) 
			# Calculate P_gamma chunk by chunk for each chunk in the block

			for row in range(index,end_of_block):
				P_gamma[config, row] = logaddexpvect(each_h1[:,row]) 
				used_index.append(row)
			index = end_of_block - 1 # Progess the index to end of block  
			
		elif binary_number[index] == 1 and binary_number[index + 1] == 0:
			exponent = -(((big_data[:, index] - big_h_vals[:,index])**2) / (2 * sigma * sigma)) # -((D-h)/(sqrt(2)sigma))**2  
			each_h1[:,index] = exponent + big_prior[:,index]  + log_dh - prefactor
		    	P_gamma[config,index] = logaddexpvect(each_h1[:,index]) # There is a numpy logaddexp function

		elif binary_number[index] == 0:
		    	P_gamma[config,index] = (-((data[index])**2)/(2.0*sigma*sigma)) - prefactor

		index = index + 1
		l_likelihood[config] = np.sum(P_gamma[config,:])

	l_norm.append(np.log((1/(len(binary_number)-1))*(nCr(len(data)-1,n_changepoints[config]))))
	l_evidence.append(l_likelihood[config] + l_norm[config])
	config += 1


l_odds = l_evidence - l_evidence[1]
sorted_evidence = sorted(np.exp(l_evidence))
evidence_index = [i[0] for i in sorted(enumerate(l_evidence), key=lambda x:x[1])]

sorted_n_CP = [n_changepoints[i] for i in evidence_index]

#for i in range(len(P_gamma)):
#	print(str(bin_array[i]))
#	print(str(P_gamma[i]) + "\n")

# Define the odds of one config vs all other configs
# Denominator is sum of all that are not that index
odds_all = np.zeros(len(l_evidence));
evidence = np.ma.array(np.exp(l_evidence), mask=False)

for index in range(len(l_evidence)):
	evidence.mask[index] = True
	odds_all_denom = np.sum(evidence)
	evidence.mask = False
	odds_all[index] = evidence[index]/odds_all_denom;

sorted_odds_all = sorted(odds_all)
odds_index = [i[0] for i in sorted(enumerate(odds_all), key=lambda x:x[1])]

sorted_odds = sorted(np.exp(l_odds))
sort_index = [i[0] for i in sorted(enumerate(l_odds), key=lambda x:x[1])]

sorted_binaries = [bin_list[i] for i in odds_index]
sorted_priors = [l_norm[i] for i in sort_index]
#print("Value of sorted_odds_all is " + str(sorted_odds_all[-1]) + ".\n")
#print("Value of sorted_evidence is " + str(sorted_evidence) + " and has a length of " + str(len(sorted_evidence)) + " .\n")
sanity_check = [odds_index[i] - sort_index[i] for i in range(len(sort_index))]
print("Sanity check result: " + str(sum(sanity_check)) + ".\n")

results_dict = []
for i in range(len(sorted_odds_all)):
	results_dict.append({"sorted_binaries":sorted_binaries[i], "sorted_odds_all":sorted_odds_all[i], "sorted_evidence":sorted_evidence[i] , "sorted_priors":sorted_priors[i]})

for i in range(len(results_dict)):
	print(str(results_dict[i]) + "\n")

plot_functions.plot_like(np.log10(sorted_evidence), output)
plot_functions.plot_odds(np.log10(sorted_odds_all), output)
plot_functions.barcode_plot(sorted_binaries,  sorted_odds, output)
#for i in sorted_binaries:
#	print(str(i))

# Output key parameters to file.
# Plot barcode plots.



