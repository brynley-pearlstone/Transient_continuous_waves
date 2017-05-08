def plot_data(data, output):
        import matplotlib as mpl
        import matplotlib.pyplot as plt
	import numpy as np

#        plt.clf()
        plt.plot(data)
#        plt.xlabel("Chunk number")
#        plt.ylabel("Data atoms (Evidence)")
        plt.grid(True)
        plt.title("Data atoms")
#        plt.show()
	ax = plt.gca();
        ax.set_yticklabels([])
        ax.set_xticklabels([])
#        ax.set_xticks(np.arange(0, len(data), 1));
 #       ax.set_xticklabels(np.arange(0, len(data), 1));  
#	ax.set_aspect(0.25/ax.get_data_ratio())      
	plt.savefig(output +  "data.png")


def plot_like(var, output):
	import matplotlib as mpl
	import matplotlib.pyplot as plt
	
#	plt.clf()
	plt.plot(var)
	plt.xlabel("Rank (Least likely to most likely)")
	plt.ylabel("log_{10}(Evidence) for each signal model")
	plt.grid(True)
	plt.title("Plot of sorted log-likelihood by rank")
#	plt.show()
	plt.savefig(output +  "evidence.png")

def plot_odds(var, output):
        import matplotlib as mpl
        import matplotlib.pyplot as plt


        plt.plot(var[::-1], range(len(var),0,-1))
        plt.ylabel("Rank (Least to most)")
        plt.xlabel("log_{10}(Odds)")
	
        plt.grid(True)
#	plt.tick_params(
#		axis='x',          # changes apply to the x-axis
#		which='both',      # both major and minor ticks are affected
#		bottom='off',      # ticks along the bottom edge are off
#		top='off',         # ticks along the top edge are off
#		labelbottom='off') # labels along the bottom edge are off
	
#       plt.title("Log-odds sorted by rank")
	bx = plt.gca()
#	bx.set_aspect(4.0/bx.get_data_ratio())
	bx.set_yticklabels([])
	plt.show()
        plt.savefig(output +  "odds.png")

def barcode_plot(sorted_binaries, sorted_odds, data, output):
        import matplotlib as mpl
        import matplotlib.pyplot as plt
	import numpy as np
	import matplotlib.gridspec as gridspec
	shift_up_odds = []
	for odd in sorted_odds:
		shift_up_odds.append(odd + sorted_odds[0])

	bin_array = np.array(sorted_binaries)
	# Scale binaries so that black/whites are highlighted
	odds_scale = [(x/shift_up_odds[-1]) for x in shift_up_odds]
	shifted_array = []
	for item in bin_array:
		shifted_array.append(item - 0.5)
	
	scaled_binaries = [] 
	for [i,item] in enumerate(shifted_array):
		scaled_binaries.append(odds_scale[i] * item)
		scaled_binaries[i] = scaled_binaries[i] + 0.5
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
	cx.set_yticks(np.arange(-0.5, len(sorted_odds), 1));
	cx.set_xticks(np.arange(-0.5, len(sorted_binaries[1]), 1));
	cx.set_yticklabels(np.arange(0, len(sorted_odds)+1, 1));
	cx.set_xticklabels(np.arange(0, len(sorted_binaries[1])+1, 1));
	cx.grid(color='k', linestyle='-', linewidth=1)
	cx.set_aspect(1.0/cx.get_data_ratio())

	ax4 = plt.subplot(gs[1:, -1])
	#plt.subplot(2,2,4)
	plot_odds(sorted_odds, output)
#	axistemp = (range(len(sorted_binaries[1])))
