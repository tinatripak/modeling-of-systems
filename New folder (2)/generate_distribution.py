import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')
import warnings
warnings.filterwarnings("ignore")
import random
from create_bins import *

n = 10000

def check_hypothesis(alpha, stat_val, p_value):
    if p_value < alpha:
        print(f'Не можемо прийняти нульову гіпотезу на рівні значемості alpha={alpha}.')
        print('Значення статистики:')
        print('\t- stat_val = %s\n\t- p-value = %s' % (round(stat_val, 5), round(p_value, 5)))
    else:
        print('Можемо прийняти нульову гіпотезу про розподіл данних з заданим параметром.')
        print('Значення статистики:')
        print('\t- stat_val = %s\n\t- p-value = %s' % (round(stat_val, 5), round(p_value, 5)))

def exp_cdf(x, l):
    return 1 - np.exp(-l*x) 

def normal_pdf(x, mu, sigma):
    return (1/(sigma*np.sqrt(2*np.pi)))*np.exp(-np.power((x-mu)/sigma, 2)/2) 

def uniform_pdf(x, a, b):
    return (1/(b-a))*((x >= a) & (x <= b)) 

#1
lambda_val = 3.5
epsilon_uniform = np.random.uniform(low=0, high=1, size=n)

print('M(epsilon) = %s\nD(epsilon) = %s' % (epsilon_uniform.mean(), epsilon_uniform.std(ddof=1)**2))

x_exp = -np.log(epsilon_uniform) / lambda_val

fig, ax = plt.subplots(1,1, figsize=(15,6))
sns.distplot(x_exp, ax=ax, color='red', label=f'$\lambda = {lambda_val}$')
ax.set_xlabel(u'Згенеровані дані')
ax.set_ylabel(u'Частота')
ax.set_title(u'Гістограма згенерованого експоненціального розподілу')
ax.legend()
plt.show()

print('M(x) = %s\nstd(x) = %s\nD(x) = %s' % (x_exp.mean(), x_exp.std(ddof=1), x_exp.std(ddof=1)**2))

observed_freq, expected_freq = create_bins_expon(x_exp, 1/((x_exp.mean() + x_exp.std(ddof=1)) / 2))
stat_val, p_value = stats.chisquare(list(observed_freq.values()), list(expected_freq.values()), ddof=1)
alpha = 0.05

check_hypothesis(alpha, stat_val, p_value)

#2
a_val = 0
sigma = 1
epsilon_uniform = np.random.uniform(low=0, high=1, size=(n, 12))

print('M(epsilon) = %s\nD(epsilon) = %s' % (epsilon_uniform.mean(), epsilon_uniform.std(ddof=1)**2))

x_normal = sigma * (epsilon_uniform.sum(axis=1) - 6) + a_val

fig, ax = plt.subplots(1,1, figsize=(15,6))
sns.distplot(x_normal, ax=ax, color='red', label=f'$\mu = {a_val}$, $\sigma = {sigma}$')
ax.set_xlabel(u'Згенеровані дані')
ax.set_ylabel(u'Частота')
ax.set_title(u'Гістограма згенерованого нормального розподілу')
ax.legend()
plt.show()

print('M(x) = %s\nstd(x) = %s\nD(x) = %s' % (x_normal.mean(), x_normal.std(ddof=1), x_normal.std(ddof=1)**2))

observed_freq, expected_freq = create_bins_norm(x_normal, x_normal.mean(), x_normal.std(ddof=1))
stat_val, p_value = stats.chisquare(list(observed_freq.values()), list(expected_freq.values()), ddof=2)
alpha = 0.05

check_hypothesis(alpha, stat_val, p_value)

# 3
z_0 = random.random()
z = z_0
a = 5 ** 13
c = 2 ** 31
x_uniform = []

for i in range(n):
    x = z / c
    x_uniform.append(x)
    z = (a * z) % c
    
x_uniform = np.array(x_uniform)
fig, ax = plt.subplots(1,1, figsize=(15,6))
sns.distplot(x_uniform, ax=ax, color='red', label=f'z_0 = {z_0}, a =  5 ** 13, c = 2 ** 31')
ax.set_xlabel(u'Згенеровані дані')
ax.set_ylabel(u'Частота')
ax.set_title(u'Гістограма згенерованого рівномірного розподілу')
ax.legend()
plt.show()

print('M(epsilon) = %s\nD(epsilon) = %s' % (x_uniform.mean(), x_uniform.std(ddof=1)**2))
b_obs = x_uniform.mean() + np.sqrt(3)*x_uniform.std(ddof=1)
a_obs = 2*x_uniform.mean() - b_obs
print(f'a_obs = {round(a_obs, 5)}, b_obs = {round(b_obs, 5)}')

b = (x.mean() + np.sqrt(3)*x.std(ddof=1))
a = 2*x.mean() - b
observed_freq, expected_freq = create_bins_uniform(x_uniform, a, b)
stat_val, p_value = stats.chisquare(list(observed_freq.values()), list(expected_freq.values()), ddof=2)
alpha = 0.05

check_hypothesis(alpha, stat_val, p_value)