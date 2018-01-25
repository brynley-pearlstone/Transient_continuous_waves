import os
import numpy as np
from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument("-i", "--input_dir", dest = "input_dir",
                  help = "Directory containing the indivifual time atoms", metavar = "STRING")
parser.add_argument("-n", "--n_chunks", dest = "n_chunks",
                  help = "Number of  chunks to split the data into", metavar = "INT")
parser.add_argument("-o", "--outdir", dest = "outdir",
                  help = "Outfile directory", metavar = "STRING")
parser.add_argument("-d", "--detectors", dest = "detectors",
                  help = "String of detector names eg ['H1','L1','V1']", metavar = "STRING")

   
args = parser.parse_args()      

n_chunks = int(args.n_chunks)

input_dir = str(args.input_dir)
outdir = str(args.outdir)
f not os.path.exists(outdir + detectors[0] + '/'):

detectors = args.detectors

if not os.path.exists(input_dir + detectors[0] + '/'):
	print('Error, data atoms not where expected')
	quit(0)

#n_binaries = 2**(n_chunks)
numlist = np.linspace(0, (2**n_chunks)-1, num=2**n_chunks)
bin_list = []

# for binary in range(n_binaries)
for itt in range(len(numlist)):
        number = bin(int(numlist[int(itt)]))
        x = []
        for item in number[2:]:
                x.append(int(item))
        while len(x)<len(all_data[0]):
                x = [0] + x
        bin_list.append(x)


for binary in bin_list:
	on_list = []
	off_list = []
	for posn in len(binary):
		if binary[posn] == 1:
			on_list.append(posn)
		elif binary[posn] == 0:
			off_list.append(posn)
		else:
			print('Something went wrong, aborting.')
			quit(0)
	# Sanity check
	if (len(on_list) + len(off_list)) != len(binary:
		print('Something has gone wrong! Aborting')
		quit(0)
	for det in detectors:
		for place,chunk in enumerate(on_list):
			with open(input_dir + str(det) + '-chunk_' + str(chunk) + '_to_' str(chunk + 1) + '.txt','r') as f:
				lines = f.readlines()
				with open(args.outdir + str(det) + '/' +  str(binary) + '_on.txt','w+') as o:
					for line in lines:
						o.write(line)
                for place,chunk in enumerate(off_list):
                        with open(input_dir + str(det) + '-chunk_' + str(chunk) + '_to_' str(chunk + 1) + '.txt','r') as f:
                                lines = f.readlines()
                                with open(args.outdir + str(det) + '/' + str(binary) + '_off.txt','w+') as o:
                                        for line in lines:
                                                o.write(line)


