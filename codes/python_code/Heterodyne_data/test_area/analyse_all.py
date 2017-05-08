import os

# Sanity check
# Test the number of chunked time files for each detector

H1_chunks = []
L1_chunks = []

for H1item in os.listdir('H1/'):
	H1_chunks.append(H1item)

for L1item in os.listdir('L1/'):
        L1_chunks.append(L1item)

print(L1_chunks)
print(H1_chunks)

if len(L1_chunks) != len(H1_chunks):
	print('Number of chunk files in each detector not equal! Please address')
if not os.path.exists('output/'):
	os.makedirs('output/')

for item in range(len(H1_chunks)):
#	print(item[0:2])
	os.system('lalapps_pulsar_parameter_estimation_nested --detectors H1,L1 --par-file ../PULSAR04.par --input-files H1/' + (H1_chunks[item]) + ',L1/' + (L1_chunks[item]) + ' --outfile output/' + (H1_chunks[item][29:-3]) + 'hdf --Nlive 1024 --Nmcmcinitial 0 --tolerance 0.1 --prior-file ../PULSAR04.priors')



