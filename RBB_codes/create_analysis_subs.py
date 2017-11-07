#!/usr/bin/env python
  
"""
The main purpose of this script is to assess the distribution of evidence ratios and
upper limits produced by lalapps_pulsar_parameter_estimation_nested when running on the
Gaussian test likelihood. It will run with a uniform prior distribution bounded at 0,
with a variety of increasing maximum values, to see how the evidence calculation
performs. It can run with various proposal distributions.
  
This is all done by setting up a Condor DAG to run the required codes.
  
Copyright (C) 2017 Matthew Pitkin
"""
  
from __future__ import print_function
  
import os
import sys
import uuid
import argparse
  
parser = argparse.ArgumentParser( )
parser.add_argument("-r", "--rundir", dest="rundir", required=True, help="Set the run directory for outputs")
parser.add_argument("-p", "--exec-path", dest="execpath", required=True, help="Set the path to the required executables")
parser.add_argument("-N", "--N-sims", dest = "N_sims", default=100, type=int, help="Set the number of parallel trials to run")
parser.add_argument("-C", "--n_chunks", dest = "n_chunks", help = "Number of chunks to generate", metavar = "INT")
parser.add_argument("-a", "--analysis_code", dest="run_analysis", required=True, help="Set the RBB analysis run script location")
parser.add_argument("-s", "--SNR", dest="SNR", required=True, help="SNR of fake data chunks analysed")
parser.add_argument("-S", "--to-split", dest="to_split", help="Set to 0 if splitting and runnning LPPEN is not required. Default is 1", metavar="INT", default=0) 
parser.add_argument("-o", "--outdir", dest="outdir", help="Location for the outputs of each run to go", metavar="STR")


#  parse input options
opts = parser.parse_args()
   
#2 the base directory
basedir = opts.rundir
if not os.path.isdir(basedir):
	print("Error... base directory '%s' does not exist." % basedir, file=sys.stderr)
	sys.exit(1)
if basedir[-1]!='/':
	basedir = basedir + '/'  

outdir = opts.outdir
if not os.path.isdir(outdir):
        print("Output directory '%s' does not exist. Creating directory" % outdir, file=sys.stderr)
        os.system('mkdir -p ' + outdir)
if outdir[-1]!='/':
        outdir = outdir + '/'

  
# create log directory if it doesn't exist
logdir = os.path.join(basedir, 'log')
if not os.path.isdir(logdir):
	os.mkdir(logdir)
  
# setup sub file for extraction script
#if not os.path.isfile(opts.run_splitter) or not os.access(opts.run_splitter, os.X_OK):
#  print("Error... test run script '%s' does not exist, or is not executable." % opts.run_splitter, file=sys.stderr)
#  sys.exit(1)
  
# check executable path is a directory
if not os.path.isdir(opts.execpath):
	print("Error... path for run executables does not exist.", file=sys.stderr)
	sys.exit(1)
  
##################  
#subfile to execute data collating and RBB analysis

grandchildsubfile = os.path.join(basedir, 'run_grandchild_analysis.sub')
fp = open(grandchildsubfile, 'w')

grandchildsubtext = """universe = vanilla
executable =  %s
arguments = -r %sPULSAR$(Pulsar_number)/ -E %s -n %i -S %i -o %sPULSAR$(Pulsar_number)/
getenv = True 
log = %s
error = %s
output = %s
notification = never
accounting_group = aluk.dev.o1.cw.transient.development
queue 1
""" % (opts.run_analysis, basedir, opts.execpath, int(opts.n_chunks), int(opts.SNR), outdir, os.path.join(logdir, 'run-$(cluster).log'), os.path.join(logdir,'run-$(cluster).err'), os.path.join(logdir,'run-$(cluster).out'))
    
fp.write(grandchildsubtext)
fp.close()

###################  

# setup Condor sub file for runs

to_split = float(opts.to_split)
# Run lalapps_pulsar_parameter_estimation_nested on each of the little things
#!!!create child sub file to do the child analyses
if to_split!=0:
	childsubfile = os.path.join(basedir, 'run_child_analysis.sub')
	fp = open(childsubfile, 'w')
  
	childsubtext = """universe = vanilla
	executable = /software/physics/ligo/spack/000/linux-redhat6-x86_64/gcc-5.4.0/ldg/ndjed33/bin/lalapps_pulsar_parameter_estimation_nested 
	arguments = $(args)  
	getenv = True
	log = %s
	error = %s
	output = %s
	notification = never
	accounting_group = aluk.dev.o1.cw.transient.development
	queue 1
	""" % (os.path.join(logdir, 'run-$(cluster).log'), os.path.join(logdir,'run-$(cluster).err'), os.path.join(logdir,'run-$(cluster).out'))
	  
	fp.write(childsubtext)
	fp.close()

	dagfile = os.path.join(basedir, 'run_analysis.dag')
	fp = open(dagfile, 'w')
 
	# one loop for each realisation
	for i in range(opts.N_sims):
		# Run the data splitting routine
		parent_uippen = '%03d' %(i+1)

		# One for each of the files in 
		triangle_number = sum(range(int(opts.n_chunks)+1))
		argsfile = '%sPULSAR%s/output/lalapps_args.txt' % (basedir, parent_uippen)
		lines = [line.strip('\n') for line in open(argsfile)]
		# Lines for the RBB runs
                parent_uippen = '%03d' %(i+1)
                # Grandchild jobs to perform final analysis
                grandchild_uippen = '%03d_gc' %(i+1)
                # Write dag  line for the first sub file
                dagstr = 'JOB %s %s\nRETRY %s 0\nVARS %s Pulsar_number=\"%s\" \n\n' % (grandchild_uippen, grandchildsubfile, grandchild_uippen, grandchild_uippen, parent_uippen)
                fp.write(dagstr)

		
		for j in range(triangle_number):
			# Child ID job number = concattenated parent_ID + '_' + child id %03d
			child_uippen = '%03d_%03d' % (i+1,j+1)   
			# Read in args file, parse as 'args="contents"'
			args = lines[j]
			# Child ID job number = concattenated parent_ID + '_' + child id %03d
			dagchildstr = 'JOB %s %s\nRETRY %s 0\nVARS %s args=\"%s\" \n\n' % (child_uippen, childsubfile, child_uippen, child_uippen, args)
			fp.write(dagchildstr)
	
			dag_spawn_str = 'PARENT %03d_%03d CHILD %s_gc \n\n' % (i+1,j+1, parent_uippen)
			fp.write(dag_spawn_str)
 	fp.close()


# create dag for all the jobs
if to_split==0:
	dagfile2 = os.path.join(basedir, 'run_RBB.dag')
	fd = open(dagfile2, 'w') 
	
	# one loop for each realisation
	for i in range(opts.N_sims):
		# Run the data splitting routine
		parent_uippen = '%03d' %(i+1)
		# Grandchild jobs to perform final analysis
		grandchild_uippen = '%03d_gc' %(i+1)
		# Write dag  line for the first sub file
		dagstr = 'JOB %s %s\nRETRY %s 0\nVARS %s Pulsar_number=\"%s\" \n\n' % (grandchild_uippen, grandchildsubfile, grandchild_uippen, grandchild_uippen, parent_uippen)
		fd.write(dagstr)
  
	fd.close()
