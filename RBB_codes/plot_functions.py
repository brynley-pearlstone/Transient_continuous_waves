def plot_data(data, output):
        import matplotlib as mpl
	mpl.use("Agg")
        import matplotlib.pyplot as plt
	import numpy as np

        plt.bar(range(len(data)),data)
        plt.grid(True)
        plt.title("Data")
	ax = plt.gca();
       
	ax.set_xticklabels([])
	ax.set_ylim([np.amin(data) - (0.25* ( np.amax(data)-np.amin(data))) , np.amax(data) +  (0.25 *( np.amax(data)-np.amin(data)))])
        major_ticks = np.arange(np.floor(np.amin(data)), np.floor(np.amax(data)+2), 1)# np.floor(np.amax(data) - np.amin(data)))
        ax.set_yticks(major_ticks, minor=False)
	plt.show()
	#plt.savefig(output +  "data.png")

def plot_odds(var, output):
        import matplotlib as mpl
	import numpy as np
	mpl.use("Agg")
        import matplotlib.pyplot as plt

        plt.plot(var, range(len(var),0,-1))
        plt.xlabel("log_10 Posterior")
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
        #plt.savefig(output +  "odds.png")

def barcode_plot(sorted_binaries, sorted_post, data, true_binary_position, output):
	
	import matplotlib as mpl
	mpl.use("Agg")
        import matplotlib.pyplot as plt
	import numpy as np
	import matplotlib.gridspec as gridspec

	shift_up_odds = []
	for post in sorted_post:
		shift_up_odds.append(post + np.abs(np.amin((sorted_post[-1]))))
	bin_array = np.array(sorted_binaries)
	odds_scale = [(x/shift_up_odds[0]) for x in shift_up_odds]
	shifted_array = []
	for item in bin_array:
		shifted_array.append(item - 0.5)
	scaled_binaries = [] 
	for [i,item] in enumerate(shifted_array):
		scaled_binaries.append(odds_scale[i] * item)
		scaled_binaries[i] = scaled_binaries[i] + 0.5
	gs = gridspec.GridSpec(9,4)

	ax1 = plt.subplot(gs[0, :-1])
	plot_data(data, output)

	ax3 = plt.subplot(gs[1:,:-1])
	y = plt.imshow(scaled_binaries, cmap = 'gray_r', interpolation='none')
	plt.xlabel('Chunk')
	plt.ylabel('Rank')
	cx = plt.gca();
	major_ticks = np.arange(0, len(sorted_post)+1, 5) 
	minor_ticks = np.arange(0, len(sorted_post), 1)                                               
	cx.set_yticklabels(major_ticks)	
	cx.set_yticks(np.arange(0, len(sorted_post), 1), minor=True)
        cx.set_yticks(major_ticks)
        cx.set_yticklabels(major_ticks)
	cx.set_xticks(np.arange(0, len(sorted_binaries[1]), 1))
       	cx.set_xticklabels(np.arange(1, len(sorted_binaries[1])+1, 1))
	cx.set_aspect(1.0/cx.get_data_ratio())
	for i in range(len(sorted_post)):
		cx.axhline(i+0.5, linestyle='-', color='k')
        for j in range(len(sorted_binaries[1])):
                cx.axvline(j+0.5, linestyle='-', color='k')
	# Put in the red lines around true binary
	if true_binary_position<50:
		cx.axhline(true_binary_position-0.5, linestyle='-', color='r')	
		cx.axhline(true_binary_position+0.5, linestyle='-', color='r')
		cx.axvline(len(sorted_binaries[1])-0.5, linestyle='-', color='r')
		cx.axvline(-0.5, linestyle='-', color='r')
	cx.grid(which='min r')                               

	ax4 = plt.subplot(gs[1:, -1])
	plot_odds(sorted_post, output)

	plt.savefig(output + 'barcode.png')

