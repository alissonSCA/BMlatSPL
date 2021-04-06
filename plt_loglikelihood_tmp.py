import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
sns.set_theme(style="dark")

Radius       	= [10, 20, 30] 		# distance between the reference points and the query point
Noise_level 	= 1+np.arange(10)	# noise level
Ks          	= [3, 6, 10]		# number of reference points
methods			= ['pmlat', 'lin', 'mlat', 'pml', 'BMlat']

for k in Ks:
	print('K = %d'%(k))
	for radius in Radius:
		print('\tradius = %d'%(radius))
		loglike = pd.read_csv('./results/loglikelihood/loglike'+'_K_'+str(k)+'_RD_'+str(radius)+'.csv')
		
		# Define the palette as a list to specify exact values
		# palette = sns.color_palette("rocket_r")

		# Plot the lines on two facets
		# sns.relplot(
		#     data=loglike,
		#     x="noise_level", y="likelihood",
		#     hue="method",
		#     kind="line"
		# )	
		sns.set_theme(style="ticks")

		# Initialize the figure with a logarithmic x axis
		f, ax = plt.subplots(figsize=(7, 6))
		# ax.set_yscale("log")

		# Load the example planets dataset
		dt = loglike[loglike['noise_level'] > 4]

		# Plot the orbital period with horizontal boxes
		sns.boxplot(x="noise_level", y="likelihood", data=dt, hue='method',
		            whis=[0, 100], width=.6, palette="vlag")

		# # Add in points to show each observation
		# sns.stripplot(x="noise_level", y="likelihood", data=dt, hue='method',
		#               size=2, linewidth=0)

		# Tweak the visual presentation
		ax.xaxis.grid(True)
		ax.set(ylabel="likelihood", title="k=%d, rd=%d"%(k, radius))
		sns.despine(trim=True, left=True)
		
		plt.savefig('./figures/likelihood/likelihood'+'_K_'+str(k)+'_RD_'+str(radius)+'.png')		