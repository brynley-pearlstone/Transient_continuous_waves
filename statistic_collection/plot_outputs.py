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
	y_pos = np.arange(len(SNRlist)) 
	
	f, px = plt.subplots(1,1)
#	fig, px = plt.figure()
	colors =['w','y','r','m','b','c','g','k','gray']
	patch_handles = []
	left = np.zeros(len(SNRlist)) # left alignment of data starts at zero
	for i, d in enumerate(data):
		patch_handles.append(plt.barh(y_pos, d, color=colors[i%len(colors)], align='center', left=left))
	# accumulate the left-hand offsets
		left += d

	# go through all of the bar segments and annotate
	for j in xrange(len(patch_handles)):
		for i, patch in enumerate(patch_handles[j].get_children()):
			bl = patch.get_xy()
			x = 0.5*patch.get_width() + bl[0]
			y = 0.5*patch.get_height() + bl[1]
#			if patch.get_width()>10:
#				px.text(x,y, "%f%%" % (percentages[i,j]), ha='center')

#	a=px.get_xticks().tolist()
	px.set_yticks(y_pos)
	px.set_yticklabels(SNRlist)
	px.set_xlabel('Cumulative percentage of mismatched intermittency chunks')
	px.set_xlim([0,100])	
	px.plot(is_correct_perc, y_pos, '--', linewidth=6)

	f.savefig(output_file)

def h_stacked_bar(SNR_list, list_of_mismatches, list_of_percentages, is_correct_perc, output_file):
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
		print(btm)
		patch_handles.append(plt.bar(x_pos, d, color=colors[i%len(colors)], align='center', bottom=btm))
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
	px.set_xlabel('Chunk SNR')
	px.set_ylabel('Cumulative percentage of mismatched intermittency chunks')
	px.set_ylim([0,100])	
	px.plot(x_pos, is_correct_perc,  '--', linewidth=6)

	f.savefig(output_file)

#	import numpy as np
#	import matplotlib.pyplot as plt
#	# some labels for each row
#	SNRlist = []
#	for SNR in SNR_list:
#		SNRlist.append(str(SNR))
#	r = len(SNRlist)
#	# how many data points overall (average of 3 per person)
#	#n = r * 3
#	# which person does each segment belong to?
#	#rows = np.random.randint(0, r, (n,))
#
#	# how wide is the segment?
#	widths = np.random.randint(3,12, n,)
#
#	# what label to put on the segment
#	#labels = xrange(n)
#	colors ='roygbmk'
#	patch_handles = []
#	ax = plt.figure()
#	left = np.zeros(r,)
#	row_counts = np.zeros(r,)
#	for (r, w, l) in zip(rows, widths, labels):
#		print r, w, l
#		patch_handles.append(ax.barh(r, w, align='center', left=left[r],
#			color=colors[int(row_counts[r]) % len(colors)]))
#		left[r] += w
#		row_counts[r] += 1
#		# we know there is only one patch but could enumerate if expanded
#		patch = patch_handles[-1][0] 
#		bl = patch.get_xy()
#		x = 0.5*patch.get_width() + bl[0]
#		y = 0.5*patch.get_height() + bl[1]
##		ax.text(x, y, "%d%%" % (l), ha='center',va='center')
#	y_pos = np.arange(8)
#	ax.set_yticks(y_pos)
#	ax.set_yticklabels(people)
#	ax.set_xlabel('Distance')
#
#







