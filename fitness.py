import math
import numpy as np

def rastrigin(X):
    return sum([(x ** 2 - 10 * np.cos(2 * math.pi * x) + 10) for x in X])


def sphere(X):
    return sum([(x ** 2) for x in X])


def rosenbrock(X):
    fitness = 0
    for i in range(1, len(X)-1):
        fitness += ((100 * ((X[i + 1] - (X[i]) ** 2) ** 2)) + (X[i] - 1) ** 2)
    return fitness


