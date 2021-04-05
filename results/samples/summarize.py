import numpy as np
import pandas as pd
import os

methods = ['lin', 'mlat', 'pmlat', 'pml']
Ks	= [3, 6, 10]
Radius	= [10, 20, 30]
n_level = 1 + np.arange(10)
n_runs	= 30

summary = {'method':[], 'K':[], 'radius':[], 'noise_level':[], 'run':[]}
for method in methods:
	for K in Ks:
		for radius in Radius:
			for noise_level in n_level:
				for r in np.arange(n_runs):
					if (os.path.isfile('./MT_'+method+'_K_'+str(K)+'_RD_'+str(radius)+'_nl_'+str(noise_level)+'_r_'+str(r)+'.pic')):
						summary['method'].append(method)
						summary['K'].append(K)
						summary['radius'].append(radius)
						summary['noise_level'].append(noise_level)
						summary['run'].append(r)
					else:
						break
df = pd.DataFrame(summary)
df.to_csv('./summary.csv')
