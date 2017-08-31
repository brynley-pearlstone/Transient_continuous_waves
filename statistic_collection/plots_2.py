#!/usr/bin/env python
                  
# This script is intended to do an analysis of several files.
# It ill be called by a dag job - and run several times simultaneously
# Inputs:         
# Path to correct_binary_position
# Path to true_binary
# Path to guessed_binary 

#from __future__ import division
#import numpy as np
#import matplotlib as mpl
#from argparse import ArgumentParser
#import os
#mpl.rcParams['agg.path.chunksize'] = 10000
#import matplotlib.pyplot as plt
#import math
#import matplotlib as mpl
##import plotly.plotly as py
#import plotly.tools as tls

def plot_boxplot(list_of_inputs, list_of_SNR, input_type, output_file):
	import numpy as np
	import matplotlib as mpl
	mpl.use('Agg')
	mpl.rcParams['agg.path.chunksize'] = 10000
	import matplotlib.pyplot as plt
	plt.ioff()
	data = list_of_inputs
	plt.boxplot(data)
	plt.xticks(range(len(list_of_SNR)), list_of_SNR) 
	plt.xlabel('Chunk SNR Value')
	plt.ylabel(input_type)
	plt.savefig(output_file)


def plot_pixelplot(list_of_inputs, list_of_SNR, binarray_x, binarray_y, input_type, output_file):
        import numpy as np
        import matplotlib as mpl
        mpl.use('Agg')
        mpl.rcParams['agg.path.chunksize'] = 10000
        import matplotlib.pyplot as plt
        plt.ioff()
        data = np.array(list_of_inputs)
	SNRs = np.array(list_of_SNR)
#	print(binarray_x)
	binarray = [np.array(binarray_x), np.array(binarray_y)]
#	print(binarray)
        plt.hist2d(data,SNRs,bins=binarray,cmin=1)
        plt.xlabel('Chunk SNR Value')
        plt.ylabel(input_type)
	plt.colorbar()
#	for axis in [plt.xaxis, plt.yaxis]
#		axis.set(ticks=np.arange(0.5, len(labels)), ticklabels=labels)
        plt.savefig(output_file)


def plot_scatterplot(list_of_SNRs, list_of_values, ylims, input_type, output_file):
        import numpy as np
        import matplotlib as mpl
        mpl.use('Agg')
	mpl.rcParams['agg.path.chunksize'] = 10000
        import matplotlib.pyplot as plt
	plt.figure()
	plt.plot(list_of_values, list_of_SNRs,'b+')
	plt.xlabel('Total trial SNR')
	plt.ylabel(input_type)
	plt.ylim(ylims)
	plt.title(str(input_type) + ' distribution over trial SNR')
	plt.savefig(output_file)
	
	
def is_correct_plot(list_of_SNRs, list_of_values, list_of_errors, output_file):
        import numpy as np
        import matplotlib as mpl
        mpl.use('Agg')
        mpl.rcParams['agg.path.chunksize'] = 10000
        import matplotlib.pyplot as plt
        plt.figure()
#        plt.plot(list_of_SNRs, list_of_values)
        plt.errorbar(list_of_SNRs, list_of_values, yerr=list_of_errors, fmt='--o')
	plt.xlabel('Chunk SNR')
        plt.ylabel('Proportion of intermittencies corectly recovered')
        plt.ylim([0,1])
#        plt.title('Proportion of correctly recovered intermittencies by chunk SNR')
        plt.savefig(output_file)


def stacked_bar(SNR_list, list_of_mismatches, list_of_percentages, is_correct_perc, output_file):
	import numpy as np
	import matplotlib as mpl
	import matplotlib.pyplot as plt
        mpl.use('Agg')
	mpl.rcParams['agg.path.chunksize'] = 10000
        SNRlist = []
        for SNR in SNR_list: 
                SNRlist.append(str(SNR))
        segments = len(list_of_mismatches)
#	people = ('A','B','C','D','E','F','G','H')
#	segments = 4
	# generate some multi-dimensional data & arbitrary labels
	data = list_of_percentages
	percentages = list_of_percentages
#	print("Percentages = \n")
#	for item in percentages:
#		print(item)
	x_pos = np.arange(len(SNRlist)) 
	
	f, px = plt.subplots(1,1)
#	fig, px = plt.figure()
	colors =['w','y','r','m','b','c','g','k','gray']
	patch_handles = []
	btm = np.zeros(len(SNRlist)) # left alignment of data starts at zero
	for i, d in enumerate(data):
		patch_handles.append(plt.barh(d, x_pos, color=colors[i%len(colors)], align='center', bottom=btm))
	# accumulate the left-hand offsets
		btm += d

	# go through all of the bar segments and annotate
	for j in xrange(len(patch_handles)):
		for i, patch in enumerate(patch_handles[j].get_children()):
			bl = patch.get_xy()
			x = 0.5*patch.get_width() + bl[0]
			y = 0.5*patch.get_height() + bl[1]
#			if patch.get_width()>10:
#				px.text(x,y, "%f%%" % (percentages[i,j]), ha='center')

#	a=px.get_xticks().tolist()
	px.set_xticks(x_pos)
	px.set_xticklabels(SNRlist)
	px.set_ylabel('Cumulative percentage of mismatched intermittency chunks')
	px.set_ylim([0,100])	
	px.plot(x_pos, is_correct_perc,  '--', linewidth=6)

	f.savefig(output_file)

