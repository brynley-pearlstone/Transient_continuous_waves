import os
from argparse import ArgumentParser
import random

parser = ArgumentParser()

parser.add_argument("-d", "--Input_directory", dest = "directory",
                  help = "Location of .hdf5s file to unpack", metavar = "STRING")
parser.add_argument("-n", "--Number", dest = "number",
                  help = "Number of .par files to generate", metavar = "INT")


args = parser.parse_args()

numbers = int(args.number)

directory = str(args.directory)

if directory[-1]!='/':
        directory = directory + '/'

if os.path.exists(directory):
	print('Starting now')
else:
	os.mkdir(directory)

header = ['NAME', 'PSRJ', 'F0', 'F1', 'RA', 'DEC', 'PEPOCH', 'UNITS']#, 'H0', 'COSIOTA', 'PSI', 'PHI0', 'HPLUSS', 'HCROSS'

#limits = [['STR'], ['STR'], [0,rand1*750], [rand2*1e-7], [HH:MM:SS.dec], [HH:MM:SS.dec], PEPOCH, [STR]]#, [rand2*1e-23], [-1,1], [0,pi/2], [0, pi], [0, H0], [0,H0]]

for number in range(numbers):
	par_list = []

	rand1 = random.random()
	rand2 = random.random()
	pulsar_dict = {}
	pulsar_name = 'JPULSAR' + str(number)
	outfile = directory + pulsar_name + '.par'

	pulsar_dict[header[0]] = pulsar_name
	par_list.append(pulsar_dict[header[0]])
	pulsar_dict[header[1]] = pulsar_name
	pulsar_dict[header[2]] = rand1 * 750
	pulsar_dict[header[3]] = rand2 * 1e-23
	RA1 = str(random.randint(0,23))
	RA2 = str(random.randint(0,59))
	RA3 = str(random.random()*60)
	RA_all = RA1 + RA2 + RA3
	pulsar_dict[header[4]] = RA_all
	DEC1 = str(random.randint(-89,89))
        DEC2 = str(random.randint(0,59))
        DEC3 = str(random.random()*60)
        DEC_all = DEC1 + DEC2 + DEC3
        pulsar_dict[header[5]] = DEC_all
	pulsar_dict[header[6]] = 57800
	pulsar_dict[header[7]] = 'TDB'
 
        par_list.append(pulsar_dict[header[0]])
        par_list.append(pulsar_dict[header[1]])
        par_list.append(pulsar_dict[header[2]])
        par_list.append(pulsar_dict[header[3]])
        par_list.append(pulsar_dict[header[4]])
        par_list.append(pulsar_dict[header[5]])
        par_list.append(pulsar_dict[header[6]])
        par_list.append(pulsar_dict[header[7]])
	pulsar_out = open(outfile, 'w+')
	pulsar_out.seek(0)
	for posn, entry in enumerate(header):
		pulsar_out.write(entry + '\t' + str(par_list[posn]) + '\n')
	pulsar_out.close()







