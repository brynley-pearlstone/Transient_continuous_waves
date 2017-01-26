def plot_like(var, output):
	import matplotlib as mpl
	import matplotlib.pyplot as plt
	
	plt.clf()
	plt.plot(var)
	plt.xlabel("Rank (Least likely to most likely)")
	plt.ylabel("log_{10}(Evidence) for each signal model")
	plt.grid(True)
	plt.title("Plot of sorted log-likelihood by rank")
	plt.show()
	plt.savefig(output +  "evidence.png")

def plot_odds(var, output):
        import matplotlib as mpl
        import matplotlib.pyplot as plt
	
        plt.clf()
        plt.plot(var)
        plt.xlabel("Rank (Least likely to most likely)")
        plt.ylabel("log_{10}(Odds)")
        plt.grid(True)
        plt.title("Plot of sorted log-odds (given model vs all other models) sorted by rank")
	plt.show()
        plt.savefig(output +  "odds.png")

def barcode_plot(sorted_binaries,  sorted_odds, output):
        import matplotlib as mpl
        import matplotlib.pyplot as plt
	
	# Scale binaries so that black/whites are highlighted
	odds_scale = [x/sorted_odds[-1] for x in sorted_odds]
	scaled_binaries = [odds_scale * i for i in sorted_binaries]
	
	#plot on 2d array
	plt.plot(scaled_binaries)
	plt.colorbar(orientation='vertical')
	plt.imshow(cmap='gray')
	

