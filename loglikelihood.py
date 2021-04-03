import numpy as np
from scipy.stats import multivariate_normal
import multilateration as mlat
from scipy.spatial import distance
import pickle


noise_level = 10
n_samples   = 1000
K           = 3
n_runs      = 30


dataset = pickle.load(open('./dataset/04_03/likelihood/nl_0_K_3_RD_30.pic', 'rb'))

err = np.zeros([len(dataset), 1])
for i, data in enumerate(dataset):
	R = data['R']
	d = data['d']
	q = data['q']

	# Q_lin  = np.zeros([n_samples, 2])
	# Q_reg  = np.zeros([n_samples, 2])
	# Q_prob = np.zeros([n_samples, 2])
	Q_pml  = np.zeros([n_samples, 2])
	for j in np.arange(n_samples):
		print('\tsample %d'%(j))
		R2 = R + np.random.normal(0, noise_level,size=[K,2])
		# Q_lin[j,:]  = mlat.lin_multilateration(R2, d)
		# Q_reg[j,:]  = mlat.multilateration(R2, d)
		# Q_prob[j,:] = mlat.dj_multilateration(R2, d)
		Q_pml[j,:]  = mlat.PML(R2, d)


	# model = mlat.ProbabilisticMultilateration()
	# model.sampling(R, d, sigma=noise_level, theta=100, max_treedepth=12, adapt_delta=0.9)

	# m = np.mean(Q_lin, axis=0)
	# C = np.cov(Q_lin.T)
	# err[i,0] = multivariate_normal.pdf(q, m, C)
	# m = np.mean(Q_reg, axis=0)
	# C = np.cov(Q_reg.T)
	# err[i,1] = multivariate_normal.pdf(q, m, C)
	# m = np.mean(Q_prob, axis=0)
	# C = np.cov(Q_prob.T)
	# err[i,2] = multivariate_normal.pdf(q, m, C)
	m = np.mean(Q_pml, axis=0)
	C = np.cov(Q_pml.T)
	err[i,0] = multivariate_normal.pdf(q, m, C)
	print('loglikelihood %d: %1.4f'%(i, err[i,0]))
	# m = np.mean(model.Q, axis=0)
	# C = np.cov(model.Q.T)
	# err[i,3] = multivariate_normal.pdf(q, m, C)
pickle.dump(err, open('results/25_03/likelihood/err_circle.pic', 'wb'))
print(err)
print(err.mean(axis=0))