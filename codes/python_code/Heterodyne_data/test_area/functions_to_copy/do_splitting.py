#!/usr/bin/env python 

#make executable
import os
from argparse import ArgumentParser

#imports
parser = ArgumentParser()

#take vars
#full path to H1 input
#full path to L1 input
#n_chunks
#full path to output

parser.add_argument("-n", "--n_chunks", dest = "n_chunks",
                  help = "Number of chunks", metavar = "INT")
parser.add_argument("-H", "--H1_input", dest = "H1_input",
                  help = "Full path to H1 input file", metavar = "STRING")
parser.add_argument("-L", "--L1_input", dest = "L1_input",
                  help = "Full path to L1 input file", metavar = "STRING")
parser.add_argument("-o", "--output_path", dest = "output_path",
		  help = "Full path to output of split files", metavar = "STRING")
parser.add_argument("-P", "--Par_path", dest = "par_files",
                  help = "Full path to par files", metavar = "STRING")
parser.add_argument("-p", "--Prior_path", dest = "prior_files",
                  help = "Full path to prior files", metavar = "STRING")
parser.add_argument("-E", "--Execdir", dest = "execdir",
                   help = "Full path to .py files used to do analysis", metavar = "STRING")
parser.add_argument("-D", "--analysis_dir", dest = "analysis_dir",
                  help = "Full path to output of LPPEN files", metavar = "STRING")


args = parser.parse_args()

n_chunks = int(args.n_chunks)
H1_input = str(args.H1_input)
L1_input = str(args.L1_input)
output_path = str(args.output_path)
par_files = str(args.par_files)
prior_files = str(args.prior_files)
analysis_dir = str(args.analysis_dir)`
execdir = str(args.execdir)

os.system('python ' + execdir + 'timesplitter.py -f ' + H1_input + ' -n ' + str(n_chunks) + ' -o  ' + output_path + ' -d H1')
os.system('python ' + execdir + 'timesplitter.py -f ' + L1_input + ' -n ' + str(n_chunks) + ' -o  ' + output_path + ' -d L1')

os.system('python ' + execdir + 'write_analysis_args.py -P ' + par_files + ' -p  ' + prior_files + ' -D ' + analysis_dir)
