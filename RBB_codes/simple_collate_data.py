#Write a code to collate the relevant information for data

from argparse import ArgumentParser
parser = ArgumentParser()

parser.add_argument("-n", "--n_chunks", dest = "n_chunks",
                  help = "Number of chunks used in data", metavar = "INT")
parser.add_argument('-d', '--input_directory', dest = 'input_directory',
                  help = 'Directory containing all of the outputs from lalapps_pulsar_parameter_estimation_nested', metavar = 'STRING')
parser.add_argument('-o', '--output', dest = 'output',
		  help = 'Location to output data file', metavar = 'STRING')

args = parser.parse_args()

n_chunks = int(args.n_chunks)

numbers = range(2**n_chunks)
binary_number = []

for itt,number in enumerate(numbers):
	binary = bin(number)
	#print(binary[2:])
	x = []
	for item in binary[2:]:
		x.append(int(item))
	x.append(0)
	binary_number.append(x)
	
# Pad binary numbers

binary_numbers = []
for binary in binary_number:
	while len(binary) < n_chunks+1: #len(binary_number[-1]):
		binary.insert(0,0) #` = '0' + binary
	binary_numbers.append(binary)
	
# Import the relevant data for each configuratiion of chunks

input_directory = str(args.input_directory)

import os

def assign_data_value(directory, chunk_start, chunk_end, atom_value):
	f = directory + '/chunk_' + str(chunk_start) + '_to_' + str(chunk_end) + '.output.txt'
	item_instance = open(f, 'r')
	lines = []
	for line in item_instance:
		lines.append(line)
	if atom_value == 1:
		atom_line = lines[0].split('=')
		chunks_value = atom_line[1]
	elif atom_value ==0:
                atom_line = lines[3].split('=')
                chunks_value = atom_line[1]
	else:
		print("I'm sorry Dave, I can't do that for you")
		quit(0)
	return chunks_value

def get_bayes_factor(directory, block_start, block_end, atom_value):
        f = directory + '/chunk_' + str(chunk_start) + '_to_' + str(chunk_end) + '.output.txt'
        item_instance = open(f, 'r')
        lines = []
        for line in item_instance:
                lines.append(line)
        if atom_value == 1:
                atom_line = lines[1].split('=')
                chunks_value = float(atom_line[1])
        elif atom_value ==0:
		#Return the negative value of the log bayes factor, ie the Noise-Vs-Signal ratio
		#This means the data parts can still be summed as usual, just have to be careful to check it works.
                atom_line = lines[1].split('=')
                chunks_value = -1 * float(atom_line[1])
        else:
                print("I'm sorry Dave, I can't do that for you")
                quit(0)
        return chunks_value

def get_posterior(directory, block_start, block_end):
        p = directory + '/posteriors/chunk_' + str(block_start) + '-' + str(block_end) + '_pos.txt'
        pos_file = open(p, 'r')
        pos_lines = []
        for line in pos_file:
        	pos_lines = line
	h_value = pos_lines
        return h_value

#For each binary number, import the correct data
from binary_structure import binary_structure
data_bins = []
bayes_bins = []
h_bins = []
for bin_itt,bin_num in enumerate(binary_number):
	data = []
	posterior_data = []
	bayes_factor_data = []
	print(str(bin_num) + '\n')
	for index in range(n_chunks):
	#for bin_posn, atom in enumerate(bin_num):
		if bin_num[index]==1:
			print(index)
			data_value = assign_data_value(input_directory, index, index + 1, 1)
			post_value = get_posterior(input_directory, index, index + 1)
			bayes_factor_value = get_bayes_factor(input_directory, index, index + 1, 1)
			data.append(float(data_value[:-1]))
			posterior_data.append(float(post_value))
			bayes_factor_data.append(float(bayes_factor_value))
		elif bin_num[index] == 0:
			chunk_start = index
			chunk_end = index + 1
			chunk_value = 0
			data_value = assign_data_value(input_directory, chunk_start, chunk_end, chunk_value)
                        post_value = get_posterior(input_directory, chunk_start, chunk_end)
                        bayes_factor_value = get_bayes_factor(input_directory, chunk_start, chunk_end, chunk_value)
			data.append(float(data_value[:-1]))
			posterior_data.append(float(post_value))
			bayes_factor_data.append(float(bayes_factor_value))
		else:
			print("I'm sorry Dave, I can't do that for you.")
			quit(0)
	data_bins.append(data)
	bayes_bins.append(bayes_factor_data)
	h_bins.append(posterior_data)

output = str(args.output) 
outfile = open(output, 'w+')
outfile.seek(0)
for num,item in enumerate(data_bins):
	outfile.write(str(item) + '\n')
	print(str(num) + ': ' + str(item))
outfile.close()

bf_outpath = output.split('/')
bf_out = ''
for part in bf_outpath[:-1]:
	bf_out = bf_out + part + '/'

bf_out = bf_out + 'simple_bayes_factor_data.txt'

with open(bf_out, 'w') as b:
	for num,item in enumerate(bayes_bins):
		b.write(str(item) + '\n')

h_outpath = output.split('/')
h_out = ''
for part in h_outpath[:-1]:
        h_out = h_out + part + '/'

h_out = h_out + 'simple_h_posterior_data.txt'
with open(h_out, 'w') as h:
        for num,item in enumerate(h_bins):
                h.write(str(item) + '\n')

