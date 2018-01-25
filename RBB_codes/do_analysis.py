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
parser.add_argument("-S", "--SNR", dest = "snr",
                   help = "SNR of fake data analysed", metavar = "STR")
parser.add_argument("-o", "--outdir", dest = "outdir",
                   help = "Location for theoutput of each run", metavar = "STR")


args = parser.parse_args()

n_chunks = int(args.n_chunks)
rundir = str(args.rundir)
execdir = str(args.execdir)
outdir = str(args.outdir)

if execdir[-1]!='/':
	execdir = execdir + '/'

if rundir[-1]!='/':
	rundir = rundir + '/'

if outdir[-1]!='/':
        outdir = outdir + '/'

os.system('mkdir -p ' + outdir)

os.system('python ' + execdir + 'post_samples_test.py -N ' + str(n_chunks) + ' -d ' + rundir + 'output/')

os.system('python ' + execdir + 'read_data.py -i ' + rundir + 'output/')

os.system('python ' + execdir + 'collate_evidences.py -n ' + str(n_chunks) + ' -d ' + rundir + 'output/ -o ' + outdir + 'data.txt')

os.system('mkdir -p ' + outdir + 'simple_version')

os.system('python ' + execdir + 'simple_collate_data.py -n ' + str(n_chunks) + ' -d ' + rundir + 'output/ -o ' + outdir + '/simple_version/data.txt')

os.system('python ' + execdir + 'RBB_summing_evidence.py -i ' + outdir + 'data.txt -o ' + outdir + 'analysis_out' + ' -b ' + rundir + 'input_binary.txt')

os.system('python ' + execdir + 'RBB_summing_evidence_w_cutoff.py -i ' + outdir + 'data.txt -o ' + outdir + 'posterior_cut_out' + ' -b ' + rundir + 'input_binary.txt -p ' + outdir + 'h_posterior_data.txt')

os.system('python ' + execdir + 'RBB_summing_bayes_factor.py -i ' + outdir + 'bayes_factor_data.txt -o ' + outdir + 'bayes_factor_cut_out' + ' -b ' + rundir + 'input_binary.txt')

os.system('python ' + execdir + 'simple_RBB.py -i ' + outdir + 'simple_version/data.txt -o ' + outdir + 'simple_version' + ' -b ' + rundir + 'input_binary.txt')

outlist = outdir.split('/')
stats_out = ''
for item in outlist[:-1]:
	stats_out = stats_out + '/' + item

stats_out = stats_out + '/'

os.system('python ' + execdir + 'read_statistics.py -t ' + rundir + 'input_binary.txt -d ' + outdir + 'analysis_out/ -b ' + outdir + 'bayes_factor_cut_out/ -p ' + outdir + 'posterior_cut_out/ -s ' + outdir + 'simple_version/ -o ' + stats_out + 'Coherent_blocks_output_collated.txt -B ' + stats_out + 'Bayescut_coherent_blocks_collates_output.txt -P ' + stats_out + 'Posterior_cut_collated_outputs.txt -V ' + stats_out + 'Incoherent_blocks_output_collated.txt -n ' + rundir[-4:-1] + ' -S ' + str(args.snr))

#Step 4:
#Translate from HDF5 to txt
#       using read_all.py
#Step 5:
#Collate into blocks of chunks with correct values
#       using collate_data.py
#Step 6:
#Compute RBB
#       using RBB.py

