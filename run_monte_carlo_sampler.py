import numpy as np
import multilateration as mlat
import pickle


Radius       	= [10, 20, 30] 		# distance between the reference points and the query point
Noise_level 	= 1+np.arange(10)	# noise level
Ks          	= [3, 6, 10]		# number of reference points
methods			= ['mlat', 'lin', 'pmlat', 'pml']




for method in methods:
	print(method)
	for k in Ks:
		print('\tK = %d'%(k))
		for radius in Radius:
			print('\t\tradius = %d'%(radius))
			dataset = pickle.load(open('./dataset/nl_0_K_'+str(k)+'_RD_'+str(radius)+'.pic', 'rb'))[0]
			for noise_level in Noise_level:
				print('\t\t\tnoise level = %d'%(noise_level))
				
				R = dataset['R']
				d = dataset['d']
				# q = dataset['q']

				Q = mlat.monte_carlo_sampler(method, R, d, noise_level)
				pickle.dump(Q, open('results/samples/MT_'+method+'_K_'+str(k)+'_RD_'+str(rd)+'_nl_'+str(noise_level)+'.pic', 'wb'))
