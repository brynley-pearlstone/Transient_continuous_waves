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
mpl.use("Agg")
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

parser.add_argument("-d", "--data_list", dest = "data",
                  help = "List of data written as [x, x, x ...].", metavar = "LIST", default = [])
parser.add_argument("-i", "--input_file", dest = "infile",
		  help = "Location of the data file to be used as input, as a string.", metavar = "STRING")
parser.add_argument("-o", "--Output_path", dest = "outpath",
                  help = "Location of the data file to be used to print output.", metavar = "STRING")
parser.add_argument("-b", "--True-binary", dest = "true_binary",
                  help = "Location of the true binary unmber injected into the data.", metavar = "STRING")



args = parser.parse_args()

infile = args.infile
if not os.path.exists(infile):
        os.makedirs(infile)
        print('Please double check input file')

data = args.data
#CP_prior = args.CP_prior
output = args.outpath 

if output[-1] != '/':
        output += '/'
if not os.path.exists(output):
        os.makedirs(output)
        print(output + ' created.')


# Define subrouting to read in evidences from file

data = []
def read_data(infile):
	data = []
	with open(infile, mode='r') as file: 
		content = file.read()
	for line in content.split('\n'):	
		string_line = line.split(',')
		for item in range(len(string_line)):
			string_line[item] = string_line[item].strip()
			string_line[item] = string_line[item].strip('\t')
			string_line[item] = string_line[item].strip('[')
			string_line[item] = string_line[item].strip(']')
		data_line = []
		for item in string_line:
			if item != '':
				data_line.append(float(item))
		if data_line != []:
			data.append(data_line)
	return data


data = read_data(infile)
#for line in data:
	#print(line)
all_data = np.asarray(data)


#create a list of binary numbers of length len(data)
numlist = np.linspace(0, (2**len(all_data[0]))-1, num=2**len(all_data[0]))
bin_list = []

for itt in range(len(numlist)):
	number = bin(int(numlist[int(itt)]))
	x = []
	for item in number[2:]:
		x.append(int(item))
	while len(x)<len(all_data[0]):
		x = [0] + x	
	bin_list.append(x)

bin_array = np.array(bin_list)


# Initialise vars for RBB
l_likelihood =  np.zeros(len(bin_list))
l_evidence = []
config = 0
n_changepoints = []
l_norm = []

#Do RBB
for itt_number in range(len(bin_array)):
	config = itt_number
	# Get n_cp for given bin number
	binary_number = bin_list[itt_number]
	binary_struc =  binary_structure( binary_number )
	n_changepoints.append(binary_struc["n_changepoints"])
	data = all_data[itt_number]
	l_likelihood[config] = sum(data)
	l_norm.append(np.log((1/(len(binary_number)))*(nCr(len(data)-1,n_changepoints[config]))))
	l_evidence.append(l_likelihood[config] + l_norm[config])
#	config += 1

l_odds = l_evidence - l_evidence[0]

sorted_evidence = sorted(l_evidence)
evidence_index = [i[0] for i in sorted(enumerate(l_evidence), key=lambda x:x[1])]
sorted_n_CP = [n_changepoints[i] for i in evidence_index]
#print(l_evidence)

# Define the odds of one config vs all other configs
# Denominator is sum of all that are not that index
odds_all = np.zeros(len(l_evidence));
mask_evidence = np.ma.array((l_evidence), mask=False) #remove exponential applied to evidence - try to avoid NAN
for index in range(len(l_evidence)):
	mask_evidence.mask[index] = True
	running_evidence_sum = -1 * np.inf
	for i in range(len(mask_evidence)):
		if i != index:
			running_evidence_sum =  np.logaddexp(running_evidence_sum, mask_evidence[i])	#odds_all_denom = np.sum(mask_evidence)
	odds_all_denom = running_evidence_sum
	mask_evidence.mask = False
	#print(odds_all_denom)
	#print(mask_evidence[index])
	odds_all[index] = mask_evidence[index]  - odds_all_denom;

sorted_odds_all = sorted(odds_all)
odds_index = [i[0] for i in sorted(enumerate(odds_all), key=lambda x:x[1])]

sorted_odds = sorted(l_odds)
sort_index = [i[0] for i in sorted(enumerate(l_odds), key=lambda x:x[1])]

sorted_binaries = [bin_list[i] for i in odds_index]
sorted_priors = [l_norm[i] for i in odds_index]

sorted_data = [all_data[i] for i in odds_index]


with open(args.true_binary, mode='r') as file:
	content = file.read()
	content_lines = content.split('\n')
	#print(content_lines[1])
	true_bin = content_lines[1].strip('\n')
	
true_binary = []

for entry in true_bin:
	true_binary.append(int(entry))

#print(true_binary)

bins_out = output + 'sorted_binaries.txt'
b = open(bins_out, 'w+')
b.seek(0)
for numb,binary_list in enumerate(sorted_binaries):
	b.write(str(binary_list) + '\n')
	if binary_list[0] == true_binary[0]:
		run_sum = 0
		#print(binary_list)
		for entry in range(len(true_binary)):
			#print(entry)
			#print(true_binary[entry])
			#print(binary_list[entry])
			run_sum = run_sum + (int(true_binary[entry]) - int(binary_list[entry]))
		if run_sum == 0:
			true_binary_position = 2**len(true_binary) - (numb + 1)
			#print(true_binary_position)
	

sanity_check = [odds_index[i] - sort_index[i] for i in range(len(sort_index))]

out = output + 'output.txt'
o = open(out, 'w+')
o.seek(0)
o.write('true_binary_position:\n')
o.write(str(true_binary_position) + '\n\n')
#o.write("Sanity check result: " + str(sum(sanity_check)) + ".\n")


results_dict = []
for i in range(len(sorted_odds_all)):
	results_dict.append({"sorted_binaries":sorted_binaries[i], "sorted_odds_all":sorted_odds_all[i], "sorted_evidence":sorted_evidence[i] , "sorted_priors":sorted_priors[i], "data used":sorted_data[i]})

for i in range(len(results_dict)):
	#print(str(results_dict[i]) + "\n")
	o.write(str(results_dict[i]) + "\n")

# Find the right data instance to plot to show data atoms
# Note: This litterally makes no sense.
i = len(all_data[0])
running_total = 0
while i>0:
	running_total += int(2**(i-1))
	i-=2
print("Running total = " + str(running_total))

o.close()
odds_to_plot = sorted_odds_all[::-1]

sorted_binaries_to_plot = sorted_binaries[::-1]

data_signal_atoms = []
j = 0
for i in range(len(sorted_binaries[1])-1, -1, -1):
	this_data = all_data[2**i]
	print(i)
	print(j)
	data_signal_atoms.append(this_data[j])
	j += 1

if len(sorted_odds_all) > 50:
	plot_functions.barcode_plot(sorted_binaries_to_plot[:49],  odds_to_plot[:49], data_signal_atoms, true_binary_position,  output)
else:
        plot_functions.barcode_plot(sorted_binaries,  sorted_odds_all, data_signal_atoms, true_binary_position, output)

#for i in sorted_binaries:
#print(str(i))

# Output key parameters to file.
# Plot barcode plots.


print("Sanity check result: " + str(sum(sanity_check)) + ".\n")
