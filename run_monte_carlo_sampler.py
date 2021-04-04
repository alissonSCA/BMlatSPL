import numpy as np
import multilateration as mlat
import pickle


Radius       	= [20]#[10, 20, 30] 		# distance between the reference points and the query point
Noise_level 	= 1+np.arange(10)	# noise level
Ks          	= [6]#[3, 6, 10]		# number of reference points
methods			= ['pmlat']#['mlat', 'lin', 'pmlat', 'pml']
n_runs			= 30				# number of runs




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
				for r in np.arange(n_runs):
					print('\t\t\t\trun = %d'%(r))
					Q = mlat.monte_carlo_sampler(method, R, d, noise_level)
					pickle.dump(Q, open('results/samples/MT_'+method+'_K_'+str(k)+'_RD_'+str(radius)+'_nl_'+str(noise_level)+'_r_'+str(r)+'.pic', 'wb'))

