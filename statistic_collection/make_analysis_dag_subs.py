#!/usr/bin/env python
  
#"""
#The main purpose of this script is to assess the distribution of evidence ratios and
#upper limits produced by lalapps_pulsar_parameter_estimation_nested when running on the
#Gaussian test likelihood. It will run with a uniform prior distribution bounded at 0,
#with a variety of increasing maximum values, to see how the evidence calculation
#performs. It can run with various proposal distributions.
#  
#This is all done by setting up a Condor DAG to run the required codes.
#  
#Copyright (C) 2017 Matthew Pitkin
#"""
  
from __future__ import print_function
 
import os
import sys
import uuid
import argparse
  
parser = argparse.ArgumentParser( )
parser.add_argument("-r", "--rundir", dest="rundir", required=True, help="Set the run directory for outputs")
#parser.add_argument("-S", "--splitter-code", dest="run_splitter", required=True, help="Set the test run script location")
parser.add_argument("-p", "--exec-path", dest="execpath", required=True, help="Set the path to the required executables")
parser.add_argument("-N", "--N-sims", dest = "N_sims", default=200, type=int, help="Set the number of parallel trials to run analysis on")
#parser.add_argument("-C", "--n_chunks", dest = "n_chunks", help = "Number of chunks to generate", metavar = "INT")
parser.add_argument("-a", "--analysis_code", dest="run_analysis", required=True, help="Set the path to the Meta analysis code")
parser.add_argument("-S", "--SNR_list", dest="SNR_list", required=True, help="List of SNR values to analyse")  
parser.add_argument("-V", "--averaging_code", dest="run_average", required=True, help="Path to the analysis-averaging code") 

# parse input options
opts = parser.parse_args()
  
# the base directory
basedir = opts.rundir
if not os.path.isdir(basedir):
  print("Error... base directory '%s' does not exist." % basedir, file=sys.stderr)
  sys.exit(1)
if basedir[-1]!='/':
	basedir = basedir + '/'  

# set the numbers of live points to run with
#nlive = 1024
  
# create log directory if it doesn't exist
logdir = os.path.join(basedir, 'log')
if not os.path.isdir(logdir):
  os.mkdir(logdir)
  
# setup sub file for extraction script
if not os.path.isfile(opts.run_analysis) or not os.access(opts.run_analysis, os.X_OK):
  print("Error... test run script '%s' does not exist, or is not executable." % opts.run_analysis, file=sys.stderr)
  sys.exit(1)
  
# check executable path is a directory
if not os.path.isdir(opts.execpath):
  print("Error... path for run executables does not exist.", file=sys.stderr)
  sys.exit(1)
  
# setup Condor sub file for runs

# Create child sub file to do the child analyses
subfile = os.path.join(basedir, 'run_stat_analysis.sub')
fp = open(subfile, 'w')

subtext = """universe = vanilla
executable = %s 
arguments = --true_binary %sSNR_$(SNRDIR)/PULSAR$(PULSAR_NUMBER)/input_binary.txt --sorted_binaries %sSNR_$(SNRDIR)/PULSAR$(PULSAR_NUMBER)/analysis_out/sorted_binaries.txt --output_dict %sSNR_$(SNRDIR)/PULSAR$(PULSAR_NUMBER)/analysis_out/output.txt --output %sSNR_$(SNRDIR)/SNR_trials_info_out.txt -n $(PULSAR_NUMBER) -S $(SNRDIR)
getenv = True
log = %s
error = %s
output = %s
notification = never
accounting_group = aluk.dev.o1.cw.transient.development
queue 1
""" % (opts.run_analysis, opts.rundir, opts.rundir, opts.rundir, opts.rundir,  os.path.join(logdir, 'run-$(cluster).log'), os.path.join(logdir,'run-$(cluster).err'), os.path.join(logdir,'run-$(cluster).out'))
  
fp.write(subtext)
fp.close()


# Write sub file for average all.py

childsubfile = os.path.join(basedir, 'run_stat_analysis_child.sub')
fc = open(childsubfile, 'w')

childsubtext = """universe = vanilla
executable = %s 
arguments = --SNR $(SNR) --input_path %sSNR_$(SNRDIR)/SNR_trials_info_out.txt --output_path %sanalysis_results.txt 
getenv = True
log = %s
error = %s
output = %s
notification = never
accounting_group = aluk.dev.o1.cw.transient.development
queue 1
""" % (opts.run_average, opts.rundir, opts.rundir, os.path.join(logdir, 'run-$(cluster).log'), os.path.join(logdir,'run-$(cluster).err'), os.path.join(logdir,'run-$(cluster).out'))


fc.write(childsubtext)
fc.close()


SNR_list = str(opts.SNR_list).strip('[')
SNR_list = SNR_list.strip(']')
SNRs = SNR_list.split(',')
print(SNRs)

# create dag for all the jobs
dagfile = os.path.join(basedir, 'run_stat_analysis.dag')
fp = open(dagfile, 'w')

#for SNR in SNR_list:
for SNR in SNRs:
  
  # change path to include SNR-dependancy
  # write dag string for all jobs for each SNR
# one loop for each realisation
  for i in range(opts.N_sims):
  # Run the data splitting routine
    uippen = '%03d_%03d' %(int(SNR),i+1)

    # Write dag line for the sub file
    dagstr = 'JOB %s %s\nRETRY %s 0\nVARS %s SNRDIR=\"%s\" PULSAR_NUMBER=\"%03d\" \n\n' % (uippen, subfile, uippen, uippen, SNR, i+1)
    fp.write(dagstr)
 
  # Average results for each SNR
  # Write DAG lines for average_results.py
  #c_Job = '%s%s' % (SNR, uippen) # Job number for child jobs
  #avedagstr = 'JOB %s %s\nRETRY %s 0\nVARS %s SNR=\"%s\" \n\n'% (c_Job, childsubfile, c_Job, c_Job, SNR)  #python average_results.py -S 30 -m /scratch/spxbp1/10_tests/mismatch.txt -p /scratch/spxbp1/10_tests/list_posn.txt -c /scratch/spxbp1/10_tests/is_correct.txt -o test_output.txt
  #fp.write(avedagstr)
  #for i in range(opts.N_sims):
    # Put in a check to make sure that the relevant files are there - and that the parent analysis would have worked correctly
    # check if str(opts.rundir) + 'SNR_' + str(SNR) + '/mismatch.txt exists
  #  if os.path.isfile(str(opts.rundir) + 'SNR_' + str(SNR) + '/mismatch.txt'):
  #    dag_spawn_str = 'PARENT %03d CHILD %s \n\n' % (i+1,c_Job)
  #    fp.write(dag_spawn_str)  
#  Next SNR
fp.close()

