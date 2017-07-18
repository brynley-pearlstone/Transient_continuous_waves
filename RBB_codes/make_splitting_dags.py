#!/usr/bin/env python

from __future__ import print_function


import os
import sys
import uuid
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--rundir", dest="rundir", required=True, help="Set the run directory for outputs")
parser.add_argument("-S", "--splitter-code", dest="run_splitter", required=True, help="Set the test run script location")
parser.add_argument("-p", "--exec-path", dest="execpath", required=True, help="Set the path to the required executables")
parser.add_argument("-N", "--N-sims", dest = "N_sims", default=100, type=int, help="Set the number of parallel trials to run")
parser.add_argument("-C", "--n_chunks", dest = "n_chunks", help = "Number of chunks to generate", metavar = "INT")


# parse input options
opts = parser.parse_args()

# the base directory
basedir = opts.rundir
if not os.path.isdir(basedir):
  print("Error... base directory '%s' does not exist." % basedir, file=sys.stderr)
  sys.exit(1)
if basedir[-1]!='/':
        basedir = basedir + '/'

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


# Run lalapps_pulsar_parameter_estimation_nested on each of the little things
#!!!create child sub file to do the child analyses
subfile = os.path.join(basedir, 'run_splitter.sub')
fp = open(subfile, 'w')

subtext = """universe = vanilla
executable = %s 
arguments =   -n %s  -H  %sPULSAR$(Pulsar)/fine_H1* -L %sPULSAR$(Pulsar)/fine_L1* -o %sPULSAR$(Pulsar)/output -P %sPULSAR$(Pulsar)/JPULSAR$(Pulsar).par -p %sPULSAR$(Pulsar)/JPULSAR$(Pulsar).priors -E %s -D %sPULSAR$(Pulsar)/output/
getenv = True
log = %s
error = %s
output = %s
notification = never
accounting_group = aluk.dev.o1.cw.transient.development
queue 1
""" % (opts.run_splitter, opts.n_chunks,  basedir, basedir, basedir,  basedir, basedir, opts.execpath, basedir, os.path.join(logdir, 'run-$(cluster).log'), os.path.join(logdir,'run-$(cluster).err'), os.path.join(logdir,'run-$(cluster).out'))

fp.write(subtext)
fp.close()

dagfile = os.path.join(basedir, 'run_splitting.dag')
fp = open(dagfile, 'w')

# one loop for each realisation
for i in range(opts.N_sims):
  # Run the data splitting routine
  uippen = '%03d' %(i+1)

  # Grandchild jobs to perform final analysis

  # Write dag  line for the first sub file
  dagstr = 'JOB %s %s\nRETRY %s 0\nVARS %s Pulsar=\"%s\" \n\n' % (uippen, subfile, uippen, uippen, uippen)
  fp.write(dagstr)

