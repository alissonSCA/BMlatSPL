import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pickle
sns.set_theme(style="dark")

dataset = pickle.load(open('./dataset/nl_0_K_6_RD_10.pic', 'rb'))[0]

q = dataset['q']
R = dataset['R']

x0 = R[:,0]
x1 = R[:,1]

data = {'x_0':x0, 'x_1':x1}

g = sns.jointplot(data=data, x='x_0', y='x_1')
plt.show()