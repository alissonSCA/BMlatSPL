import pickle
import matplotlib.pyplot as plt
import numpy as np



Radius       = [10, 20, 30] #maximum distance the sensor could read
Noise_level = 1+np.arange(10)
Ks          = [3, 6, 10]

for radius in Radius:	
	for K in Ks:
		e_rw = pickle.load(open('./results/18_03/circle/error'+'_K_'+str(K)+'_RD_'+str(radius)+'.pic', 'rb'))


		Noise = 1+np.arange(10)
		plt.plot(Noise, e_rw, 'o-')
		plt.legend(['linear', 'regular', 'd. Jean', 'PML', 'mean', 'mode'])
		plt.ylim((0,15))
		plt.xlabel('noise level')
		plt.ylabel('error')
		plt.savefig('./figs/18_03/circle/error_circle_18_03'+'_K_'+str(K)+'_RD_'+str(radius)+'.png')
		plt.show()

		print(e_rw)

# L = [10]
# for i, l in enumerate(L):
# 	print(l)
# 	dataset = pickle.load(open('./dataset/rw_nl_10_len_'+str(l)+'.pic', 'rb'))
# 	for j in np.arange(l):
# 		R = dataset[j]['R']
# 		plt.figure()
# 		plt.scatter(R[:,0], R[:,1])
# 		plt.show()
