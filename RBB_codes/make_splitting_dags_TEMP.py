#!/usr/bin/env python

from __future__ import print_function


import os
import sys
import uuid
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--indir", dest="indir", required=True, help="Set the input directory")
parser.add_argument("-o", "--outdir", dest="outdir", required=True, help="Set the output directory")
parser.add_argument("-S", "--splitter-code", dest="run_splitter", required=True, help="Set the test run script location")
parser.add_argument("-p", "--exec-path", dest="execpath", required=True, help="Set the path to the required executables")
parser.add_argument("-N", "--N-sims", dest = "N_sims", default=100, type=int, help="Set the number of parallel trials to run")
parser.add_argument("-C", "--n_chunks", dest = "n_chunks", help = "Number of chunks to generate", metavar = "INT")
parser.add_argument("-l", "--nlive", dest = "nlive", help = "Number of live ponts for nested sampling", metavar = "INT")


# parse input options
opts = parser.parse_args()

# the base directory
inputdir = opts.indir
outputdir = opts.outdir
if not os.path.isdir(inputdir):
  print("Error... base directory '%s' does not exist." % inputdir, file=sys.stderr)
  sys.exit(1)

if not os.path.isdir(outputdir):
  print("Error... output directory '%s' does not exist." % outputdir, file=sys.stderr)
  os.system('mkdir ' + outputdir)
#  sys.exit(1)
if inputdir[-1]!='/':
        inputdir = inputdir + '/'
if outputdir[-1]!='/':
        outputdir = pitputdir + '/'

# create log directory if it doesn't exist
logdir = os.path.join(outputdir, 'log')
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
subfile = os.path.join(outputdir, 'run_splitter.sub')
fp = open(subfile, 'w')

subtext = """universe = vanilla
executable = %s 
arguments =   -n %s  -H  %sPULSAR$(Pulsar)/fine_H1* -L %sPULSAR$(Pulsar)/fine_L1* -o %sPULSAR$(Pulsar)/output -P %sPULSAR$(Pulsar)/JPULSAR$(Pulsar).par -p %sPULSAR$(Pulsar)/JPULSAR$(Pulsar).priors -E %s -D %sPULSAR$(Pulsar)/output/ -l %s
getenv = True
log = %s
error = %s
output = %s
notification = never
accounting_group = aluk.dev.o1.cw.transient.development
queue 1
""" % (opts.run_splitter, opts.n_chunks,  inputdir, inputdir, outputdir,  inputdir, inputdir, opts.execpath, outputdir, opts.nlive, os.path.join(logdir, 'run-$(cluster).log'), os.path.join(logdir,'run-$(cluster).err'), os.path.join(logdir,'run-$(cluster).out'))

fp.write(subtext)
fp.close()

dagfile = os.path.join(outputdir, 'run_splitting.dag')
fp = open(dagfile, 'w')

# one loop for each realisation
for i in range(opts.N_sims):
  # Run the data splitting routine
  uippen = '%03d' %(i+1)

  # Grandchild jobs to perform final analysis

  # Write dag  line for the first sub file
  dagstr = 'JOB %s %s\nRETRY %s 0\nVARS %s Pulsar=\"%s\" \n\n' % (uippen, subfile, uippen, uippen, uippen)
  fp.write(dagstr)

