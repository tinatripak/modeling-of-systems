
import numpy as np
from scipy import stats
from normilize_bins import *

def create_bins_expon(x, l, n_bins=30):
    start = x.min()
    finish = x.max() + 1e-9
    h = (finish - start) / n_bins
    n = x.size
    
    obs_freq = {}
    exp_freq = {}
    
    current = start
    i = 0
    while current <= finish:
        obs_freq[i] = np.sum((x >= current) & (x < (current+h)))
        p_i = np.exp(-l*current) - np.exp(-l*(current+h))
        exp_freq[i] = p_i * n
        i += 1
        current += h

    return normilize_bins_expon(obs_freq, exp_freq)

def create_bins_norm(x, mu, sigma, n_bins=30):
    start = x.min()
    finish = x.max() + 1e-9
    h = (finish - start) / n_bins
    n = x.size

    obs_freq = {}
    exp_freq = {}
    
    current = start
    i = 0
    while current <= finish:
        obs_freq[i] = np.sum((x >= current) & (x < (current+h)))
        p_i = np.abs(stats.norm(mu, sigma).cdf(current) - stats.norm(mu, sigma).cdf(current+h))
        exp_freq[i] = p_i * n
        i += 1
        current += h

    return normilize_bins_norm(obs_freq, exp_freq)

def create_bins_uniform(x, a, b, n_bins=30):
    start = x.min()
    finish = x.max() + 1e-9
    h = (finish - start) / n_bins
    n = x.size
    
    obs_freq = {}
    exp_freq = {}
    
    current = start
    i = 0
    while current <= finish:
        obs_freq[i] = np.sum((x >= current) & (x < (current+h)))
        p_i = np.abs(stats.uniform(a, b).cdf(current) - stats.uniform(a, b).cdf(current+h))
        exp_freq[i] = p_i * n
        i += 1
        current += h
        
    return normilize_bins_uniform(obs_freq, exp_freq)