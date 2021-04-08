import pickle
import matplotlib.pyplot as plt
import numpy as np



Radius       = [10, 20, 30] #maximum distance the sensor could read
Noise_level = 2+np.arange(9)
Ks          = [3, 6, 10]

for radius in Radius:	
	for K in Ks:
		e_rw = pickle.load(open('./results/multilateration/error'+'_K_'+str(K)+'_RD_'+str(radius)+'.pic', 'rb'))[:len(Noise_level),:]


		plt.plot(Noise_level, e_rw, 'o-')
		plt.legend(['linear', 'regular', 'pmlat', 'pml', 'mean', 'mode'])
		plt.ylim((0,15))
		plt.xlabel('noise level')
		plt.ylabel('error')
		plt.savefig('./figures/multilateration/error_K_'+str(K)+'_RD_'+str(radius)+'.png')
		plt.close('all')

		print(e_rw)
