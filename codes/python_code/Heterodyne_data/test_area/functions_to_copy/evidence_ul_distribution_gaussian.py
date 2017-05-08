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
parser.add_argument("-c", "--run-code", dest="run", required=True, help="Set the test run script location")
parser.add_argument("-p", "--exec-path", dest="execpath", required=True, help="Set the path to the required executables")
parser.add_argument("-N", "-N-sims", dest = "N_sims", default=100, type=int, help="Set the number of parallel trials to run")
parser.add_argument("-J", "--Job_number", dest = "number", help = "Job number used to label instances", metavar = "INT")
parser.add_argument("-C", "--n_chunks", dest = "n_chunks", help = "Number of chunks to generate", metavar = "INT")
parser.add_argument("-t", "--start_time", dest = "start_time", help = "Start time for fake data", metavar = "INT")
parser.add_argument("-l", "--signal_length", dest = "signal_length", help = "Length of signal to generate", metavar = "INT")
parser.add_argument("-s", "--scale_SNR", dest = "scale_SNR", help = "Desired signal SNR", metavar = "FLOAT")


# parse input options
opts = parser.parse_args()

# the base directory
basedir = opts.rundir
if not os.path.isdir(basedir):
  print("Error... base directory '%s' does not exist." % basedir, file=sys.stderr)
  sys.exit(1)

# set the numbers of live points to run with
nlive = 1024

# create log directory if it doesn't exist
logdir = os.path.join(basedir, 'log')
if not os.path.isdir(logdir):
  os.mkdir(logdir)

# setup sub file for extraction script
if not os.path.isfile(opts.run) or not os.access(opts.run, os.X_OK):
  print("Error... test run script '%s' does not exist, or is not executable." % opts.run, file=sys.stderr)
  sys.exit(1)

# check executable path is a directory
if not os.path.isdir(opts.execpath):
  print("Error... path for run executables does not exist.", file=sys.stderr)
  sys.exit(1)

#Set up the condor sub file for for each of the many parallel runs
# setup Condor sub file for runs
subfile = os.path.join(basedir, 'runmake_data.sub')
fp = open(subfile, 'w')

#run the do_analysis code on each simulation
subfiletxt = """universe = vanilla
executable = %s
arguments = -J $(JOB) -C %d -t 900000000 -l %d -s %d
getenv = True
log = %s
error = %s
output = %s
notification = never
accounting_group = aluk.dev.o1.cw.transient.development
queue 1
""" % (opts.run, int(opts.n_chunks), int(opts.signal_length), int(opts.scale_SNR), os.path.join(logdir, 'run-$(cluster).log'), os.path.join(logdir,'run-$(cluster).err'), os.path.join(logdir,'run-$(cluster).out'))
fp.write(subfiletxt)
fp.close()


# Run lalapps_pulsar_parameter_estimation_nested on each of the little things
#!!!create child sub file to do the child analyses
childsubfile = os.path.join(basedir, 'run_child_analysis.sub')
fp = open(childsubfile, 'w')

childsubtext = """universe = vanilla
executable = lalapps_pulsar_parameter_estimation_nested 
arguments = --detectors H1,L1 --par-file --Nlive 1024 --Nmcmcinitial 0 --tolerance 0.1 # --par-file  --input-files --outfile  --prior-file 
getenv = True
log = %s
error = %s
output = %s
notification = never
accounting_group = aluk.dev.o1.cw.transient.development
queue 1
""" % (opts.run, int(opts.n_chunks), int(opts.signal_length), int(opts.scale_SNR), os.path.join(logdir, 'run-$(cluster).log'), os.path.join(logdir,'run-$(cluster).err'), os.path.join(logdir,'run-$(cluster).out'))

fp.write(childsubtxt)
fp.close()


# create dag for all the jobs
dagfile = os.path.join(basedir, 'run.dag')
fp = open(dagfile, 'w')

#one loop for each realisation
for i in range(opts.N_sims):#, maxv in enumerate(maxvals):
 # create output directory
#  maxvdir = os.path.join(basedir, '%03d' % i)
#  if not os.path.isdir(maxvdir):
#    os.mkdir(maxvdir)

#  # create prior file
#  priorfile = os.path.join(maxvdir, 'prior.txt')
#  fpm = open(priorfile, 'w')
#  fpm.write('H0 uniform 0.0 %.4e\n' % maxv)
#  fpm.close()
# Write dag file for the first sub file
  dagstr = 'JOB %s %s\nRETRY %s 0\nVARS %s macrooutfile=\"%s\" \n' % (uippen, subfile, uippen, uippen, outfilenest)
  fp.write(dagstr)
  # one loop for each signal segment
  # loop over number of iterations
# One for each of the files in 
triangle_number = sum(range(int(opts.N_chunks)+1))

  for j in range(triangle_number):
    # unique ID
    uippen = '%03d_%03d' % (i,j) #uuid.uuid4().hex
    confdir = os.path.join(basedir, '%03d_%03d' % (i,j))
    
    # create output nested file
    outfilenest = os.path.join(confdir, 'nest_%03d_%03d.hdf' % (i,j))
  
    # write out ppen job
    # Child ID job number = concattenated parent_ID + '_' + child id %03d
    dagchildstr = 'JOB %s %s\nRETRY %s 0\nVARS %s macrooutfile=\"%s\" \n' % (uippen, childsubfile, uippen, uippen, outfilenest)
    fp.write(dagstr)
  
    #!!! write out child jobs
   
fp.close()
