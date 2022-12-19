def normilize_bins_expon(obs_freq, exp_freq):
    assert len(obs_freq) > 2 or len(exp_freq) > 2
    for i in sorted(obs_freq.keys(), reverse=True)[:-1]:
        if obs_freq[i] <= 5 or exp_freq[i] <= 5:
            obs_freq[i-1] += obs_freq[i]
            exp_freq[i-1] += exp_freq[i]
            del obs_freq[i], exp_freq[i]
            
    return obs_freq, exp_freq

def normilize_bins_norm(obs_freq, exp_freq):
    assert len(obs_freq) > 2 or len(exp_freq) > 2
        
    for i in sorted(obs_freq.keys(), reverse=True)[:-1]:
        if obs_freq[i] <= 5 or exp_freq[i] <= 5:
            obs_freq[i-1] += obs_freq[i]
            exp_freq[i-1] += exp_freq[i]
            del obs_freq[i], exp_freq[i]
    
    for i in sorted(obs_freq.keys())[:-1]:
        if obs_freq[i] <= 5 or exp_freq[i] <= 5:
            j = 1
            while not i+j in obs_freq:
                j += 1
            obs_freq[i+j] += obs_freq[i]
            exp_freq[i+j] += exp_freq[i]
            del obs_freq[i], exp_freq[i]
    
    return obs_freq, exp_freq


def normilize_bins_uniform(obs_freq, exp_freq):
    assert len(obs_freq) > 2 or len(exp_freq) > 2
        
    for i in sorted(obs_freq.keys(), reverse=True)[:-1]:
        if obs_freq[i] <= 5 or exp_freq[i] <= 5:
            obs_freq[i-1] += obs_freq[i]
            exp_freq[i-1] += exp_freq[i]
            del obs_freq[i], exp_freq[i]
    
    for i in sorted(obs_freq.keys())[:-1]:
        if obs_freq[i] <= 5 or exp_freq[i] <= 5:
            j = 1
            while not i+j in obs_freq:
                j += 1
            obs_freq[i+j] += obs_freq[i]
            exp_freq[i+j] += exp_freq[i]
            del obs_freq[i], exp_freq[i]
    
    return obs_freq, exp_freq