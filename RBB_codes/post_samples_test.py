from lalapps.pulsarpputils import pulsar_nest_to_posterior
import numpy as np
import os

from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument("-N", "--n_chunks", dest = "n_chunks",
                   help = "Number of chunks that were split into", metavar = "INT")

parser.add_argument("-d", "--outdir", dest = "outdir",
                   help = "Output directory for a given pulsar", metavar = "STRING")

#parser.add_argument("-l", "--dict_list", dest = "dict_list",
#                   help = "List of paths from basedir each library", metavar = "LIST")

args = parser.parse_args()

if args.outdir[-1]!='/':
	args.outdir = args.outdir + '/'

if not os.path.isdir(str(args.outdir) + 'posteriors/'):
	os.mkdir(str(args.outdir) + 'posteriors/')


for i in range(int(args.n_chunks)):
	for j in range(int(args.n_chunks)+1):
		if j>i:
			os.system('lalapps_nest2pos -p ' + args.outdir + str(i) + '_' + str(j) + '_pos_samples.hdf ' + args.outdir + 'chunk_' + str(i) + '_to_' + str(j) + '.hdf') 
			with open(args.outdir + 'posteriors/chunk_' + str(i) + '-' + str(j) + '_pos.txt', 'w') as f: 
				pos, logZs, logZn = pulsar_nest_to_posterior(args.outdir + str(i) + '_' + str(j) + '_pos_samples.hdf')
				chunk_mean_h = np.mean(pos['H0'].samples)
				chunk_stdev_h = np.std(pos['H0'].samples)
				f.write(str(chunk_mean_h) + '\n' + str(chunk_stdev_h) + '\n')
			
