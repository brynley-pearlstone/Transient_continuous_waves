# Program to split a given time series into chunks.
# The code will read in a large stretch of data, and a cmdln arg
# for number of chunks n, and it should output, and it should output
# 2^n - 1 time series of continuous chunks

import os
from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument("-f", "--file", dest = "filename",
                  help = "Location of data file to unpack", metavar = "STRING")
parser.add_argument("-n", "--n_chunks", dest = "n_chunks",
		  help = "Number of  chunks to split the data into", metavar = "INT")
parser.add_argument("-o", "--outfile", dest = "outfile",
                  help = "Outfile directory", metavar = "STRING")
parser.add_argument("-d", "--detector", dest = "detector",
                  help = "Detector Name eg H1, L1, V1", metavar = "STRING")

args = parser.parse_args()

n_chunks = int(args.n_chunks)

filename = str(args.filename)
if not os.path.exists(filename):
        print('Please double check input file')

detector_name = str(args.detector)

outfile = str(args.outfile)
if outfile[-1] != '/':
	outfile = outfile + '/'
if not os.path.exists(outfile):
        os.makedirs(outfile)
elif not os.path.exists(outfile + detector_name + '/'):
	os.makedirs(outfile + detector_name + '/')

lines = []
#f = open(filename, 'r')
with open(filename, 'r') as f:
	for line in f:
		lines.append(line[:-1])
	splitline = [line.split() for line in lines]

time_length = float(splitline[-1][0]) - float(splitline[0][0])
chunk_time = []
for i in range(n_chunks):
	chunk_time.append(float(splitline[0][0]) + float(i * (time_length / n_chunks)))
chunk_time.append(float(splitline[-1][0]))
print(chunk_time)

for i in range(len(chunk_time)):
	new_time = chunk_time[i] - 0.5
	chunk_time[i] = new_time	

chunk_time[-1] += 1
 
for j in range(n_chunks):
	for k in range(len(chunk_time)):
		if k>j:
			with open(outfile + detector_name + '/' + detector_name + '-chunk_' + str(j) + '_to_' + str(k) + '.txt', 'w+') as output_file:
				output_file.seek(0)
				for l in splitline:
					if float(l[0]) >= chunk_time[j] and float(l[0]) <= chunk_time[k]:
						output_file.write(str(l[0]) + '\t' + str(l[1]) + '\t' + str(l[2]) +  ' \n')
