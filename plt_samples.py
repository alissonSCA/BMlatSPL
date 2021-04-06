import pickle
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
sns.set_theme(style="dark")

Radius       	= [10, 20, 30] 		# distance between the reference points and the query point
Noise_level 	= 1+np.arange(10)	# noise level
Ks          	= [3, 6, 10]		# number of reference points
methods			= ['pmlat', 'lin', 'mlat', 'pml', 'BMlat']

for method in methods:
	print(method)
	for k in Ks:
		print('\tK = %d'%(k))
		for radius in Radius:
			print('\t\tradius = %d'%(radius))

			q_star = pickle.load(open('./dataset/nl_0_K_'+str(k)+'_RD_'+str(radius)+'.pic', 'rb'))[0]['q']
			for noise_level in Noise_level:
				print('\t\t\tnoise level = %d'%(noise_level))

				Q = pickle.load(open('results/samples/MT_'+method+'_K_'+str(k)+'_RD_'+str(radius)+'_nl_'+str(noise_level)+'.pic', 'rb'))
				x0 = Q[:,0]
				x1 = Q[:,1]

				data = {'x_0':x0, 'x_1':x1}

				g = sns.jointplot(data=data, x='x_0', y='x_1')

				sns.scatterplot(x=q_star[:,0], y=q_star[:,1], ec="r", s=15, linewidth=1.5, ax=g.ax_joint)
				plt.savefig('./figures/samples/MT_'+method+'_K_'+str(k)+'_RD_'+str(radius)+'_nl_'+str(noise_level)+'.png')
				plt.close('all')
