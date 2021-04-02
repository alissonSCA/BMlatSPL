import numpy as np
from scipy.spatial import distance
import pickle


# Setup params
Radius       = [10, 20, 30] 		# distance between reference points and query point
Noise_level  = np.linspace(0,10,11) # noise level
Ks           = [3, 6, 10]			# number of reference points
N            = 30 					# number of datasets

## Generate dataset
for radius in Radius:
	print('radius = %d'%(radius))  
	for K in Ks:  	
		print('\tK = %d'%(K))
		Alpha = [(2*np.pi)*(i/K) for i in 1+np.arange(K)]
		q = np.random.uniform(-40, 40,size=[1, 2])
		R = np.array([q + [radius*np.cos(alpha), radius*np.sin(alpha)] for alpha in Alpha])[:,0,:]
		d = distance.cdist(R, q)[:,0]

		for noise_level in Noise_level:
			print('\t\tnoise_level = %1.2f'%(noise_level))

			dataset = []
			while len(dataset) < N:
				data = {'R':R + np.random.normal(0, noise_level, size=[K,2]), 'd':d, 'q':q, 'K':K}
				dataset.append(data)
				print('\t\t\t%d of %d'%(len(dataset), N))

			pickle.dump(dataset, open('./dataset/nl_'+('%1.0f'%noise_level)+'_K_'+str(K)+'_RD_'+str(radius)+'.pic', 'wb'))

