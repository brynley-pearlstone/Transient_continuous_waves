

from __future__ import division
import os
import numpy as np
from argparse import ArgumentParser
import ast
import plot_outputs as pt

parser = ArgumentParser()

parser.add_argument("-S", "--SNRs", dest = "SNRs",
                   help = "List of SNR values to use on any given run", metavar = "LIST")

parser.add_argument("-d", "--basedir", dest = "basedir",
                   help = "Base directory before all of the SNR dirs get split", metavar = "STRING")

parser.add_argument("-l", "--dict_list", dest = "dict_list",
                   help = "List of paths from basedir each library", metavar = "LIST")


args = parser.parse_args()

if args.basedir[-1] != '/':
	basedir = str(args.basedir) + '/'
else:
	basedir = str(args.basedir)
dicts_list = args.dict_list.strip('[')
dict_list = dicts_list.strip(']')
dictionaries = dict_list.split(',')
#print(dictionaries)

SNRs_list = args.SNRs.strip('[')
SNR_list = SNRs_list.strip(']')
list_SNRs = SNR_list.split(',')
list_of_SNRs = []
for item in list_SNRs:
	list_of_SNRs.append(float(item))

full_dict_path = []
for dtry in dictionaries:#args.dict_list:
	full_dict_path.append(basedir + str(dtry))	
	
mismatch_list = []
posn_list = []
is_correct_list = []
#position = []
#correct = []
true_SNR_list = []
Best_guess_list = []
True_binary_list = []
Pulsar_number_list = []

all_mismatch = []
all_posn = []
all_correct = []
all_true_SNR = []
all_best_guess = []
all_true_binary = []

		
full_dict = []
with open(basedir + 'all_trials_dict.txt', 'w') as outfile:
	for fname in full_dict_path:
		with open(fname) as infile:
			for line in infile:
				stripline = line.strip('\n')
	        	        line_dict = ast.literal_eval(stripline)
				#print(line_dict)
		                mismatch_list.append(int(line_dict["Number wrong places"]))
				#print(mismatch_list)
                		posn_list.append(int(line_dict["List position"]))
        	        	is_correct_list.append(int(line_dict["Is_correct"]))
		                true_SNR_list.append(float(line_dict["Full SNR"]))
        	        	Best_guess_list.append(line_dict["Best guess"])
        		        True_binary_list.append(line_dict["True binary"])
	                	Pulsar_number_list.append(int(line_dict["Pulsar number"]))
				outfile.write(line)
				full_dict.append(line)
			# Define list of lists
			all_mismatch.append(mismatch_list) 
			all_posn.append(posn_list)
			all_correct.append(is_correct_list)
			all_true_SNR.append(true_SNR_list)
			all_best_guess.append(Best_guess_list)
			all_true_binary = []
				
with open(basedir + 'all_mismatch.txt', 'w') as outfile:
        for part in all_mismatch:
		outfile.write(str(part) + '\n')

with open(basedir + 'all_posn.txt', 'w') as outfile:
	for part in all_posn:
	        outfile.write(str(part) + '\n')

with open(basedir + 'all_true_SNR.txt', 'w') as outfile:
	for part in all_true_SNR:
	        outfile.write(str(part) + '\n')



#print(all_mismatch)
pt.plot_boxplot(all_mismatch, list_of_SNRs, 'Number of mismatched bits', basedir + 'mismatch_boxplot.png')
pt.plot_boxplot(all_correct, list_of_SNRs, 'Number of correct binary number guesses', basedir + 'is_correct_boxplot.png')
pt.plot_boxplot(all_posn, list_of_SNRs, 'Position of true binary on sorted binaries list', basedir + 'posn_boxplot.png')
pt.plot_boxplot(all_true_SNR, list_of_SNRs, 'Full tria SNR value', basedir + 'SNR_boxplot.png')

# Start tupples
S_list = []
m_list = []
p_list = []
c_list = []
for num,SNR in enumerate(all_true_SNR):
	S_list.append(SNR)
	m_list.append(all_mismatch[num])
	p_list.append(all_posn[num])
	c_list.append(all_correct[num])

with open(basedir + 'S_list.txt', 'w') as outfile:
	outfile.write(str(S_list))

with open(basedir + 'm_list.txt', 'w') as outfile:
        outfile.write(str(S_list))

with open(basedir + 'p_list.txt', 'w') as outfile:
        outfile.write(str(S_list))


pt.plot_scatterplot(S_list, m_list, 'Number of mismatched bits', basedir + 'mismatch_spread.png')
pt.plot_scatterplot(S_list, p_list, 'Position of true binary on sorted binaries list', basedir + 'position_spread.png')
pt.plot_scatterplot(S_list, c_list, 'Number of correct binary number guesses', basedir + 'is_correct_spread.png')



#with open(input_dir, 'r') as f:
#        s = f.read()
#        for line in s:
#                stripline = line.strip('\n')
#                line_dict = ast.literal_eval(stripline)
#                mismatch_list.append(line_dict["Number wrong places"])
#                posn_list.append(line_dict["List position"])
#                is_correct_list.append(line_dict["Is correct"])
#        `       true_SNR_list.append(line_dict["Full SNR"])
#                Best_guess_list.append(line_dict["Best guess"])
#                True_binary_list.append(line_dict["True binary"])
#                Pulsar_number_list.append(line_dict["Pulsar number"])
#
#






