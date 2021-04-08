import numpy as np
from scipy.stats import multivariate_normal
import multilateration as mlat
from scipy.spatial import distance
import pandas as pd
import pickle



Radius       	= [10, 20, 30] 		# distance between the reference points and the query point
Noise_level 	= 2+np.arange(9)	# noise level
Ks          	= [3, 6, 10]		# number of reference points
methods			= ['MAPMLAT', 'LMLAT', 'MLAT', 'PMLAT', 'BMLAT']
n_runs			= 30				# number of runs

for k in Ks:
	print('K = %d'%(k))
	for radius in Radius:
		print('\tradius = %d'%(radius))

		q_star = pickle.load(open('./dataset/nl_0_K_'+str(k)+'_RD_'+str(radius)+'.pic', 'rb'))[0]['q']

		loglike = {}
		n = []
		l = []
		m = []
		r = []
		for method in methods:
			print('\t\t'+method)		

			for noise_level in Noise_level:
				print('\t\t\tnoise level = %d'%(noise_level))

				for run in np.arange(n_runs):
					Q = pickle.load(open('results/samples/MT_'+method+'_K_'+str(k)+'_RD_'+str(radius)+'_nl_'+str(noise_level)+'_r_'+str(run)+'.pic', 'rb'))
					
					mu= np.mean(Q, axis=0)
					C = np.cov(Q.T)
					n.append(noise_level)
					l.append(multivariate_normal.pdf(q_star, mu, C))
					m.append(method)
					r.append(run)
							
		loglike['noise_level'] 	= n
		loglike['likelihood']  	= l
		loglike['method']		= m
		loglike['run']			= r

		df = pd.DataFrame(loglike)
		df.to_csv('./results/likelihood/likelihood'+'_K_'+str(k)+'_RD_'+str(radius)+'.csv')
