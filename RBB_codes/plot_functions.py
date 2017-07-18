def plot_data(data, output):
        import matplotlib as mpl
	mpl.use("Agg")
        import matplotlib.pyplot as plt
	import numpy as np

        plt.bar(range(len(data)),data)
        plt.grid(True)
        plt.title("Data atoms")
	ax = plt.gca();
#        ax.set_yticklabels([])
#	plt.locator_params(axis='y', nticks=2)
        plt.ylabel('Chunk Signal evidence')
	ax.set_xticklabels([])
	ax.set_ylim([np.amin(data) - (0.25* ( np.amax(data)-np.amin(data))) , np.amax(data) +  (0.25 *( np.amax(data)-np.amin(data)))])
	#plt.locator_params(axis='y', nticks=2)
        major_ticks = np.arange(np.floor(np.amin(data)), np.floor(np.amax(data)+2), np.floor(np.amax(data) - np.amin(data)))
        ax.set_yticks(major_ticks, minor=False)


	plt.savefig(output +  "data.png")



def plot_like(var, output):
	import matplotlib as mpl
	mpl.use("Agg")
	import matplotlib.pyplot as plt
	
#	plt.clf()
	plt.plot(var)
#	plt.xlabel("Rank (Least likely to most likely)")
	plt.ylabel("log_{10}(Evidence) for each signal model")
	plt.grid(True)
	plt.title("Plot of sorted log-likelihood by rank")
#	plt.show()
	plt.savefig(output +  "evidence.png")

def plot_odds(var, output):
        import matplotlib as mpl
	import numpy as np
	mpl.use("Agg")
        import matplotlib.pyplot as plt

        plt.plot(var, range(len(var),0,-1))
#        plt.ylabel("Rank (Least to most)")
        plt.xlabel("log_{10}(Odds)")
	
        plt.grid(True)
	bx = plt.gca()
	bx.set_xlim([np.amin(var)-10 , np.amax(var)+10 ])
	major_ticks = np.arange(np.floor(np.amin(var)), np.floor(np.amax(var)+2), 0.5 * ( np.floor(np.amax(var) - np.amin(var))))
	minor_ticks = np.arange(np.floor(np.amin(var)), np.floor(np.amax(var)+2), 0.1 * ( np.floor(np.amax(var) - np.amin(var))))
        bx.set_xticks(major_ticks, minor=False)
	bx.set_xticks(minor_ticks, minor=True)
        bx.grid(which = 'minor', alpha=0.5)
	bx.set_yticklabels([])
	plt.show()
        plt.savefig(output +  "odds.png")

def barcode_plot(sorted_binaries, sorted_odds, data, true_binary_position, output):
	
	import matplotlib as mpl
	mpl.use("Agg")
        import matplotlib.pyplot as plt
	import numpy as np
	import matplotlib.gridspec as gridspec
#	print(sorted_binaries[0])
#        print(sorted_binaries[-1])
#	print(sorted_odds[0])
#	print(sorted_odds[-1])

	shift_up_odds = []
	for odd in sorted_odds:
		shift_up_odds.append(odd + np.abs(np.amin((sorted_odds[-1]))))
	#print(shift_up_odds)
	bin_array = np.array(sorted_binaries)
	# Scale binaries so that black/whites are highlighted
	odds_scale = [(x/shift_up_odds[0]) for x in shift_up_odds]
	shifted_array = []
	for item in bin_array:
		shifted_array.append(item - 0.5)
	
	#print(shifted_array)
	scaled_binaries = [] 
	for [i,item] in enumerate(shifted_array):
		scaled_binaries.append(odds_scale[i] * item)
		scaled_binaries[i] = scaled_binaries[i] + 0.5
#		print(str(scaled_binaries[i]) + '\n')
	gs = gridspec.GridSpec(9,4)


	ax1 = plt.subplot(gs[0, :-1])
	#plt.subplot(2,2,1)
	plot_data(data, output)

	ax3 = plt.subplot(gs[1:,:-1])
	#plt.subplot(2,2,3)
	y = plt.imshow(scaled_binaries, cmap = 'gray', interpolation='none')
	plt.xlabel('Chunk definer')
	plt.ylabel('Rank')
	cx = plt.gca();
	
	major_ticks = np.arange(0, len(sorted_odds)+1, 5) 
#	print(major_ticks)
	minor_ticks = np.arange(0, len(sorted_odds), 1)                                               
	cx.set_yticklabels(major_ticks);	
	cx.set_yticks(np.arange(0, len(sorted_odds), 1), minor=True)
        cx.set_yticks(major_ticks);
        cx.set_yticklabels(major_ticks);
	cx.set_xticks(np.arange(-0.5, len(sorted_binaries[1]), 1))
	#cx.set_xticks(minor_ticks, minor=True)                    
       	cx.set_xticklabels(np.arange(0, len(sorted_binaries[1]), 1))

#	cx.grid(color='k', linestyle='-', linewidth=1)
	cx.set_aspect(1.0/cx.get_data_ratio())
	for i in range(len(sorted_odds)):
		cx.axhline(i+0.5, linestyle='-', color='k')
        for j in range(len(sorted_binaries[1])):
                cx.axvline(j+0.5, linestyle='-', color='k')
	# Put in the red lines around true binary
	cx.axhline(true_binary_position-0.5, linestyle='-', color='r')	
	cx.axhline(true_binary_position+0.5, linestyle='-', color='r')
	cx.axvline(len(sorted_binaries[1])-0.5, linestyle='-', color='r')
	cx.axvline(-0.5, linestyle='-', color='r')
	cx.grid(which='min r')                               
	#cx.grid(which = 'minor', alpha=0)                                                
	#ax.grid(which='major', alpha=0.5) 

	ax4 = plt.subplot(gs[1:, -1])
	#plt.subplot(2,2,4)
	plot_odds(sorted_odds, output)
	plt.savefig(output + 'barcode.png')
#	axistemp = (range(len(sorted_binaries[1])))
