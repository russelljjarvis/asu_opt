import array
import random
import scoop as scoop
import numpy as np, numpy
import scoop
from math import sqrt
from scoop import futures
from deap import algorithms
from deap import base
from deap import benchmarks
from deap.benchmarks.tools import diversity, convergence, hypervolume
from deap import creator
from deap import tools

toolbox = base.Toolbox()


class Individual(list):
    '''
    This object is used as one unit of chromosome or allele by DEAP.
    '''
    def __init__(self, *args):
        list.__init__(self, *args)
        self.stored_value=None
        self.stored_error=None
        self.sciunitscore=None

creator.create("FitnessMax", base.Fitness, weights=(-1.0,))#Final comma here, important, not a typo, must be a tuple type.
creator.create("Individual", array.array, typecode='d', fitness=creator.FitnessMax)



def uniform(low, up, size=None):
    '''
    This is the PRNG distribution that defines the initial
    allele population
    '''
    try:
        return [random.uniform(a, b) for a, b in zip(low, up)]
    except TypeError:
        return [random.uniform(a, b) for a, b in zip([low] * size, [up] * size)]




toolbox.register("map", futures.map)

toolbox.register("attr_float", uniform, BOUND_LOW, BOUND_UP, NDIM)

toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr_float)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate",sciunitjudge)
toolbox.register("mate", tools.cxSimulatedBinaryBounded, low=BOUND_LOW, up=BOUND_UP, eta=20.0)
toolbox.register("mutate", tools.mutPolynomialBounded, low=BOUND_LOW, up=BOUND_UP, eta=20.0, indpb=1.0/NDIM)
toolbox.register("select", tools.selNSGA2)
