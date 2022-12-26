import random
import numpy as np


def exponential_distribution(meanTime):
    res = 0.0
    while res == 0:
        res = random.random()
    return -meanTime * np.log(res)


def uniform_distribution(minTime, maxTime):
    res = 0.0
    while res == 0:
        res = random.random()
    return minTime + res * (maxTime - minTime)


def normal_distribution(meanTime, devTime):
    return meanTime + devTime * random.gauss(0.0, 1.0)

def erlang_distribution(meanTime, n):
    res = 1
    for i in range(n):
        res *= random.random()
    return - np.log(res) / (n * meanTime)

