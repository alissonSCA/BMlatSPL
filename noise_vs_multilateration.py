import numpy as np
from scipy.spatial import distance
import matplotlib.pyplot as plt
import multilateration as mlat
import pandas as pd
import pickle

Radius       = [10, 20, 30] #maximum distance the sensor could read
Noise_level = 2+np.arange(9)
Ks          = [3, 6, 10]

model = mlat.BayesianMultilateration()
for radius in Radius:	
	for K in Ks:
		error = np.zeros([9, 6])
		for noise_level in Noise_level:
			dataset = pickle.load(open('./dataset/nl_'+str(noise_level)+'_K_'+str(K)+'_RD_'+str(radius)+'.pic', 'rb'))

			err = np.zeros([len(dataset), 6])
			for i, data in enumerate(dataset):
				R = data['R']
				d = data['d']
				q = data['q'].reshape(1,-1)

				model.sampling(R, d, sigma=noise_level, theta=2e2)

				q_lin = mlat.lin_multilateration(R, d)
				q_reg = mlat.multilateration(R, d)
				q_dj  = mlat.p_multilateration(R, d)
				q_PML = mlat.PML(R, d)
				q_mea = model.get_mean()
				q_mod = model.get_mode()

				estimated_points = np.array([q_lin, q_reg, q_dj, q_PML, q_mea, q_mod])
				estimated_points = estimated_points.reshape(6, 2)
				distances = distance.cdist(q, estimated_points)[0,:]
				err[i, :] = distances	
				print(distances)
			error[noise_level-2,:] = np.mean(err, axis=0)

		pickle.dump(error, open('./results/multilateration/error'+'_K_'+str(K)+'_RD_'+str(radius)+'.pic', 'wb'))