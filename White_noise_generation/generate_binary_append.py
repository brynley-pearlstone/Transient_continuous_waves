import numpy as np
import random
from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument("-n", "--n_chunks", dest = "n_chunks",
                  help = "Number of chunks to be used", metavar = "INT")
parser.add_argument("-s", "--seed", dest = "seed",
                  help = "Random seed to use for number generator", metavar = "INT", default = "None")
parser.add_argument("-b", "--binary", dest = "binary",
                  help = "Binary number to be outputted", metavar = "INT", default = "NA")


args = parser.parse_args()
seeder = args.seed
n_chunks = int(args.n_chunks)
bina = str(args.binary)
random.seed()
#print(bina)

def generate_binary(n_chunks):
        number = random.randint(0,2**n_chunks + 1)
        binary = bin(number)[2:-1]
        maxbin = bin(2**n_chunks)[2:-1]
        while len(binary)<len(maxbin):
                binary = '0' + binary
	actual_cp_n = 0
	for i in range(n_chunks-1):
		if binary[i]!=binary[i+1]:
			actual_cp_n += 1
#        actual_cp_n = np.sum(np.abs(np.diff(binary)))
	return binary, actual_cp_n
	
n_cp = random.randint(0,n_chunks-1)
print(n_cp)
if bina=="NA":
	actual_cp_n = n_chunks + 1
#	number = random.randint(0,2**n_chunks)
#	binary = bin(number)[2:-1]
#	maxbin = bin(2**n_chunks)[2:-1]
#	while len(binary)<len(maxbin):
#		binary = '0' + binary
#	actual_cp_n = np.sum(np.abs(np.diff(binary)))
	while n_cp != actual_cp_n:
		binary, actual_cp_n = generate_binary(n_chunks)
		print(actual_cp_n)
elif len(bina)!=n_chunks:
	print('Chosen binary number is the wrong length. Please respecify!')
else:
	binary = bina

outfile = open('input_binary.txt','a')

#outfile.seek(0)

outfile.write(str(binary) + '\n')

outfile.close()



# for a given binary, work out chunk lengths
# either break up into right number of chunks (ie 8),
# multiply scale snr by binary number value
# and then split back together.
       
