#!/usr/bin/env python

# This script is expected to read in the outputs from read_statistics.py, the measures collated, and taking an average and standard deviation of them both.

# This needs to read in 2 files for ech value of SNR, as well as the SNR value.

# Can we hard-code in the file system? /scratch/spxbp1/analysis_out/SNR[XX]/

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

parser.add_argument("-i", "--label", dest = "label",
                   help = "label for output files", metavar = "STR")

parser.add_argument("-a", "--handle", dest = "handle",
                   help = "true binary to sort for", metavar = "STR")

args = parser.parse_args()

if args.basedir[-1] != '/':
	basedir = str(args.basedir) + '/'
else:
	basedir = str(args.basedir)

full_dict_path = []
dicts = str(args.dict_list).strip('[')
dicts2 = str(dicts.strip(']'))
dict_list = dicts2.split(',')
for dtry in dict_list:
	full_dict_path.append(basedir + str(dtry))	
	
handle = str(args.handle)
label = str(args.label)
mismatch_list = []
posn_list = []
is_correct_list = []
#position = []
#correct = []
true_SNR_list = []
Best_guess_list = []
True_binary_list = []
Pulsar_number_list = []
chunk_SNR_list = []

all_mismatch = []
all_posn = []
all_correct = []
all_true_SNR = []
all_best_guess = []
all_true_binary = []
all_SNR = []

all_mismatch2 = []
all_posn2 = []
all_correct2 = []
all_true_SNR2 = []
all_best_guess2 = []
all_true_binary2 = []
all_SNR2 = []		
correctportion = []
all_correct_errors = []
full_dict = []
with open(basedir + 'all_trials_dict.txt', 'w') as outfile:
	for fname in full_dict_path:
		mismatch_list = []
		posn_list = []
		is_correct_list = []
		#position = []
		#correct = []
		true_SNR_list = []
		Best_guess_list = []
		True_binary_list = []
		Pulsar_number_list = []
		chunk_SNR_list = []
		totalsum = 0
		correctsum = 0
		with open(fname) as infile:
			for line in infile:
				stripline = line.strip('\n')
	        	        line_dict = ast.literal_eval(stripline)
#				print(str(line_dict["True binary"]))
				if line_dict["True binary"] == handle:
					print(str(line_dict["True binary"]))
					#print(line_dict)
			                mismatch_list.append(int(line_dict["Number wrong places"]))
                			posn_list.append(int(line_dict["List position"]))
        	        		is_correct_list.append(int(line_dict["Is_correct"]))
		                	true_SNR_list.append(float(line_dict["Full SNR"]))
	        	        	Best_guess_list.append(line_dict["Best guess"])
        			        True_binary_list.append(line_dict["True binary"])
	        	        	Pulsar_number_list.append(line_dict["Pulsar number"])
					chunk_SNR_list.append(int(line_dict["Chunk_SNR"]))
					outfile.write(line)
					full_dict.append(line)
			                all_mismatch.append(int(line_dict["Number wrong places"]))#(mismatch_list)
                			all_posn.append(int(line_dict["List position"]))#(posn_list)
                			all_correct.append(int(line_dict["Is_correct"]))#(is_correct_list)
                			all_true_SNR.append(float(line_dict["Full SNR"]))#(true_SNR_list)
	                		all_best_guess.append(line_dict["Best guess"])#(Best_guess_list)
        	        		all_true_binary.append(line_dict["True binary"])#(True_binary_list)
                			all_SNR.append(int(line_dict["Chunk_SNR"]))#(chunk_SNR_list)
					totalsum += 1
					correctsum += int(line_dict["Is_correct"])

				# Define list of lists
		if totalsum != 0:
			correctportion.append((correctsum + 0.0)/(totalsum + 0.0))
		elif totalsum==0:
			correctportion.append(0)
		all_mismatch2.append(mismatch_list) 
		all_posn2.append(posn_list) 
		all_correct2.append(is_correct_list) 
		all_true_SNR2.append(true_SNR_list) 
		all_best_guess2.append(Best_guess_list) 
		all_true_binary2.append(True_binary_list) 
		all_SNR2.append(chunk_SNR_list)
		all_correct_errors.append(np.var(is_correct_list)/np.sqrt(len(is_correct_list)))
#print(all_mismatch)
pt.plot_pixelplot(all_SNR,all_mismatch, [0,1,2,3,4,5,6,7,8,9], [0,1,2,3,4,5,6,7,8,9,10,11] ,"Number of incorrect chunks", basedir + 'mismatch_histogram.png')

pt.plot_pixelplot(all_SNR, all_posn,[1,2,3,4,5,6,7,8,9,10,11], range(np.amax(all_posn)) ,"Rank position of true intermitency.", basedir + 'posn_histogram' + label + '.png')
pt.plot_pixelplot(all_SNR, all_correct, [0,1,2],[0,1,2,3,4,5,6,7,8,9,10,11],"Proportion of correctly recovered intermittencies", basedir + 'is_correct_histogram' + label + '.png')
pt.plot_pixelplot(all_SNR, all_true_SNR, [0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40],[0,1,2,3,4,5,6,7,8,9,10,11] , "Signal SNR integrated over intermittency.", basedir + 'full_SNR_histogram' + label + '.png')

# Start tupples
S_list = []
m_list = []
p_list = []
c_list = []
average_correct = []
for num,SNR in enumerate(all_SNR):
	S_list.append(SNR)
	m_list.append(all_mismatch[num])
	p_list.append(all_posn[num])
	c_list.append(all_correct[num])
	average_correct.append(np.mean(all_correct[num]))
  
pt.plot_scatterplot(all_mismatch, all_SNR, [-1,np.amax(all_mismatch) + 1], 'Number of incorrect chunks', basedir + 'mismatch_spread' + label + '.png')
pt.plot_scatterplot(all_posn, all_SNR, [-1,np.amax(all_posn) + 1], 'Ranked position of true intemittency', basedir + 'position_spread' + label + '.png')
pt.plot_scatterplot(all_correct, all_SNR, [-1,np.amax(all_correct) + 1], 'Proportion of correctly recovered intemittencies', basedir + 'is_correct_spread' + label + '.png')

SNR_list = [1,2,3,4,5,6,7,8,9,10]

is_correct_errors = all_correct_errors
# var(x)/sqrt(n)
print('Errors = ' + str(is_correct_errors))
pt.is_correct_plot(SNR_list, correctportion, is_correct_errors, basedir + 'is_correct_line' + label + '.png')

#list_of_percents = np.zeros([12,12])
list_of_percents2 = np.zeros([10,10])
list_of_proportions = np.zeros([10,10])

for i,m in enumerate(m_list):
	total = len(m_list)
	for j in range(9):
		if m == j:
#			print(list_of_percents2)
#			print(S_list[i])
#			print(j)
			list_of_percents2[j,int(S_list[i])-1] += 1

print(all_SNR2)
for i,m in enumerate(all_SNR2):
	total = len(m)
	for j in range(9):
		list_of_proportions[j,i] = (100 * list_of_percents2[j,i])/total

is_correct_perc = [i * 100 for i in correctportion]
#print(is_correct_perc)
#pt.stacked_bar(SNR_list, [0,1,2,3,4,5,6,7,8], list_of_percents2, is_correct_perc, basedir + 'stacked_bar_mismatch' + label + '.png')

pt.stacked_bar(SNR_list, [0,1,2,3,4,5,6,7,8], list_of_proportions, is_correct_perc, basedir + 'stacked_bar_proportional_mismatch' + label + '.png')

