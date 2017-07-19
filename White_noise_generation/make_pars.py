import os
from argparse import ArgumentParser
import random
import numpy as np

parser = ArgumentParser()

parser.add_argument("-d", "--directory", dest = "directory",
                  help = "Location to put .par file", metavar = "STRING")
parser.add_argument("-n", "--Number", dest = "number",
                  help = "Number of .par files to generate", metavar = "INT")


args = parser.parse_args()

numbers = str(args.number)

directory = str(args.directory)

if directory[-1]!='/':
        directory = directory + '/'

if os.path.exists(directory):
	print('Starting now')
else:
	os.mkdir(directory)

header = ['NAME', 'PSRJ', 'F0', 'F1', 'RA', 'DEC', 'PEPOCH', 'UNITS', 'H0', 'COSIOTA', 'PSI', 'PHI0']#, 'HPLUSS', 'HCROSS'

#limits = [['STR'], ['STR'], [0,rand1*750], [rand2*1e-7], [HH:MM:SS.dec], [HH:MM:SS.dec], PEPOCH, [STR], [rand2*1e-23], [-1,1], [0,pi/2], [0, pi]]#, [0, H0], [0,H0]]

#for number in range(numbers):
par_list = []
rand1 = random.random()
rand2 = random.random()
pulsar_dict = {}

pulsar_name = 'JPULSAR' + str(numbers)
outfile = directory + pulsar_name + '.par'

pulsar_dict[header[0]] = pulsar_name
#par_list.append(pulsar_dict[header[0]])
pulsar_dict[header[1]] = pulsar_name
pulsar_dict[header[2]] = rand1 * 750
pulsar_dict[header[3]] = rand2 * 1e-10
RA1 = str(random.randint(0,23))
RA2 = str(random.randint(0,59))
RA3 = str(random.random()*60)
RA_all = str(RA1) + ':' + str(RA2) + ':' + str(RA3)
pulsar_dict[header[4]] = RA_all
cosDEC = (random.random() - 0.5 ) * 2
dec = np.arccos(cosDEC)
decdeg = dec * 180/np.pi

def decdeg2dms(dd):
	mnt,sec = divmod(dd*3600,60)
	deg,mnt = divmod(mnt,60)
	return deg,mnt,sec

dec_degree, dec_minute, dec_seconds = decdeg2dms(decdeg)
dec_deg_int = int(dec_degree)
dec_minute_int = int(dec_minute)
dec_seconds_int = int(dec_seconds)
#DEC2 = str(random.randint(0,59))

#DEC3 = str(random.random()*60)
DEC_all = str(dec_deg_int) + ':' + str(dec_minute_int) + ':' + str(dec_seconds)
pulsar_dict[header[5]] = DEC_all
pulsar_dict[header[6]] = 57800
pulsar_dict[header[7]] = 'TDB'
pulsar_dict[header[8]] = str(rand2 * 1e-23)
pulsar_dict[header[9]] = str((random.random()*2)-1)
pulsar_dict[header[10]] = str(random.random()*np.pi*0.5)
pulsar_dict[header[11]] = str(random.random()*np.pi)
 
par_list.append(pulsar_dict[header[0]])
par_list.append(pulsar_dict[header[1]])
par_list.append(pulsar_dict[header[2]])
par_list.append(pulsar_dict[header[3]])
par_list.append(pulsar_dict[header[4]])
par_list.append(pulsar_dict[header[5]])
par_list.append(pulsar_dict[header[6]])
par_list.append(pulsar_dict[header[7]])
par_list.append(pulsar_dict[header[8]])
par_list.append(pulsar_dict[header[9]])
par_list.append(pulsar_dict[header[10]])
par_list.append(pulsar_dict[header[11]])

pulsar_out = open(outfile, 'w+')
pulsar_out.seek(0)
for posn, entry in enumerate(header):
	pulsar_out.write(entry + '\t' + str(par_list[posn]) + '\n')
pulsar_out.close()


prior_file = directory + pulsar_name + '.priors'

prior_out = open(prior_file, 'w+')
prior_out.seek(0)

prior_head = ['H0', 'PHI0', 'PSI', 'COSIOTA']
prior_form = 'uniform'
prior_lower = [0, 0, 0, -1]
prior_upper = [1e-20, 3.141592653589793, 1.5707963267948966, 1]

for place,name in enumerate(prior_head):
	prior_out.write(name + '\t' + prior_form + '\t' + str(prior_lower[place]) + '\t' + str(prior_upper[place]) + '\n')
prior_out.close()

