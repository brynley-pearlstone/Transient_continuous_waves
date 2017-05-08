import h5py
from argparse import ArgumentParser
import os

parser = ArgumentParser()

parser.add_argument("-f", "--hdf5 file", dest = "filename",
                  help = "Location of .hdf5 file to unpack", metavar = "STRING")

args = parser.parse_args()

filename = str(args.filename)
if not os.path.exists(filename):
        os.makedirs(filename)
        print('Please double check input file')

f = h5py.File(filename, 'r')
data = f['lalinference']['lalinference_nest']
vari = []
valu = []
for i in data.attrs:
	vari.append(i)
	valu.append(data.attrs[i])
     
# Write vari and valu to file
output = filename[:-3]
if output[-1] != '.':
	outname = output + '.output.txt'
else:	
	outname = output + 'output.txt'

out_file = open(outname, 'w+')
out_file.seek(0)

for i in range(len(vari)):
	out_file.write(str(vari[i]) + ' = ' + str(valu[i]) + '\n')

out_file.close()
