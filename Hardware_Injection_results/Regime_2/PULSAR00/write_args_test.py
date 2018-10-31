import os
from argparse import ArgumentParser
parser = ArgumentParser()

parser.add_argument("-D", "--Analysis_directory", dest="Directory",
		  help = "Directory in which analysis takes place", metavar = "STRING")
parser.add_argument("-p", "--prior_path", dest = "prior_path",
                  help = "Path to pulsar prior file", metavar = "INT")
parser.add_argument('-P', '--par_path', dest = 'par_path',
                  help = 'Path to pulsar par file', metavar = 'STR')
parser.add_argument('-n', '--n_chunks', dest = 'n_chunks',
                  help = 'Number of cunks used in this analysis', metavar = 'INT')
parser.add_argument('-l', '--nlive', dest = 'nlive',
                  help = 'Number of live points to use for the nested sampler', metavar = 'STR')
parser.add_argument('-d', '--dets', dest = 'dets',
                  help = 'List of detectors to analyse', metavar = 'STR')


args = parser.parse_args()
directory = str(args.Directory)
prior_path = str(args.prior_path)
par_path = str(args.par_path)
n_chunks = int(args.n_chunks)
dets = args.dets
# Sanity check
if not directory[-1]=='/':
	directory = directory + '/'

if not os.path.exists(directory):
	print('Analysis directory does not exist. \nPlease reconsider the choices that bought you here.\n')
	quit(0)
# Test the number of chunked time files for each detector

#if not os.path.exists(directory+ 'output/'):
#        os.makedirs(directory + 'output/')

outfile = directory + 'lalapps_args.txt'
detname = []
detfiles = []
for i in range(len(dets)):
	if i==0:
		detname.append(str(dets[i]))
		for j in range(n_chunks):
		        for k in range(n_chunks + 1):
		                if k>j:
					detfiles.append(directory + dets[i] + '/' + dets[i] + '-chunk_' + str(j) + '_to_' + str(k) + '.txt')	 
	else:
                detname.append(',' + str(dets[i]))
                for j in range(n_chunks):
                        for k in range(n_chunks + 1):
                                if k>j:
			                detfiles.append(',' + directory + dets[i] + '/' + dets[i] + '-chunk_' + str(j)+'_to_' + str(k) + '.txt')
		



#for j in range(n_chunks):
#        for k in range(n_chunks + 1):
#                if k>j:
#for index in range(len(detfiles):
#	args_to_write = '--detectors ' + [str(det) for det in detname] + ' --oldChunks --par-file ' + par_path + ' --input-files ' + [detfile[index] for detfile in detfile_list] + ' --outfile ' + directory + 'chunk_' + str(i) +'_to_' + str(j) + '.hdf --Nlive ' + str(args.nlive) + ' --Nmcmcinitial 0 --tolerance 0.1 --prior-file ' + prior_path + '\n'
#	print(args_to_write)
#        outtext.write(args_to_write)

outtext = open(outfile, 'w+')

outtext.seek(0)

for index in range(len(detfiles):
        args_to_write = '--detectors ' + [str(det) for det in detname] + ' --oldChunks --par-file ' + par_path + ' --input-files ' + [detfile[index] for detfile in detfile_list] + ' --outfile ' + directory + 'chunk_' + str(i) +'_to_' + str(j) + '.hdf --Nlive ' + str(args.nlive) + ' --Nmcmcinitial 0 --tolerance 0.1 --prior-file ' + prior_path + '\n'
        print(args_to_write)
        outtext.write(args_to_write)

#for i in range(n_chunks):
#        for j in range(n_chunks + 1):
#                if j>i:
#                        args_to_write = '--detectors H1,L1 --oldChunks --par-file ' + par_path + ' --input-files ' + directory + 'H1/H1-chunk_' + str(i) +'_to_' + str(j) + '.txt,' + directory + 'L1/L1-chunk_' + str(i) +'_to_' + str(j) + '.txt --outfile ' + directory + 'chunk_' + str(i) +'_to_' + str(j) + '.hdf --Nlive ' + str(args.nlive) + ' --Nmcmcinitial 0 --tolerance 0.1 --prior-file ' + prior_path + '\n'
#                        print(args_to_write)
#                        outtext.write(args_to_write)


#                        args_to_write = '--detectors H1,L1 --oldChunks --par-file ' + par_path + ' --input-files ' + directory + 'H1/H1-chunk_' + str(i) +'_to_' + str(j) + '.txt,' + directory + 'L1/L1-chunk_' + str(i) +'_to_' + str(j) + '.txt --outfile ' + directory + 'chunk_' + str(i) +'_to_' + str(j) + '.hdf --Nlive ' + str(args.nlive) + ' --Nmcmcinitial 0 --tolerance 0.1 --prior-file ' + prior_path + '\n'

#for H1item in os.listdir(H1dir):
#        H1_chunks.append(HL1item)
#for L1item in os.listdir(L1dir):
#        L1_chunks.append(L1item)

#if len(L1_chunks) != len(H1_chunks):
#	print('Something has gone wrong with the chunking process. Please review.\n')
#	quit(0)

#if len(L1_chunks) != len(H1_chunks):
#	print('Number of chunk files in each detector not equal! Please address')
#if not os.path.exists('output/'):
#	os.makedirs('output/')

#outfile = directory + 'lalapps_args.txt'
#outtext = open(outfile, 'w+')

#outtext.seek(0)
 
#for i in range(n_chunks):
#	for j in range(n_chunks + 1):
#		if j>i:
#			args_to_write = '--detectors H1,L1 --oldChunks --par-file ' + par_path + ' --input-files ' + directory + 'H1/H1-chunk_' + str(i) +'_to_' + str(j) + '.txt,' + directory + 'L1/L1-chunk_' + str(i) +'_to_' + str(j) + '.txt --outfile ' + directory + 'chunk_' + str(i) +'_to_' + str(j) + '.hdf --Nlive ' + str(args.nlive) + ' --Nmcmcinitial 0 --tolerance 0.1 --prior-file ' + prior_path + '\n'
#		        print(args_to_write)
#			outtext.write(args_to_write)
# THIS is the part that wants to be paralellised.  Pull it out of the loop, find a way to parse the arguments
#for item in range(len(H1_chunks)):
#	args_to_write = '--detectors H1,L1 --par-file ' + par_path + ' --input-files ' + directory + 'H1/' + (H1_chunks[item]) + ',' + directory + 'L1/' + (L1_chunks[item]) + ' --outfile ' + directory + (H1_chunks[item][27:-3]) + 'hdf --Nlive 1024 --Nmcmcinitial 0 --tolerance 0.1 --prior-file ' + prior_path + '\n' 
#	print(args_to_write)
#	outtext.write  ('--detectors H1,L1 --par-file
