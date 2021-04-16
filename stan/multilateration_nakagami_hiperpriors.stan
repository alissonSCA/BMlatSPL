functions{  
  real nakagammi_log(real x, real m, real omega){
    real p;
    p = (2*pow(m,m))/(tgamma(m)*pow(omega, m));
    p = p*pow(x, 2*m-1);
    //p = p*exp((-m/omega)*pow(x,2));
    return log(p)-(m/omega)*pow(x,2);
  }
  real dnakagammi_log(real x, real d, real theta){
    real m;
    real omega;
    omega = pow(d, 2) + theta;
    m = omega/(2*(omega-pow(d,2)));    
    return nakagammi_log(x, m, omega);
  }  
}
data {
    int<lower=1> K;           // number of reference points
    int<lower=1> dim;         // data in R^{dim}
    vector<lower=0>[K] d;     // estimated distances
    matrix[K, dim] R;         // reference points
    real<lower=0> theta;      // mean scale for nakagammi likilihood
    real<lower=0> sigma;	  // mean scale for reference points noise
}
transformed data {
  vector[dim] R_mean;
  for (j in 1:dim){
    R_mean[j] = 0;
  }
  for (i in 1:K){
    for (j in 1:dim){
      R_mean[j] += R[i,j]/K;
    }
  }
}
parameters {
    vector[dim] q; 
    matrix[K,dim] s;
    real naka_pos;
    real ref_p_pos;
}
model {
  q ~ multi_normal(R_mean, diag_matrix(rep_vector(100,dim)));
  naka_pos ~ gamma(theta/1 + 1, 1);
  ref_p_pos ~ inv_gamma(100-1, 100*sigma);
  for (i in 1:K){
    //priors
    s[i] ~ multi_normal(R[i], diag_matrix(rep_vector(ref_p_pos,dim)));
    
    //likilihood
    d[i] ~ dnakagammi(distance(s[i], q), naka_pos);
  }
}