import numpy as np
import os

Radius       	= [10, 20, 30] 		# distance between the reference points and the query point
Noise_level 	= 2+np.arange(9)	# noise level
Ks          	= [3, 6, 10]		# number of reference points
methods			= ['pmlat', 'lin', 'mlat', 'pml', 'BMlat']
methods_new		= ['MAPMLAT', 'LMLAT', 'MLAT', 'PMLAT', 'BMLAT']
n_runs			= 30				# number of runs

for k in Ks:
	print('K = %d'%(k))
	for radius in Radius:
		print('\tradius = %d'%(radius))

		for noise_level in Noise_level:
			print('\t\tnoise level = %d'%(noise_level))

			for run in np.arange(n_runs):
				print('\t\t\trun = %d'%(run))

				for old_method, new_method in zip(methods, methods_new):
					old_path = './MT_'+old_method+'_K_'+str(k)+'_RD_'+str(radius)+'_nl_'+str(noise_level)+'_r_'+str(run)+'.pic'
					new_path = './MT_'+new_method+'_K_'+str(k)+'_RD_'+str(radius)+'_nl_'+str(noise_level)+'_r_'+str(run)+'.pic'
					os.rename(old_path, new_path)
