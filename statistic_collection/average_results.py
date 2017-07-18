#!/usr/bin/env python

# This script is expected to read in the outputs from read_statistics.py, the measures collated, and taking an average and standard deviation of them both.

# This needs to read in 2 files for ech value of SNR, as well as the SNR value.

# Can we hard-code in the file system? /scratch/spxbp1/analysis_out/SNR[XX]/

from __future__ import division
import os
import numpy as np
from argparse import ArgumentParser
import ast

parser = ArgumentParser()

parser.add_argument("-S", "--SNR", dest = "SNR",
                   help = " SNR value to use on any given run", metavar = "FLOAT")

#parser.add_argument("-b", "--basedir", dest = "basedir",
#                   help = "Base directory - up one level from the SNR subdirectories eg /scratch/spxbp1/analysis_out/", metavar = "STRING")

#parser.add_argument("-m", "--mismatch_file", dest = "mismatch_file",
 #                  help = "Path to the mismatch file", metavar = "STRING")

#parser.add_argument("-p", "--position_file", dest = "position_file",
 #                  help = "Path to the position file.", metavar = "STRING")

#parser.add_argument("-c", "--is_correct_file", dest = "is_correct_file",
#                   help = "Path to the is-correct file.", metavar = "STRING")

parser.add_argument("-i", "--input_path", dest = "input_path",
                   help = "Full path to the input dictionary file.", metavar = "STRING")

parser.add_argument("-o", "--output_path", dest = "output_path",
                   help = "Full path to the ideal output file.", metavar = "STRING")

#parser.add_argument("-b", "--input_binary", dest = "input_binary",
#                   help = "Full path to the input_binary for each run.", metavar = "STRING")

args = parser.parse_args()

#SNR = args.SNR
#mismatch_path = str(args.mismatch_file)
#position_path = str(args.position_file)
#is_correct_path = str(args.is_correct_file)

#basedir = str(args.basedir)

#if basedir[-1]!='/':
#	basedir = basedir + '/'

# Don't have to cycle over SNR directory.
# Can just give it one SNR value

input_dir = args.input_path
mismatch_list = []
posn_list = []
#is_correct_list = []
#position = []
#correct = []
true_SNR_list = []
Best_guess_list = []
True_binary_list = []
Pulsar_number_list = []

with open(input_dir, 'r') as f:
	s = f.read()
	for line in s:
		stripline = line.strip('\n')
		line_dict = ast.literal_eval(stripline)
		mismatch_list.append(line_dict["Number wrong places"])
		posn_list.append(line_dict["List position"])
		is_correct_list.append(line_dict["Is correct"])
	`	true_SNR_list.append(line_dict["Full SNR"])
		Best_guess_list.append(line_dict["Best guess"])
		True_binary_list.append(line_dict["True binary"])
		Pulsar_number_list.append(line_dict["Pulsar number"])



number_mismatches = len(mismatch_list)
number_positions = len(posn_list)
number_corrects = len(is_correct_list)
if number_mismatches != number_positions:
	print('Lenth of lists containing mismnatches and positions are not the same.\n Please double check the analysis.')
	quit()
mismatch_mean = (np.sum(mismatch_list) + 0.0) / number_mismatches
posn_mean = (np.sum(posn_list) + 0.0) / number_positions
correct_mean = (np.sum(is_correct_list) + 0.0) / number_corrects

with open(args.output_path, 'a') as output:
	output.write('#####\n SNR = ' + str(SNR) + ' \n \tFor ' + str(number_mismatches) + ' test runs: \n \tMean configurations correctly guessed (1 is best): ' + str(correct_mean) + ' \n \tMean digits mismatched (0 is best): ' + str(mismatch_mean) + '\n \tMean rank of true binary (0 is best): ' + str(posn_mean) + '\n ##### \n ##### \n')
# Plot these measures
# Make a plotting finction

# Calculate total SNR
# Coherent adds as sqrt(t)
# Incoherent adds as 4thrt(t)
	
	




