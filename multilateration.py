import numpy as np
import pystan
from scipy.spatial import distance
from scipy.special import digamma
from scipy.optimize import least_squares
from scipy.stats import nakagami, multivariate_normal
import pickle

def lin_multilateration(R, d):
	r = R[0,:].reshape(1,-1)
	R = R[1:,:]
	K, dim = R.shape
	dr = d[0]*np.ones(K)
	d = d[1:]
	dri = distance.cdist(R, r) 

	A = R - r
	b = np.array([0.5*(np.power(a,2)+np.power(b,2)-np.power(c,2))[0] for a,b,c in zip(dr, dri, d)])

	theta = np.linalg.pinv(A).dot(b)
	return theta + r

def multilateration(R, d):
	K, dim = R.shape
	f = lambda q: np.power(distance.cdist(R, q.reshape(1,-1), 'sqeuclidean') - np.power(d.reshape(-1,1), 2), 2 )[:,0]
	return least_squares(f, np.zeros(dim))['x'].reshape(1,-1)

def PML_obj_func(R, d, q_hat, s):
  d_hat = distance.cdist(R, [q_hat])
  
  value = np.zeros(2)
  for i in np.arange(d.shape[0]):
    factor = (d_hat[i] - d[i])/(d_hat[i]*s[i])
    value[0] = value[0] + (factor * (q_hat[0] - R[i,0]))**2
    value[1] = value[1] + (factor * (q_hat[1] - R[i,1]))**2
  return value.sum()

def PML(R, d, s=None):
	if s == None:
		s = np.ones(d.shape[0])

	f = lambda x: PML_obj_func(R, d, x, s)
	return least_squares(f, R.mean(axis=0))['x'].reshape(1,-1)	

def p_gdFunction(d,q,r):
	m = (q - r)
	m_norm = np.linalg.norm(m, axis=1)
	S = 0
	for mi, mi_norm, di in zip(m, m_norm, d):
		parc = 0
		parc = parc + 2*np.log(di)*mi_norm
		parc = parc - di
		parc = parc - 2*mi_norm*digamma(mi_norm**2)
		parc = parc + mi_norm
		parc = parc - 2*mi_norm*np.log(1/mi_norm)
		S = S + (mi/mi_norm)*(parc)
	A = np.linalg.pinv( np.cov(r.T) )
	return S - A.dot((q - r.mean(axis=0)).T)


def p_multilateration(r, d, q0=None, alpha = 0.01, max_iter=100):
	if (q0 == None):
		q0 = np.zeros(r.shape[1])
	q = q0
	for i in np.arange(max_iter):
		g = p_gdFunction(d, q, r)
		q = q + alpha*g
	return np.array([q])	  	

def monte_carlo_sampler(method, R, d, noise_level, n_samples=1000):
	if method == 'mlat':
		f = lambda R,d: multilateration(R,d)
	elif method == 'lin':
		f = lambda R,d: lin_multilateration(R,d)
	elif method == 'pmlat':
		f = lambda R,d: p_multilateration(R,d)
	elif method == 'pml':
		f = lambda R,d: PML(R,d)

	K, dim = R.shape
	Q = np.zeros([n_samples, dim])
	for i in np.arange(n_samples):
		R2 = R + np.random.normal(0, noise_level,size=[K, dim])
		Q[i,:] = f(R2, d)
	return Q

class BayesianMultilateration:

	def __init__(self, file='./stan/multilateration_nakagami.pic'):
		self.sm = pickle.load(open(file, 'rb'))

	def sampling(self, R, d, theta=200, sigma=1, max_treedepth=10, adapt_delta=0.8):
		K, dim = R.shape
		data = {'K': K, 'dim': dim, 'R':R, 'd':d, 'theta':theta, 'sigma':sigma}
		fit = self.sm.sampling(data=data, iter=1000, chains=4, control=dict(max_treedepth=max_treedepth, adapt_delta=adapt_delta))
		params = fit.extract()

		self.Q = params['q']
		self.R = R
		self.d = d
		self.theta = theta

	def get_mean(self):
	  return np.mean(self.Q, axis=0).reshape(1,-1)

	def likelihood(self, d, q, r, theta = 1e2, f_comp = np.prod):
	  f = lambda di, mi: nakagami.pdf(di, nu=(mi**2 + theta)/(2*theta), 
	                                  scale=np.sqrt(mi**2 + theta) ) 
	  
	  m = distance.cdist([q], r)[0]    
	  return f_comp([f(di, mi) for di, mi in zip(d, m)])  

	def get_mode(self):
		N, dim = self.Q.shape
		p = np.zeros([N,1])
		for i in np.arange(N):
			prior = multivariate_normal.pdf(self.Q[i,:], mean=np.mean(self.R, axis=0), cov=100*np.eye(dim))
			p[i] = prior*self.likelihood(self.d, self.Q[i,:], self.R, theta=self.theta)
		return self.Q[np.argmax(p), :].reshape(1,-1)   	    

	def get_loglikelihood(self, q):
		mu = np.mean(self.Q, axis=0)
		S  = np.cov(self.Q.T)

		return multivariate_normal.logpdf(q, mu, S)
