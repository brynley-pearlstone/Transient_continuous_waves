#!/usr/bin/env python

# This script is intended to do an analysis of several files.
# It ill be called by a dag job - and run several times simultaneously
# Inputs:
# Path to correct_binary_position
# Path to true_binary
# Path to guessed_binary

from __future__ import division
import numpy as np
import matplotlib as mpl
from argparse import ArgumentParser
import os
mpl.rcParams['agg.path.chunksize'] = 10000
import matplotlib.pyplot as plt
import math
import matplotlib as mpl
import ast


parser = ArgumentParser()

parser.add_argument("-t", "--true_binary", dest = "true_binary",
                  help = "Path to file containing the true binary number used.", metavar = "STRING")

parser.add_argument("-s", "--sorted_binaries", dest = "sorted_binaries",
                  help = "Path to file containing the list of sorted binary numbers. Best guess at the end.", metavar = "STRING")

parser.add_argument("-d", "--output_dict", dest = "output_dict",
                  help = "Path to file containing the ouput dictionary, and various other outputs.", metavar = "STRING")

parser.add_argument("-o", "--output", dest = "output",
                  help = "Path to file where the average mismatch for every run is written.", metavar = "STRING")

parser.add_argument("-n", "--Pulsar_number", dest = "pulsar",
                  help = "NUmber of pulsar that corresponds to the results.", metavar = "STRING")

parser.add_argument("-S", "--SNR", dest = "SNR",
                  help = "SNR of signal injected", metavar = "FLOAT")

args = parser.parse_args()

# Parse arguments and double check that files exist

true_binary_path = str(args.true_binary)
if not os.path.isfile(true_binary_path):
	print("Please double check the path to the input_binary file")
	quit()

sorted_binaries_path = str(args.sorted_binaries)
if not os.path.isfile(sorted_binaries_path):
        print("Please double check the path to the sorted_binaries file")
        quit()

output_dict_path = str(args.output_dict)
if not os.path.isfile(output_dict_path):
        print("Please double check the path to the output dictionary file")
        quit()

#Read in files

output = {}

with open(output_dict_path, 'r') as output_dict:
	correct_binary_place = output_dict.readlines()[1].strip('\n')

with open(output_dict_path, 'r') as output_dict:
	best_guess_info = output_dict.readlines()[-1].strip('\n')

guess_dict = ast.literal_eval(best_guess_info)

Guess_posterior = guess_dict["sorted_posteriors"]



# Write position down the list

position_dict = {"List position" : correct_binary_place }
output.update(position_dict)

# calculate the difference in the bits

with open(sorted_binaries_path, 'r') as sorted_binaries:
	best_guess = sorted_binaries.readlines()[-1].strip('\n')
	best_guess0 = best_guess.strip('\n')
        best_guess1 = best_guess0.strip('[')
        best_guess2 = best_guess1.strip(']')
        best_guess3 = best_guess2.split(', ')
	guess = []
	for chara in best_guess3:
		guess.append(int(chara))

best_guess = guess
true_binary = []
with open(true_binary_path, 'r') as binary_lines:
	input_binary = binary_lines.readlines()[1].strip('\n')
	for char in input_binary:
		true_binary.append(int(char))

# Check both are the same length

if len(best_guess)!=len(true_binary):
	print('Please make sure your tests assume the same number of chunks as the input')
	quit()

number_wrong_places = 0
for posn in range(len(true_binary)):
	number_wrong_places += np.abs(int(true_binary[posn]) - int(best_guess[posn]))

# Write the mismatch to a file

no_wrong_pl_dict = {"Number wrong places" : str(number_wrong_places) }

output.update(no_wrong_pl_dict)

if number_wrong_places == 0:
	correct_dict = {"Is_correct" : "1" }
else:
	correct_dict = {"Is_correct" : "0" }

output.update(correct_dict)


info_dict = {"Pulsar number" : args.pulsar , "True binary": str(true_binary), "Best guess":str(best_guess), "Posterior":float(Guess_posterior)}
output.update(info_dict)

cSNR = float(args.SNR)
full_SNR = 0

# Compute complete injected SNR
# Need to know binary make up
# Get this from input binary var name true_binary

SNR_dict = {"Chunk_SNR" : cSNR}

output.update(SNR_dict)

print(output)
with open(args.output, 'a') as write_out:
       write_out.write(str(output) + '\n')
print("Variables written out")
