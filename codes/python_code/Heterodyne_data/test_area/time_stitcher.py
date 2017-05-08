import os
from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument("-i", "--directory", dest = "directory",
                  help = "Location of data files to stitch", metavar = "STRING")
#parser.add_argument("-n", "--n_chunks", dest = "n_chunks",
#                  help = "Number of  chunks to split the data into", metavar = "INT")
#parser.add_argument("-o", "--outfile", dest = "outfile",
#                  help = "Outfile directory", metavar = "STRING")
parser.add_argument("-d", "--detector", dest = "detector",
                  help = "Detector Name eg H1, L1, V1", metavar = "STRING")




args = parser.parse_args()

#n_chunks = int(args.n_chunks)

directory = str(args.directory)
if not os.path.exists(directory):
        print('Please double check input file')

files = os.listdir(directory)
detector_name = str(args.detector)

#outfile = str(args.outfile)
#if outfile[-1] != '/':
#        outfile = outfile + '/'
#if not os.path.exists(outfile):
#        os.makedirs(outfile)
#        os.makedirs(outfile + 'H1/')
#        os.makedirs(outfile + 'L1/')
#elif not os.path.exists(outfile + detector_name + '/'):
#        os.makedirs(outfile + detector_name + '/')

all_lines = []
for item in files:
	lines = []
	f = open(directory + item, 'r')
	for line in f:
        	lines.append(line[:-1])
		all_lines.append(line[:-1])
#	all_lines.append(lines)
	f.close()
print(all_lines)	
table_headers = lines[0:14]
#lines[0:14]= []
splitline = [line.split('\t') for line in all_lines]
print(splitline)
start_time = float(splitline[0][0])
end_time = float(splitline[-1][0])

print(splitline)
print(start_time)
print(end_time)

outfile = 'fine_' + detector_name + '-' + str(start_time) + '-' + str(end_time) + '.txt'
output = open(outfile, 'w+')
for line in splitline:
	for entry in line:
		output.write(entry + '\t')
	output.write('\n')
output.close()

