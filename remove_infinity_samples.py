import pickle
import numpy as np
import os

Radius       	= [10, 20, 30] 		# distance between the reference points and the query point
Noise_level 	= 1+np.arange(10)	# noise level
Ks          	= [3, 6, 10]		# number of reference points
methods			= ['pmlat', 'lin', 'mlat', 'pml', 'BMlat']
n_runs			= 30				# number of runs

for method in methods:
	print(method)
	for k in Ks:
		print('\tK = %d'%(k))
		for radius in Radius:
			print('\t\tradius = %d'%(radius))

			q_star = pickle.load(open('./dataset/nl_0_K_'+str(k)+'_RD_'+str(radius)+'.pic', 'rb'))[0]['q']
			for noise_level in Noise_level:
				print('\t\t\tnoise level = %d'%(noise_level))

				for run in np.arange(n_runs):

					file_name = 'results/samples/MT_'+method+'_K_'+str(k)+'_RD_'+str(radius)+'_nl_'+str(noise_level)+'_r_'+str(run)+'.pic'
					Q = pickle.load(open(file_name, 'rb'))
					N = Q.shape[0]

					change = False

					nan_values = np.sum(np.isnan(Q), axis=1)
					n_nan = np.sum(nan_values)
					print('\t\t\t\tNAN Samples = %d'%(n_nan))
					if (n_nan > 0):
						change = True
						Q = Q[nan_values==0,:]				

					x = Q > 1000
					p_inf_values = np.sum(x, axis=1)
					n_p_inf = np.sum(p_inf_values)
					print('\t\t\t\t+inf = %d'%(n_p_inf))
					if n_p_inf > 0:
						change = True
						Q = Q[p_inf_values==0,:]				

					x = Q < -1000
					m_inf_values = np.sum(x, axis=1)
					n_m_inf = np.sum(m_inf_values)
					print('\t\t\t\t-inf = %d'%(n_m_inf))
					if n_m_inf > 0:
						change = True
						Q = Q[m_inf_values==0,:]	

					if change:
						os.rename(file_name, file_name+'.bkp')
						pickle.dump(Q, open(file_name, 'wb'))
						print('\t\t\t\tupdated!')