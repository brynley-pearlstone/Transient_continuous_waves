#!/usr/bin/env python

from __future__ import division

# arguments - 
# start time
# Signal length
# par file
# scale SNR
# 
import os

from argparse import ArgumentParser
parser = ArgumentParser()

parser.add_argument("-t", "--start_time", dest = "start_time",
                  help = "Start time (GPS)", metavar = "INT")
parser.add_argument('-l', '--signal_length', dest = 'signal_length',
                  help = 'Duration of the signal (seconds)', metavar = 'INT')
parser.add_argument('-s', '--random_seed', dest = 'random_seed',
                  help = 'Random seed used to generate noise', default = 0, metavar = 'FLOAT')
parser.add_argument('-b', '--binary_number', dest = 'binary_number_file',
                  help = 'Path to location of binary configuration for realisation', metavar = 'STRING')
parser.add_argument('-p', '--par_file', dest = 'par_file',
                  help = 'Path to .par file for this simulation)', metavar = 'STRING')
parser.add_argument('-S', '--scale_SNR', dest = 'scale_SNR',
                  help = 'SNR that the signal will have when on', metavar = 'FLOAT')
parser.add_argument('-o', '--output', dest = 'output_path',
                  help = 'Path to destination for fake data', metavar = 'STRING')


args = parser.parse_args()

start_time = int(args.start_time)
signal_length = int(args.signal_length)
par_file = str(args.par_file)
scale_SNR = float(args.scale_SNR)
output_path = str(args.output_path)
random_seed = args.random_seed
binary_number_file = str(args.binary_number_file)

if output_path[-1] != '/':
	output_path = output_path + '/'

binary_file = open(binary_number_file, 'r')
binary_line = [line for line in binary_file]
binary_number = binary_line[1]
binary_number = binary_number.strip('\n')
binary_file.close()

n_chunks = (len(binary_number))

end_time = start_time + signal_length

chunk_length = signal_length / n_chunks

# Define a small number to avoid division by zero
delta = 0.0001

chunk_start = []
chunk_end = []
chunk_SNR = []

for i in range(n_chunks):
	chunk_start.append(start_time + (i * chunk_length))
	chunk_end.append(start_time + ((i+1) * chunk_length))
#	chunk_SNR.append((scale_SNR * int(binary_number[i]))+ delta)
	if int(binary_number[i]) == 1:
		chunk_SNR.append(scale_SNR)
        if int(binary_number[i]) == 0:
                chunk_SNR.append(0)


create_fake_data = []
print(binary_number)
for chunk in range(n_chunks):
	print(binary_number[chunk])
	#do
	if binary_number[chunk] == '1':
		print('--inject-file ' + par_file + ' --inject-output chunk_' + str(chunk) + '.output --fake-data H1,L1 --scale-snr ' + str(chunk_SNR[chunk]) + ' --Nlive 1024 --par-file ' +  par_file + ' --outfile ' + output_path + 'chunk_' + str(chunk) + '_out.hdf --prior-file ' + par_file[:-3] + 'priors --fake-starts ' + str(chunk_start[chunk]) + ',' + str(chunk_start[chunk]) + ' --fake-lengths ' + str(chunk_length) +  ',' + str(chunk_length) + ' --Nmcmcinitial 0')
		create_fake_data.append('--inject-file ' + par_file + ' --inject-output chunk_' + str(chunk) + '.output --fake-data H1,L1 --scale-snr ' + str(chunk_SNR[chunk]) + ' --Nlive 1024 --par-file ' +  par_file + ' --outfile ' + output_path + 'chunk_' + str(chunk) + '_out.hdf --prior-file ' + par_file[:-3] + 'priors --fake-starts ' + str(chunk_start[chunk]) + ',' + str(chunk_start[chunk]) + ' --fake-lengths ' + str(chunk_length) +  ',' + str(chunk_length) + ' --Nmcmcinitial 0')
	elif binary_number[chunk] == '0':
		print('--inject-file ' + par_file[:-4] + '_null.par  --inject-output chunk_' + str(chunk) + '.output --fake-data H1,L1 --scale-snr ' + str(chunk_SNR[chunk]) + ' --Nlive 1024 --par-file ' +  par_file[:-4] + '_null.par --outfile ' + output_path + 'chunk_' + str(chunk) + '_out.hdf --prior-file ' + par_file[:-3] + 'priors --fake-starts ' + str(chunk_start[chunk]) + ',' + str(chunk_start[chunk]) + ' --fake-lengths ' + str(chunk_length) +  ',' + str(chunk_length) + ' --Nmcmcinitial 0')
		create_fake_data.append('--inject-file ' + par_file[:-4] + '_null.par  --inject-output chunk_' + str(chunk) + '.output --fake-data H1,L1 --scale-snr ' + str(chunk_SNR[chunk]) + ' --Nlive 1024 --par-file ' +  par_file[:-4] + '_null.par --outfile ' + output_path + 'chunk_' + str(chunk) + '_out.hdf --prior-file ' + par_file[:-3] + 'priors --fake-starts ' + str(chunk_start[chunk]) + ',' + str(chunk_start[chunk]) + ' --fake-lengths ' + str(chunk_length) +  ',' + str(chunk_length) + ' --Nmcmcinitial 0')

	with open(output_path + "lppen_args.txt", 'a') as f:
		f.write(create_fake_data[chunk] + '\n')
	os.system('lalapps_pulsar_parameter_estimation_nested ' + create_fake_data[chunk])




