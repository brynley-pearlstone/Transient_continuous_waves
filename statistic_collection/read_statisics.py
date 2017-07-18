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

parser = ArgumentParser()

parser.add_argument("-t", "--true_binary", dest = "true_binary",
                  help = "Path to file containing the true binary number used.", metavar = "STRING")

parser.add_argument("-s", "--sorted_binaries", dest = "sorted_binaries",
                  help = "Path to file containing the list of sorted binary numbers. Best guess at the end.", metavar = "STRING")

parser.add_argument("-d", "--output_dict", dest = "output_dict",
                  help = "Path to file containing the ouput dictionary, and various other outputs.", metavar = "STRING")

#parser.add_argument("-m", "--mismatch", dest = "mismatch",
#                  help = "Path to file where the average mismatch for every run is written.", metavar = "STRING")

parser.add_argument("-o", "--output", dest = "output",
                  help = "Path to file where the average mismatch for every run is written.", metavar = "STRING")

#parser.add_argument("-l", "--list_position", dest = "list_position",
#                  help = "Path to file where the list position is written.", metavar = "STRING")

#parser.add_argument("-c", "--correct", dest = "correct",
#                  help = "Path to file containing measures of whether a given run is correct or not.", metavar = "STRING")

#parser.add_argument("-i", "--info_path", dest = "info_path",
#                  help = "Path to write out extra information about each pulsar.", metavar = "STRING")

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

# Write position down the list

#with open(args.list_position, 'a') as list_posn_write:
#	list_posn_write.write(str(correct_binary_place) + '\n' )

position_dict = {"List position" : correct_binary_place }
output.update(position_dict)

# calculate the difference in the bits



with open(sorted_binaries_path, 'r') as sorted_binaries:
	#print(sorted_binaries.readlines())
	best_guess = sorted_binaries.readlines()[-1]
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
	guessed_binary = binary_lines.readlines()[1].strip('\n')
	for char in guessed_binary:
		true_binary.append(int(char))

# Check both are the same length

if len(best_guess)!=len(true_binary):
	print('Please make sure your tests assume the same number of chunks as the input')
	quit()

number_wrong_places = 0
for posn in range(len(true_binary)):
	number_wrong_places += np.abs(int(true_binary[posn]) - int(best_guess[posn]))

# Write the mismatch to a file

#with open(args.mismatch, 'a') as mismatch_write:
#	mismatch_write.write(str(number_wrong_places) + '\n')

no_wrong_pl_dict = {"Number wrong places" : str(number_wrong_places) }

output.update(no_wrong_pl_dict)

#with open(args.correct, 'a') as correct_write:
if number_wrong_places == 0:
	#with open(args.correct, 'a') as correct_write:
	correct_dict = {"Is_correct" : "1" }
#        correct_write.write(str(1) + '\n')
else:
#	correct_write.write(str(0) + '\n')
	correct_dict = {"Is_correct" : "1" }

output.update(correct_dict)

#with open(args.info_path, 'a') as write_info:
#	write_info.write('Pulsar number: ' + args.pulsar + '.\n True binary: ' + str(true_binary) + '.\n Best guess: ' + str(best_guess) + '.\n\n')

info_dict = {"Pulsar number" : args.pulsar , "True binary": str(true_binary), "Best guess":str(best_guess)}
output.update(info_dict)

cSNR = float(args.SNR)
full_SNR = 0

# Compute complete injected SNR
# Need to know binary make up
# Get this from input binary var name true_binary

#for place,bit in enumerate(true_binary):
place = 0
while place < len(true_binary):
	bit = true_binary[place]	
	if bit==0:
		temp_SNR = 0
		block_SNR = 0
	elif bit==1 and true_binary[place+1]==0:
		temp_SNR = 1 * cSNR
		block_SNR = 0
	elif bit==1 and true_binary[place+1]==1:
		block_length = 1
		while true_binary[place] == 1 and true_binary[place+1]==1:
			block_length += 1
			place += 1
		block_SNR = np.sqrt(cSNR * block_length)
		print("place = " + str(place))
		print("block_length = " + str(block_length))
		print(true_binary)
		print("Block_SNR = " + str(block_SNR))
	full_SNR = full_SNR + (temp_SNR)**0.25 + (block_SNR)**0.25
	place += 1
	print("Full SNR = " + str(full_SNR) + " at place " + str(place))
SNR_dict = {"Full SNR" : full_SNR, "Chunk_SNR" : cSNR}

output.update(SNR_dict)

print(output)

with open(args.output, 'a') as write_out:
       write_out.write(str(output) + '\n')

print("Variables written out")
