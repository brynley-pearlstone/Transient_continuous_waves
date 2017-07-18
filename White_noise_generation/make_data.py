#!/usr/bin/env python

import os
from argparse import ArgumentParser


parser = ArgumentParser()

parser.add_argument("-J", "--Job_number", dest = "number",
                  help = "Job number used to label instances", metavar = "STR")
parser.add_argument("-C", "--n_chunks", dest = "n_chunks",
                  help = "Number of chunks to generate", metavar = "INT")
parser.add_argument("-t", "--start_time", dest = "start_time",
                  help = "Start time for fake data", metavar = "INT")
parser.add_argument("-l", "--signal_length", dest = "signal_length",
                  help = "Length of signal to generate", metavar = "INT")
parser.add_argument("-s", "--scale_SNR", dest = "scale_SNR",
                  help = "Desired signal SNR", metavar = "FLOAT")
parser.add_argument("-E", "--execdir", dest = "execdir",
                  help = "Directory of executable files", metavar = "STRING")
parser.add_argument("-R", "--rundir", dest = "rundir",
                  help = "Directory where output are to be placed", metavar = "STRING")


args = parser.parse_args()

numbers = str(args.number)

n_chunks = int(args.n_chunks)

start_time = str(args.start_time)
signal_length = str(args.signal_length)
scale_SNR = str(args.scale_SNR)
execdir = str(args.execdir)
rundir = str(args.rundir)
if execdir[-1]!= '/':
	execdir = execdir + '/'
if rundir[-1]!= '/':
        rundir = rundir + '/'





retval = os.getcwd()

os.system('mkdir -p ' + rundir + 'PULSAR' + str(numbers))
#os.chdir(retval + '/PULSAR' + str(numbers)+ '/')
#generate pars

os.system('python ' + execdir + 'make_pars.py --directory ' + rundir + 'PULSAR' + str(numbers) + ' --Number ' + str(numbers))
#generate priors

os.chdir(rundir + 'PULSAR' + str(numbers))
os.system('python ' + execdir + 'generate_binary.py --n_chunks ' + str(n_chunks)) #Give oputrput option
#generate binary
os.system('mkdir -p ' + rundir + 'PULSAR' + str(numbers) + '/junk')
#generate chunks of data
os.system('python ' + execdir + 'create_fake_data.py --start_time ' + start_time + ' --signal_length ' + signal_length + ' --binary_number input_binary.txt --par_file  ' + rundir + 'PULSAR' + str(numbers) + '/JPULSAR' + numbers + '.par --scale_SNR ' + scale_SNR + ' --output ' + rundir + 'PULSAR' + str(numbers) + '/junk/')

os.system('mkdir -p ' + rundir + 'PULSAR' + str(numbers) + '/H1/')
os.system('mkdir -p ' + rundir + 'PULSAR' + str(numbers) + '/L1/')
os.system('rm *_signal_only')
os.system('mv *H1_2.0 ' + rundir + 'PULSAR' + str(numbers) + '/H1')
os.system('mv *L1_2.0 ' + rundir + 'PULSAR' + str(numbers) + '/L1')

#stitch data together
os.system('python ' + execdir + 'time_stitcher.py -i ' + rundir + 'PULSAR' + str(numbers) + '/H1/ -d H1 -n ' + str(n_chunks))
os.system('python ' + execdir + 'time_stitcher.py -i ' + rundir + 'PULSAR' + str(numbers) + '/L1/ -d L1 -n ' + str(n_chunks))

#Clean up
os.system('mv ' + rundir + 'PULSAR' + str(numbers) + '/H1/fine* ' + rundir + 'PULSAR' + str(numbers) + '/')
os.system('mv ' + rundir + 'PULSAR' + str(numbers) + '/L1/fine* ' + rundir + 'PULSAR' + str(numbers) + '/')

os.system('rm -r ' + rundir + 'PULSAR' + str(numbers) + '/junk/')
os.system('rm -r ' + rundir + 'PULSAR' + str(numbers) + '/H1/')
os.system('rm -r ' + rundir + 'PULSAR' + str(numbers) + '/L1/')

os.system('python ' + execdir + 'plot_signal.py -d /scratch/spxbp1/TEST_SUITE/PULSAR' + str(numbers) + '/ -l /scratch/spxbp1/TEST_SUITE/PULSAR' + str(numbers) + '/fine_H*')
os.system('python ' + execdir + 'plot_signal.py -d ' + rundir + 'PULSAR' + str(numbers) + '/ -l ' + rundir + 'PULSAR' + str(numbers) + '/fine_L*')

