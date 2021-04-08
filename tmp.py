import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
sns.set_theme(style="dark")

Radius       	= [10, 20, 30] 		# distance between the reference points and the query point
Noise_level 	= 2+np.arange(9)	# noise level
Ks          	= [3, 6, 10]		# number of reference points
methods			= ['pmlat', 'lin', 'mlat', 'pml', 'BMlat']
methods_new		= ['MAPMLAT', 'LMLAT', 'MLAT', 'PMLAT', 'BMLAT']

for k in Ks:
	print('K = %d'%(k))
	for radius in Radius:
		print('\tradius = %d'%(radius))
		loglike = pd.read_csv('./results/sample_multilateration/distance'+'_K_'+str(k)+'_RD_'+str(radius)+'.csv')
		for old_m, new_m in zip(methods, methods_new):
			loglike[loglike['method']==old_m]['method']	= new_m
		loglike.to_csv('./results/sample_multilateration/distance'+'_K_'+str(k)+'_RD_'+str(radius)+'.csv', index=False)