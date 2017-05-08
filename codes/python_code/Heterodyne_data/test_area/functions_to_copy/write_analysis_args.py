import os
from argparse import ArgumentParser
parser = ArgumentParser()

parser.add_argument("-D", "--Analysis_directory", dest="Directory",
		  help = "Directory in which analysis takes place", metavar = "STRING"
parser.add_argument("-p", "--prior_path", dest = "prior_path",
                  help = "Path to pulsar prior file", metavar = "INT")
parser.add_argument('-P', '--par_path', dest = 'par_path',
                  help = 'Path to pulsar par file', metavar = 'STR')

args = parser.parse_args()
directory = str(args.Directory)
prior_path = str(args.prior_path)
par_path = str(args.par_path)

# Sanity check
if not directory[-1]=='/':
	directory = directory + '/'

if not os.path.exists(directory):
	print('Analysis directory does not exist. \nPlease reconsider the choices that bought you here.\n')
	quit(0)
# Test the number of chunked time files for each detector
H1_chunks = []
L1_chunks = []

H1dir = directory + 'H1/'
L1dir = directory + 'l1/'

for H1item in os.listdir(H1dir):
	H1_chunks.append(H1item)

for L1item in os.listdir(L1dir):
        L1_chunks.append(L1item)

if len(L1_chunks) != len(H1_chunks):
	print('Something has gone wrong with the chunking process. Please review.\n')
	quit(0)

if len(L1_chunks) != len(H1_chunks):
	print('Number of chunk files in each detector not equal! Please address')
if not os.path.exists('output/'):
	os.makedirs('output/')

outfile = directory + 'lalapps_args.txt'
outtext = open(outfile, 'w+')

outtext.seek(0)
 
# THIS is the part that wants to be paralellised.  Pull it out of the loop, find a way to parse the arguments
for item in range(len(H1_chunks)):
#	print(item[0:2])
	outtext.write('--detectors H1,L1 --par-file ' + par_path + ' --input-files H1/' + (H1_chunks[item]) + ',L1/' + (L1_chunks[item]) + ' --outfile output/' + (H1_chunks[item][29:-3]) + 'hdf --Nlive 1024 --Nmcmcinitial 0 --tolerance 0.1 --prior-file ' + prior_path + '\n' )



