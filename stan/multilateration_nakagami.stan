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
    real theta;               // scale for nakagammi likilihood
    real sigma;               // scale for reference points noise
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
}
model {
  q ~ multi_normal(R_mean, diag_matrix(rep_vector(100,dim)));
  for (i in 1:K){
    //priors
    s[i] ~ multi_normal(R[i], diag_matrix(rep_vector(sigma,dim)));
    
    //likilihood
    d[i] ~ dnakagammi(distance(s[i], q), theta);
  }
}