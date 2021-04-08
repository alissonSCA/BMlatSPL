import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
sns.set_theme(style="dark")

Radius       	= [10, 20, 30] 		# distance between the reference points and the query point
Noise_level 	= 2+np.arange(9)	# noise level
Ks          	= [3, 6, 10]		# number of reference points
methods			= ['pmlat', 'lin', 'mlat', 'pml', 'BMlat']

for k in Ks:
	print('K = %d'%(k))
	for radius in Radius:
		print('\tradius = %d'%(radius))
		distance = pd.read_csv('./results/sample_multilateration/distance_K_'+str(k)+'_RD_'+str(radius)+'.csv')

		sns.set_theme(style="ticks")

		# Initialize the figure with a logarithmic x axis
		f, ax = plt.subplots(figsize=(7, 6))

		# Load the example planets dataset
		dt = distance[distance['noise_level'] > 2]
		# dt = dt[dt['distance']<1]

		# Plot the orbital period with horizontal boxes
		# sns.boxplot(x="noise_level", y="distance", data=dt, hue='method',
		#             width=.6, palette="vlag")
		sns.pointplot(x="noise_level", y="distance", data=dt, hue='method', ci='sd', markers='.', estimator=np.median)

		ax.xaxis.grid(True)
		ax.set(ylabel="distance", title="k=%d, rd=%d"%(k, radius), ylim=[0,1])
		sns.despine(trim=True, left=True)
		
		plt.savefig('./figures/sample_multilateration/distance_K_'+str(k)+'_RD_'+str(radius)+'.png')		