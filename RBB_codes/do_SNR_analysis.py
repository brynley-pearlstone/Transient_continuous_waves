#!/usr/bin/env python

import os

from argparse import ArgumentParser
parser = ArgumentParser()

parser.add_argument("-r", "--rundir", dest = "rundir",
                   help = "Full location to perform analysis (incl. */Pulsar###/", metavar = "STRING")
parser.add_argument("-E", "--Execdir", dest = "execdir",
                   help = "Full path to .py files used to do analysis", metavar = "STRING")
parser.add_argument("-n", "--n_chunks", dest = "n_chunks",
                   help = "Number of chunks", metavar = "INT")

args = parser.parse_args()

n_chunks = int(args.n_chunks)
rundir = str(args.rundir)
execdir = str(args.execdir)

if execdir[-1]!='/':
	execdir = execdir + '/'

if rundir[-1]!='/':
	rundir = rundir + '/'

os.system('python ' + execdir + 'read_data.py -i ' + rundir + 'output/')

os.system('python ' + execdir + 'collate_data.py -n ' + str(n_chunks) + ' -d ' + rundir + 'output/ -o ' + rundir + 'data.txt')

#os.system('python ' + execdir + 'collate_evidences.py -n ' + str(n_chunks) + ' -d ' + rundir + 'output/ -o ' + rundir + 'data.txt')

os.system('python ' + execdir + 'RBB_from_SNR.py -i ' + rundir + 'data.txt -o ' + rundir)

#os.system('python ' + execdir + 'RBB_summing_evidence_test.py -i ' + rundir + 'data.txt -o ' + rundir)

#Step 4:
#Translate from HDF5 to txt
#       using read_all.py
#Step 5:
#Collate into blocks of chunks with correct values
#       using collate_data.py
#Step 6:
#Compute RBB
#       using RBB.py

