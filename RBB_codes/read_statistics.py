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

#Consider changing to supplying 3 directories (normal, bayescut and postcut), then append with /output.txty, /sorted_binaries.txt etc)

parser.add_argument("-t", "--true_binary", dest = "true_binary",
                  help = "Path to file containing the true binary number used.", metavar = "STRING")

# parser.add_argument("-s", "--sorted_binaries", dest = "sorted_binaries",
#                   help = "Path to file containing the list of sorted binary numbers. Best guess at the end.", metavar = "STRING")

parser.add_argument("-d", "--output_dir", dest = "output_dir",
                  help = "Path to file containing the output directory, and various other outputs. (/analysis_out)", metavar = "STRING")

parser.add_argument("-b", "--bayescut_output_dir", dest = "bayescut_dir",
                  help = "Path to file containing the output directory, and various other outputs for the bayescut data.", metavar = "STRING")

parser.add_argument("-p", "--posterior_output_dir", dest = "postcut_dir",
                  help = "Path to file containing the output directory, and various other outputs for the posterior cut data.", metavar = "STRING")

parser.add_argument("-s", "--simple_ver_output_dir", dest = "simple_dir",
                  help = "Path to file containing the output directory, and various other outputs for the simple version of RBB data.", metavar = "STRING")

parser.add_argument("-o", "--output", dest = "output",
                  help = "Path to file where the average mismatch for every run is written.", metavar = "STRING")

parser.add_argument("-B", "--Bayes_output", dest = "bayes_output",
                  help = "Path to file where the average mismatch for every bayescut run is written.", metavar = "STRING")

parser.add_argument("-P", "--post_output", dest = "post_output",
                  help = "Path to file where the average mismatch for every posterior-cut run is written.", metavar = "STRING")

parser.add_argument("-V", "--simple_output", dest = "simple_output",
                  help = "Path to file where the average mismatch for every simple run is written.", metavar = "STRING")

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

sorted_binaries_path = str(args.output_dir) + 'sorted_binaries.txt'
if not os.path.isfile(sorted_binaries_path):
        print("Please double check the path to the sorted_binaries file")
        quit()

output_dict_path = str(args.output_dir) + 'output.txt'
if not os.path.isfile(output_dict_path):
        print("Please double check the path to the output dictionary file")
        quit()

bayescut_output_dict_path = str(args.bayescut_dir) + 'output.txt'
if not os.path.isfile(bayescut_output_dict_path):
        print("Please double check the path to the bayescut output dictionary file")
        quit()

postcut_output_dict_path = str(args.postcut_dir) + 'output.txt'
if not os.path.isfile(postcut_output_dict_path):
        print("Please double check the path to the postcut output dictionary file")
        quit()

simple_output_dict_path = str(args.simple_dir) + 'output.txt'
if not os.path.isfile(simple_output_dict_path):
        print("Please double check the path to the simple output dictionary file")
        quit()

bayes_sorted_binaries_path = str(args.bayescut_dir) + 'sorted_binaries.txt'
if not os.path.isfile(bayes_sorted_binaries_path):
        print("Please double check the path to the bayescut sorted_binaries file")
        quit()

postcut_sorted_binaries_path = str(args.postcut_dir) + 'sorted_binaries.txt'
if not os.path.isfile(postcut_sorted_binaries_path):
        print("Please double check the path to the postcut sorted_binaries file")
        quit()

simple_sorted_binaries_path = str(args.simple_dir) + 'sorted_binaries.txt'
if not os.path.isfile(simple_sorted_binaries_path):
        print("Please double check the path to the simple sorted_binaries file")
        quit()

#Read in files

output = {}
bayes_output = {}
post_output = {}
simple_output = {}

# Write position of the true binary down the output list

with open(output_dict_path, 'r') as output_dict:
#	print("out_dict[1] = " + output_dict.readlines()[1])
	correct_binary_place = output_dict.readlines()[1].strip()
        output_dict.seek(0)
	print("out_dict[-1] = " + output_dict.readlines()[-1])
	output_dict.seek(0)
	coherent_correct_dict_STR =  output_dict.readlines()[-1].strip()

position_dict = {"List position" : correct_binary_place }
output.update(position_dict)


#with open(bayescut_output_dict_path, 'r') as bayescut_dict:
#        b_correct_binary_place = bayescut_dict.readlines()[1].strip('\n')
#	bayescut_dict.seek(0)
#	bayescut_correct_dict_STR =  bayescut_dict.readlines()[-1].strip('\n')

#b_position_dict = {"List position" : b_correct_binary_place }
#bayes_output.update(b_position_dict)


#with open(postcut_output_dict_path, 'r') as postcut_dict:
#        p_correct_binary_place = postcut_dict.readlines()[1].strip('\n')
#	postcut_dict.seek(0)
#	postcut_correct_dict_STR =  postcut_dict.readlines()[-1].strip('\n')

#p_position_dict = {"List position" : p_correct_binary_place }
#post_output.update(p_position_dict)


with open(simple_output_dict_path, 'r') as simple_dict:
        s_correct_binary_place = simple_dict.readlines()[1].strip('\n')
	simple_dict.seek(0)
	incoherent_correct_dict_STR =  simple_dict.readlines()[-1].strip('\n')#simple_best_guess = best_guess

s_position_dict = {"List position" : s_correct_binary_place }
simple_output.update(s_position_dict)


# Convert the string containing dicts into dicts, and read them

coherent_correct_dict = ast.literal_eval(coherent_correct_dict_STR)
coherent_guess_posterior = coherent_correct_dict['sortd_posteriors']


#bayescut_correct_dict = ast.literal_eval(bayescut_correct_dict_STR)
#bayescut_guess_posterior = bayescut_correct_dict['sortd_posteriors']


#postcut_correct_dict = ast.literal_eval(postcut_correct_dict_STR)
#postcut_guess_posterior = postcut_correct_dict['sortd_posteriors']


incoherent_correct_dict = ast.literal_eval(incoherent_correct_dict_STR)
incoherent_guess_posterior = incoherent_correct_dict['sorted_posteriors']



# calculate the difference in the bits

#with open(sorted_binaries_path, 'r') as sorted_binaries:
#	postcut_best_guess = p_guess

with open(sorted_binaries_path, 'r') as sorted_binaries:
        #print(sorted_binaries.readlines())
        best_guess = sorted_binaries.readlines()[-1]
        best_guess0 = best_guess.strip('\n')
        best_guess1 = best_guess0.strip('[')
        best_guess2 = best_guess1.strip(']')
        best_guess25 = best_guess2.strip(' ')
        best_guess3 = best_guess25.split(', ')
        c_guess = []
        for chara in best_guess3:
                c_guess.append(int(chara.strip()))

Best_guess = c_guess



with open(simple_sorted_binaries_path, 'r') as s_sorted_binaries:
        #print(sorted_binaries.readlines())
        best_guess = s_sorted_binaries.readlines()[-1]
        best_guess0 = best_guess.strip('\n')
        best_guess1 = best_guess0.strip('[')
        best_guess2 = best_guess1.strip(']')
        best_guess25 = best_guess2.strip(' ')
        best_guess3 = best_guess25.split(', ')
        s_guess = []
        for chara in best_guess3:
                s_guess.append(int(chara.strip()))

simple_best_guess = s_guess

true_binary = []
with open(true_binary_path, 'r') as binary_lines:
	guessed_binary = binary_lines.readlines()[1].strip('\n')
	for char in guessed_binary:
		true_binary.append(int(char))

# Check both are the same length

if len(Best_guess)!=len(true_binary):
	print('Please make sure your tests assume the same number of chunks as the input')
	print('Best guess = ' + str(Best_guess) + ' with length ' + str(len(Best_guess)))
	print('True binary = ' + str(true_binary) + ' with length ' + str(len(true_binary)))
	quit()

number_wrong_places = 0
for posn in range(len(true_binary)):
	number_wrong_places += np.abs(int(true_binary[posn]) - int(Best_guess[posn]))

#bayescut_number_wrong_places = 0
#for posn in range(len(true_binary)):
#        bayescut_number_wrong_places += np.abs(int(true_binary[posn]) - int(bayescut_best_guess[posn]))

#postcut_number_wrong_places = 0
#for posn in range(len(true_binary)):
#        postcut_number_wrong_places += np.abs(int(true_binary[posn]) - int(postcut_best_guess[posn]))

simple_number_wrong_places = 0
for posn in range(len(true_binary)):
        simple_number_wrong_places += np.abs(int(true_binary[posn]) - int(simple_best_guess[posn]))

# Write the mismatch to a file

no_wrong_pl_dict = {"Number wrong places" : str(number_wrong_places) }
output.update(no_wrong_pl_dict)

#b_no_wrong_pl_dict = {"Number wrong places" : str(bayescut_number_wrong_places) }
#bayes_output.update(b_no_wrong_pl_dict)

#p_no_wrong_pl_dict = {"Number wrong places" : str(postcut_number_wrong_places) }
#post_output.update(p_no_wrong_pl_dict)

s_no_wrong_pl_dict = {"Number wrong places" : str(simple_number_wrong_places) }
simple_output.update(s_no_wrong_pl_dict)


if number_wrong_places == 0:
	correct_dict = {"Is_correct" : "1", "Posterior" : coherent_guess_posterior }
else:
	correct_dict = {"Is_correct" : "0","Posterior" : coherent_guess_posterior }

#if bayescut_number_wrong_places == 0:
#        b_correct_dict = {"Is_correct" : "1","Posterior" : bayescut_guess_posterior }
#else:
#        b_correct_dict = {"Is_correct" : "0","Posterior" : bayescut_guess_posterior }

#if postcut_number_wrong_places == 0:
#        p_correct_dict = {"Is_correct" : "1","Posterior" : postcut_guess_posterior }
#else:
#        p_correct_dict = {"Is_correct" : "0","Posterior" : postcut_guess_posterior }

if simple_number_wrong_places == 0:
        s_correct_dict = {"Is_correct" : "1","Posterior" : incoherent_guess_posterior }
else:
        s_correct_dict = {"Is_correct" : "0","Posterior" : incoherent_guess_posterior }


output.update(correct_dict)
#bayes_output.update(b_correct_dict)
#post_output.update(p_correct_dict)
simple_output.update(s_correct_dict)

info_dict = {"Pulsar number" : args.pulsar , "True binary": str(true_binary).strip(), "Best guess":str(best_guess).strip()}
output.update(info_dict)

#b_info_dict = {"Pulsar number" : args.pulsar , "True binary": str(true_binary), "Best guess":str(bayescut_best_guess)}
#bayes_output.update(b_info_dict)

#p_info_dict = {"Pulsar number" : args.pulsar , "True binary": str(true_binary), "Best guess":str(postcut_best_guess)}
#post_output.update(p_info_dict)

s_info_dict = {"Pulsar number" : args.pulsar , "True binary": str(true_binary).strip(), "Best guess":str(simple_best_guess).strip()}
simple_output.update(s_info_dict)


cSNR = float(args.SNR)
full_SNR = 0
SNR_dict = {"Chunk_SNR" : cSNR}


output.update(SNR_dict)
#bayes_output.update(SNR_dict)
#post_output.update(SNR_dict)
simple_output.update(SNR_dict)

print(output)

with open(args.output, 'a') as write_out:
       write_out.write(str(output) + '\n')

#with open(args.bayes_output, 'a') as b_write_out:
#       b_write_out.write(str(bayes_output) + '\n')

#with open(args.post_output, 'a') as p_write_out:
#       p_write_out.write(str(post_output) + '\n')

with open(args.simple_output, 'a') as s_write_out:
       s_write_out.write(str(simple_output) + '\n')

print("Variables written out")
