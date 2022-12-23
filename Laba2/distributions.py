import random
import numpy as np


def exponential_distribution(meanTime):
    res = 0.0
    while res == 0:
        res = random.random()
    res = -meanTime * np.log(res)
    return res


def uniform_distribution(minTime, maxTime): 
    res = 0.0
    while res == 0:
        res = random.random()
    res = minTime + res * (maxTime - minTime)
    return res


def normal_distribution(meanTime, timeDeviation):
    return meanTime + timeDeviation * random.gauss(0.0, 1.0)
