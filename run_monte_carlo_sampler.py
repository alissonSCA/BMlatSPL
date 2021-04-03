import numpy as np
import multilateration as mlat
import pickle


Radius       	= [10, 20, 30] 		# distance between the reference points and the query point
Noise_level 	= 1+np.arange(10)	# noise level
Ks          	= [3, 6, 10]		# number of reference points
methods			= ['mlat', 'lin', 'pmlat', 'pml']




for method in methods:
	for k in Ks:
		for radius in Radius:
			dataset = pickle.load(open('./dataset/nl_0_K_'+str(k)+'_RD_'+str(radius)+'.pic', 'rb'))[0]
			for noise_level in Noise_level:
				R = dataset['R']
				d = dataset['d']
				# q = dataset['q']

				Q = mlat.monte_carlo_sampler(method, R, d, noise_level)
				pickle.dump(err, open('results/samples/MT_'+method+'_K_'+str(k)+'_RD_'+str(rd)+'_nl_'+str(noise_level)+'.pic', 'wb'))
				