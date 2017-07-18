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
import plotly.plotly as py
import plotly.tools as tls

parser = ArgumentParser()

parser.add_argument("-S", "--SNR", dest = "list_of_SNR",
                  help = "SNR of signal injected", metavar = "LIST")

parser.add_argument("-i", "--inputs", dest = "list_of_inputs",
                  help = "SNR of signal injected", metavar = "LIST")

parser.add_argument("-t", "--input_type", dest = "input_type",
                  help = "SNR of signal injected", metavar = "STRING")

parser.add_argument("-o", "--output_file", dest = "output_file",
                  help = "SNR of signal injected", metavar = "STRING")

parser.add_argument("-L", "--list_of_tuples", dest = "list_of_tuples",
                  help = "SNR of signal injected", metavar = "LIST")

args = parser.parse_args()

def plot_boxplot(list_of_inputs, list_of_SNR, input_type, output_file):
	data = list_of_inputs
	pt = plt.figure()
	pt.boxplot(data)
	pt.xticks(arrange(len(list_of_SNR)), list_of_SNR)
	pt.xlabel('Chunk SNR Value')
	pt.ylabel(input_type)
	pt.savefig(output_file)



def plot_scatterplot(list_of_tuples, input_type, output_file):
	value = []
	SNR = []
	for pair in list_of_tuples:
		value.append(float(pair[0]))
		SNR.append(float(pair[1]))
	ax = plt.figure()
	ax.plot(value, SNR)
	













