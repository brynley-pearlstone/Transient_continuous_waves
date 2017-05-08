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
parser.add_argument("-S", "--splitter-code", dest="run_splitter", required=True, help="Set the test run script location")
parser.add_argument("-p", "--exec-path", dest="execpath", required=True, help="Set the path to the required executables")
parser.add_argument("-N", "--N-sims", dest = "N_sims", default=100, type=int, help="Set the number of parallel trials to run")
#parser.add_argument("-J", "--Job_number", dest = "number", help = "Job number used to label instances", metavar = "INT")
parser.add_argument("-C", "--n_chunks", dest = "n_chunks", help = "Number of chunks to generate", metavar = "INT")
#parser.add_argument("-t", "--start_time", dest = "start_time", help = "Start time for fake data", metavar = "INT")
#parser.add_argument("-l", "--signal_length", dest = "signal_length", help = "Length of signal to generate", metavar = "INT")
#parser.add_argument("-s", "--scale_SNR", dest = "scale_SNR", help = "Desired signal SNR", metavar = "FLOAT")
parser.add_argument("-a", "--analysis_code", dest="run_analysis", required=True, help="Set the RBB analysis run script location")
  
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
if not os.path.isfile(opts.run_splitter) or not os.access(opts.run_splitter, os.X_OK):
  print("Error... test run script '%s' does not exist, or is not executable." % opts.run_splitter, file=sys.stderr)
  sys.exit(1)
  
# check executable path is a directory
if not os.path.isdir(opts.execpath):
  print("Error... path for run executables does not exist.", file=sys.stderr)
  sys.exit(1)
  
  
# setup Condor sub file for runs
subfile = os.path.join(basedir, 'runmake_data.sub')
fp = open(subfile, 'w')
  
#exec do_splitting.py
#run the do_analysis code on each simulation
subfiletxt = """universe = vanilla
executable = %s
arguments = -n %d -H %sPULSAR$(Pulsar_number)/$(H1_file) -L %sPULSAR$(Pulsar_number)/$(L1_file)  -o %s/PULSAR$(Pulsar_number)/output -P %sPULSAR$(Pulsar_number)/$(par_file) -p %sPULSAR$(Pulsar_number)/$(prior_file) -E %s -D /scratch/spxbp1/TEST_SUITE/PULSAR$(Pulsar_number)/
getenv = True
log = %s
error = %s
output = %s
notification = never
accounting_group = aluk.dev.o1.cw.transient.development
queue 1
""" % (opts.run_splitter, int(opts.n_chunks), basedir, basedir, basedir, basedir, basedir, str(opts.execpath), os.path.join(logdir, 'run-splitter-$(cluster).log'), os.path.join(logdir,'run-splitter-$(cluster).err'), os.path.join(logdir,'run-splitter-$(cluster).out'))
fp.write(subfiletxt)
fp.close()
  
######################  

# Run lalapps_pulsar_parameter_estimation_nested on each of the little things
#!!!create child sub file to do the child analyses
childsubfile = os.path.join(basedir, 'run_child_analysis.sub')
fp = open(childsubfile, 'w')
  
childsubtext = """universe = vanilla
executable = lalapps_pulsar_parameter_estimation_nested 
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

##################  
#subfile to execute data collating and RBB analysis

grandchildsubfile = os.path.join(basedir, 'run_child_analysis.sub')
fp = open(grandchildsubfile, 'w')
  
grandchildsubtext = """universe = vanilla
executable =  %s
arguments = -r %sPULSAR$(Pulsar_number)/ -E %s -n %i  
getenv = True
log = %s
error = %s
output = %s
notification = never
accounting_group = aluk.dev.o1.cw.transient.development
queue 1
""" % (opts.run_analysis, basedir, opts.execpath, int(opts.n_chunks), os.path.join(logdir, 'run-$(cluster).log'), os.path.join(logdir,'run-$(cluster).err'), os.path.join(logdir,'run-$(cluster).out'))
  
fp.write(grandchildsubtext)
fp.close()

# create dag for all the jobs
dagfile = os.path.join(basedir, 'run.dag')
fp = open(dagfile, 'w')
  
# one loop for each realisation
for i in range(opts.N_sims):
  parent_uippen = '%03d' %(i+1)
  # Write dag  line for the first sub file
#  dagstr = 'JOB %s %s\nRETRY %s 0\nVARS %s Pulsar_number = \"%s\" H1_files = \"H1/\" L1_files = \"L1/\" par_file = \"JPULSAR%s.par\" prior_file = \"JPULSAR%s.prior\" \n' % (parent_uippen, subfile, parent_uippen, parent_uippen, parent_uippen, parent_uippen, parent_uippen)
#  fp.write(dagstr)
  print('python ' + str(opts.execpath) + str(opts.run_splitter) + '-n ' + str(opts.n_chunks) + ' -H ' + basedir + 'PULSAR' + str(parent_uippen) + '/H1 -L ' + basedir + 'PULSAR' + str(parent_uippen) + '/L1 -o ' + basedir + '/PULSAR' + str(parent_uippen) + '/output -P ' + basedir + 'PULSAR' + str(parent_uippen) + '/JPULSAR' + str(parent_uippen) + '.par -p ' + basedir + 'PULSAR' + str(parent_uippen) + '/JPULSAR' + str(parent_uippen) + '.priors -E ' + str(opts.execpath) + ' -D ' + basedir + 'PULSAR' + str(parent_uippen) + '/') 

#  os.system('python ' + opts.execpath + opts.run_splitter + '-n %d -H %sPULSAR' + parent_uippen + '/H1 -L %sPULSAR' + parent_uippen + '/L1 -o %s/PULSAR' + parent_uippen + '/output -P %sPULSAR' + parent_uippen + '/JPULSAR' + parent_uippen + '.par -p %sPULSAR' + parent_uippen + '/JPULSAR' + parent_uippen + '.priors -E %s -D /scratch/spxbp1/TEST_SUITE/PULSAR' + parent_uippen + '/' % (opts.n_chunks, basedir, basedir, basedir, basedir, basedir, str(opts.execpath) ))

  # One for each of the files in 
  triangle_number = sum(range(int(opts.n_chunks)+1))
# Here, we have an issue. Argsfile doesn't exists until the dags have been submitted, so the args can't be read until after the first job has been submitted. I don't know if there is a work around for this.
# We could loop over this first stage and do it in series, as it is relatively quick.
# Need to re-write an awful lot of this though.
  argsfile = '%sPULSAR%s/lalapps_args.txt' % (basedir, parent_uippen)
  argslist = open(argsfile, 'r')
  for j in range(triangle_number):
    # Child ID job number = concattenated parent_ID + '_' + child id %03d
    child_uippen = '%03d_%03d' % (i+1,j+1)
     
    # Read in args file, parse as 'args="contents"'
    args = argslist[j]
    
    # Child ID job number = concattenated parent_ID + '_' + child id %03d
    dagchildstr = 'JOB %s %s\nRETRY %s 0\nVARS %s args=\"%s\" \n' % (child_uippen, childsubfile, child_uippen, child_uippen, args)
    fp.write(dagchildstr)
#    dag_relation_str = 'PARENT %s CHILD %s \n' % (parent_uippen, child_uippen)
#    fp.write(dag_relation_str)
    dag_spawn_str = 'PARENT %s CHILD %s_gc \n' % (child_uippen, parent_uippen)
    fp.write(dag_spawn_str)
    #!!! write out child jobs
   
  # Grandchild jobs to perform final analysis
  grandchild_uippen = '%03d_gc' %(i)
  # Write dag  line for the first sub file
  dagstr = 'JOB %s %s\nRETRY %s 0\nVARS %s \n' % (grandchild_uippen, grandchildsubfile, grandchild_uippen, grandchild_uippen)
  fp.write(dagstr)
 

fp.close()
