import numpy as np
import multilateration as mlat
import pickle
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal

Noise_level = 2+np.arange(9)

dataset = pickle.load(open('./dataset/nl_0_K_3_RD_30.pic', 'rb'))[0]
R = dataset['R']
d = dataset['d']
q = dataset['q']

model = mlat.BayesianMultilateration()

l = []
for noise_level in Noise_level:
	model.sampling(R, d, sigma=noise_level, theta=30, max_treedepth=12, adapt_delta=0.9)
	# print(model.params)


	import seaborn as sns
	sns.set_theme(style="ticks")

	# Load the penguins dataset
	# penguins = sns.load_dataset("penguins")

	# Show the joint distribution using kernel density estimation

	n_samples, k, dim = model.params['s'].shape
	data = {'sample':[], 'ref_point':[], 'x1':[], 'x2':[]}
	for i in np.arange(n_samples):
		for j in np.arange(k):
			data['sample'].append(i)
			data['ref_point'].append('ref_%d'%(j))
			data['x1'].append(model.params['s'][i,j,0])
			data['x2'].append(model.params['s'][i,j,1])
		data['sample'].append(i)
		data['ref_point'].append('q')
		data['x1'].append(model.Q[i,0])
		data['x2'].append(model.Q[i,1])

	g = sns.jointplot(
	    data=data,
	    x='x1', y='x2', hue='ref_point', 
	    kind="kde",
	)


	sns.scatterplot(data=data, x='x1', y='x2', hue='ref_point', s=5, ax=g.ax_joint)	
	sns.scatterplot(x=R[:,0], y=R[:,1], color='k', ax=g.ax_joint)
	sns.scatterplot(x=q[:,0], y=q[:,1], color='k', ax=g.ax_joint)	

	plt.savefig('./figures/reference_points_sample'+'_nl_'+str(noise_level)+'.png')
	plt.close('all')

	mu= np.mean(model.Q, axis=0)
	C = np.cov(model.Q.T)
	l.append(multivariate_normal.pdf(q, mu, C))

sns.set_theme(style="darkgrid")
like_data = {'noise_level':Noise_level, 'likelihood':l}

# Plot the responses for different events and regions
sns.lineplot(x="noise_level", y="likelihood",
             # hue="region", style="event",
             data=like_data)
plt.savefig('./figures/likelihood.png')
plt.close('all')
print(l)