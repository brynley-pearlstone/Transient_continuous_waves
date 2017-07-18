import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument("-l", "--data_file", dest = "data_list",
                  help = "File containing data to plot", metavar = "STRING")
parser.add_argument("-d", "--directory", dest = "directory",
                  help = "Directory for Pulsar.", metavar = "STRING")

args = parser.parse_args()

filename = str(args.data_list)

lines = []
f = open(filename, 'r')
for line in f:
	print(line)
        lines.append(line[:-1])

#table_headers = lines[0:14]
#lines[0:14]= []
splitline = [line.split('\t') for line in lines]

f.close

time = []
RE = []
IM = []

for line in splitline:
	print(line)
	time.append(line[0])
	RE.append(line[1])
	IM.append(line[2])


plt.plot(time, RE)
plt.ylabel("Strain (Real component)")
plt.xlabel("GPS time")
plt.title("Real part of strain")
plt.savefig(str(args.directory) +  "real.png")

plt.plot(time, IM)
plt.ylabel("Strain (imag component)")
plt.xlabel("GPS time")
plt.title("Imaginary part of strain")
plt.savefig(str(args.directory) +  "imag.png")




