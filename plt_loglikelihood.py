import pickle
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
		loglike = pickle.load(open('./results/loglikelihood/loglike'+'_K_'+str(k)+'_RD_'+str(radius)+'.pic', 'rb'))
		
		sns.set_theme(style="ticks")

		# Define the palette as a list to specify exact values
		palette = sns.color_palette("rocket_r")

		# Plot the lines on two facets
		sns.relplot(
		    data=loglike,
		    x="noise_level", y="likelihood",
		    hue="method",
		    kind="line"
		)	
		for i, method in enumerate(methods):
			print(method)
			print(loglike['likelihood'][i*9 + 9])
			print(loglike['method'][i*9 + 9])
			print('--------')

		plt.show()			