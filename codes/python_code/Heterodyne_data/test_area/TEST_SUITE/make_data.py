#!/usr/bin/env python

import os
from argparse import ArgumentParser


parser = ArgumentParser()

parser.add_argument("-J", "--Job_number", dest = "number",
                  help = "Job number used to label instances", metavar = "INT")
parser.add_argument("-C", "--n_chunks", dest = "n_chunks",
                  help = "Number of chunks to generate", metavar = "INT")
parser.add_argument("-t", "--start_time", dest = "start_time",
                  help = "Start time for fake data", metavar = "INT")
parser.add_argument("-l", "--signal_length", dest = "signal_length",
                  help = "Length of signal to generate", metavar = "INT")
parser.add_argument("-s", "--scale_SNR", dest = "scale_SNR",
                  help = "Desired signal SNR", metavar = "FLOAT")


args = parser.parse_args()

numbers = str(args.number)

n_chunks = int(args.n_chunks)

start_time = str(args.start_time)
signal_length = str(args.signal_length)
scale_SNR = str(args.scale_SNR)

retval = os.getcwd()

os.system('mkdir -p PULSAR' + str(numbers))
#os.chdir(retval + '/PULSAR' + str(numbers)+ '/')
#generate pars

os.system('python make_pars.py --directory PULSAR' + str(numbers) + ' --Number ' + str(numbers))
#generate priors

os.chdir(retval + '/PULSAR' + str(numbers))
os.system('python ../generate_binary.py --n_chunks ' + str(n_chunks))
#generate binary
os.system('mkdir -p junk')
#generate chunks of data
os.system('python ../create_fake_data.py --start_time ' + start_time + ' --signal_length ' + signal_length + ' --binary_number input_binary.txt --par_file  ' + retval + '/PULSAR' + str(numbers) + '/JPULSAR' + numbers + '.par --scale_SNR ' + scale_SNR + ' --output junk/')

os.system('mkdir -p H1/')
os.system('mkdir -p L1/')
os.system('rm *_signal_only')
os.system('mv *H1_2.0 H1')
os.system('mv *L1_2.0 L1')

#stitch data together
os.system('python ../time_stitcher -i H1/ -d H1')
os.system('python ../time_stitcher -i L1/ -d L1')

#Clean up
os.system('mv H1/fine* .')
os.system('mv L1/fine* .')

os.system('rm -r junk/')
os.system('rm -r H1/')
os.system('rm -r L1/')

