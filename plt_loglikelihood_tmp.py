import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
sns.set_theme(style="dark")

Radius       	= [10, 20, 30] 		# distance between the reference points and the query point
Noise_level 	= 2+np.arange(9)	# noise level
Ks          	= [3, 6, 10]		# number of reference points
methods			= ['MAPMLAT', 'LMLAT', 'MLAT', 'PMLAT', 'BMLAT']

for k in Ks:
	print('K = %d'%(k))
	for radius in Radius:
		print('\tradius = %d'%(radius))
		loglike = pd.read_csv('./results/likelihood/likelihood'+'_K_'+str(k)+'_RD_'+str(radius)+'.csv')
			
		sns.set_theme(style="ticks")

		# Initialize the figure with a logarithmic x axis
		f, ax = plt.subplots(figsize=(7, 6))
		# ax.set_yscale("log")

		# Load the example planets dataset
		dt = loglike[loglike['noise_level'] > 3]

		# Plot the orbital period with horizontal boxes
		# sns.boxplot(x="noise_level", y="likelihood", data=dt, hue='method',
		#             whis=[0, 100], width=.6, palette="vlag")
		sns.pointplot(x="noise_level", y="likelihood", data=dt, hue='method', ci='sd', markers='.', palette="colorblind")

		# # Add in points to show each observation
		# sns.stripplot(x="noise_level", y="likelihood", data=dt, hue='method',
		#               size=2, linewidth=0)

		# Tweak the visual presentation
		ax.xaxis.grid(True)
		ax.set(ylabel="Likelihood", xlabel='noise level', title="k=%d, radius=%d"%(k, radius))
		sns.despine(trim=True, left=True)
		
		handles, labels = ax.get_legend_handles_labels()
		ax.legend(handles=handles, labels=['MMLAT', 'LMLAT', 'MLAT', 'PMLAT', 'BMLAT'], title="")

		plt.savefig('./figures/likelihood/likelihood'+'_K_'+str(k)+'_RD_'+str(radius)+'.png')		