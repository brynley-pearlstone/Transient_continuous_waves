import h5py
from argparse import ArgumentParser
import os

parser = ArgumentParser()

parser.add_argument("-i", "--Input_directory", dest = "directory",
                  help = "Location of .hdf5s file to unpack", metavar = "STRING")

args = parser.parse_args()

directory = str(args.directory)
#if not os.path.exists(filename):
#        os.makedirs(filename)
#        print('Please double check input file')

def read_hdf5(directory, item, suffix):
	f = h5py.File(directory + '/' + item, 'r')
        data = f['lalinference']['lalinference_nest']
        vari = []
        valu = []
        for i in data.attrs:
        	vari.append(i)
                valu.append(data.attrs[i])
	if suffix == 'hdf':
	        output = directory + '/' + item[:-3]
	elif suffix == 'h5':
		output = directory + '/' + item[:-2]
        if output[-1] != '.':
                outname = output + '.output.txt'
        else:
                outname = output + 'output.txt'
        out_file = open(outname, 'w+')
        out_file.seek(0)
        for i in range(len(vari)):
                out_file.write(str(vari[i]) + ' = ' + str(valu[i]) + '\n')
        out_file.close()

for item in os.listdir(directory):
	if item[-3:] == 'hdf':
		read_hdf5(directory, item, 'hdf')
	elif item[-2:] == 'h5':
		read_hdf5(directory, item, 'h5')

