import random
from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument("-n", "--n_chunks", dest = "n_chunks",
                  help = "Number of chunks to be used", metavar = "INT")
parser.add_argument("-s", "--seed", dest = "seed",
                  help = "Random seed to use for number generator", metavar = "INT", default = "None")

args = parser.parse_args()
seeder = args.seed
n_chunks = int(args.n_chunks)

random.seed()

number = random.randint(0,2**n_chunks)

binary = bin(number)[2:-1]
maxbin = bin(2**n_chunks)[2:-1]
while len(binary)<len(maxbin):
	binary = '0' + binary

outfile = open('input_binary.txt','w+')

outfile.seek(0)

outfile.write('Input binary:\n' + str(binary) + '\n')

outfile.close()



# for a given binary, work out chunk lengths
# either break up into right number of chunks (ie 8),
# multiply scale snr by binary number value
# and then split back together.
       
