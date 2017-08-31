from lalapps.pulsarpputils import pulsar_nest_to_posterior
import numpy as np
import os

from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument("-N", "--n_chunks", dest = "n_chunks",
                   help = "Number of chunks that were split into", metavar = "INT")

parser.add_argument("-d", "--outdir", dest = "outdir",
                   help = "Base directory before all of the SNR dirs get split", metavar = "STRING")

#parser.add_argument("-l", "--dict_list", dest = "dict_list",
#                   help = "List of paths from basedir each library", metavar = "LIST")

args = parser.parse_args()

for i in range(int(args.n_chunks)-1):
	for j in range(int(args.n_chunks)):
		if j>i:
			os.system('lalapps_nest2pos -p ' + args.outdir + str(i) + '_' + str(j) + '_pos_samples.hdf ' + args.outdir + 'chunk_' + str(i) + '_to_' + str(j) + '.hdf') 
			with open(args.outdir + 'pos.txt', 'a') as f: 
				pos, logZs, logZn = pulsar_nest_to_posterior(args.outdir + str(i) + '_' + str(j) + '_pos_samples.hdf')
				chunk_mean_h = np.mean(pos['H0'].samples)
			#	f.seek[-1]
				f.write('chunk ' + str(i) + ' to ' + str(j) + ' mean of h0 samples = ' + str(chunk_mean_h) + '.\n')
