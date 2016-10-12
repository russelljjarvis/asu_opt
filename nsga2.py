
import array
import random
import json

import numpy as np, numpy

from math import sqrt
from scoop import futures
from deap import algorithms
from deap import base
from deap import benchmarks
from deap.benchmarks.tools import diversity, convergence, hypervolume
from deap import creator
from deap import tools

class Individual(list):
    def __init__(self, *args):
        list.__init__(self, *args)
        self.stored_value=None
        self.stored_error=None

creator.create("FitnessMax", base.Fitness, weights=(-1.0,))#Final comma here, important, not a typo, must be list type
creator.create("Individual", array.array, typecode='d', fitness=creator.FitnessMax)

toolbox = base.Toolbox()

BOUND_LOW, BOUND_UP = -70, -40
import pdb
import numpy as np
#pdb.set_trace()    
def ff(xx):
    return 3-(xx-2)**2



LOWER=-70
UPPER=-40
IND_SIZE=1


def brute_force_optimize(ff):
    xx=np.linspace(-70,-40,1000)
    #xvalue=np.linspace(-70,-40,1000)

    outf=np.array([ ff(float(i)) for i in xx ])
    minima_bf=outf[np.where(outf==np.min(outf))][0]
    optima_bf=outf[np.where(outf==np.max(outf))][0]
    xvalue_bf=xx[np.where(outf==np.max(outf))][0]
    print('maxima of the curve via brute force:', optima_bf)
    print('xvalue of the curve via brute force:', xvalue_bf)
 
    print('minima of the curve via brute force:', minima_bf)
    import matplotlib
    matplotlib.use('agg')

    import matplotlib.pyplot as plt
    plt.plot(xx,outf)
    plt.savefig('simple_function.png')
    return optima_bf






def sciunitjudge(individual):
    ev=[ff(float(i)) for i in individual]
    individual.stored_value=np.mean(ev)    
    #define the error function such that error is proportionate to distance from zero.
    total_error=abs(0-np.mean(ev))
    return total_error,

        
OBJ_SIZE = 1 #single weighted objective function.

NDIM = 1

def uniform(low, up, size=None):
    try:
        return [random.uniform(a, b) for a, b in zip(low, up)]
    except TypeError:
        return [random.uniform(a, b) for a, b in zip([low] * size, [up] * size)]

toolbox.register("attr_float", uniform, BOUND_LOW, BOUND_UP, NDIM)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr_float)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate",sciunitjudge)
toolbox.register("mate", tools.cxSimulatedBinaryBounded, low=BOUND_LOW, up=BOUND_UP, eta=20.0)
toolbox.register("mutate", tools.mutPolynomialBounded, low=BOUND_LOW, up=BOUND_UP, eta=20.0, indpb=1.0/NDIM)
toolbox.register("select", tools.selNSGA2)


def main(ff,seed=None):
    brute_force_optimize(ff)
    random.seed(seed)

    NGEN = 5#250
    MU = 100#population size
    CXPB = 0.9#cross over probability

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean, axis=0)
    stats.register("std", numpy.std, axis=0)
    stats.register("min", numpy.min, axis=0)
    stats.register("max", numpy.max, axis=0)
    
    logbook = tools.Logbook()
    logbook.header = "gen", "evals", "std", "min", "avg", "max"
    
    pop = toolbox.population(n=MU)

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    
    for ind, fit in zip(invalid_ind, fitnesses):
        print(ind,fit)
        ind.fitness.values = fit
        print(ind.fitness.values)
    # This is just to assign the crowding distance to the individuals
    # no actual selection is done
    pop = toolbox.select(pop, len(pop))
    
    record = stats.compile(pop)
    logbook.record(gen=0, evals=len(invalid_ind), **record)
    print(logbook.stream)

    # Begin the generational process
    for gen in range(1, NGEN):
        # Vary the population
        offspring = tools.selTournamentDCD(pop, len(pop))
        offspring = [toolbox.clone(ind) for ind in offspring]
        
        for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
            if random.random() <= CXPB:
                toolbox.mate(ind1, ind2)
            
            toolbox.mutate(ind1)
            toolbox.mutate(ind2)
            del ind1.fitness.values, ind2.fitness.values
        
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Select the next generation population
        pop = toolbox.select(pop + offspring, MU)
        record = stats.compile(pop)
        logbook.record(gen=gen, evals=len(invalid_ind), **record)
        print(logbook.stream)

    #print("Final population hypervolume is %f" % hypervolume(pop, [11.0]))

    return pop, logbook

def sciunit_optimize(ff,seed=None):
    #brute_force_optimize(ff)
    random.seed(seed)

    NGEN = 5#250
    MU = 100#population size
    CXPB = 0.9#cross over probability

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean, axis=0)
    stats.register("std", numpy.std, axis=0)
    stats.register("min", numpy.min, axis=0)
    stats.register("max", numpy.max, axis=0)
    
    logbook = tools.Logbook()
    logbook.header = "gen", "evals", "std", "min", "avg", "max"
    
    pop = toolbox.population(n=MU)

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    
    for ind, fit in zip(invalid_ind, fitnesses):
        print(ind,fit)
        ind.fitness.values = fit
        print(ind.fitness.values)
    # This is just to assign the crowding distance to the individuals
    # no actual selection is done
    pop = toolbox.select(pop, len(pop))
    
    record = stats.compile(pop)
    logbook.record(gen=0, evals=len(invalid_ind), **record)
    print(logbook.stream)

    # Begin the generational process
    for gen in range(1, NGEN):
        # Vary the population
        offspring = tools.selTournamentDCD(pop, len(pop))
        offspring = [toolbox.clone(ind) for ind in offspring]
        
        for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
            if random.random() <= CXPB:
                toolbox.mate(ind1, ind2)
            
            toolbox.mutate(ind1)
            toolbox.mutate(ind2)
            del ind1.fitness.values, ind2.fitness.values
        
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Select the next generation population
        pop = toolbox.select(pop + offspring, MU)
        record = stats.compile(pop)
        logbook.record(gen=gen, evals=len(invalid_ind), **record)
        print(logbook.stream)

    #print("Final population hypervolume is %f" % hypervolume(pop, [11.0]))

    #This is analogous to found via optimization:
    #found x coordinate of parabola, ycoodinate of parabola
    return pop[0].stored_value,pop[0]
        
if __name__ == "__main__":
    toolbox.register("map", futures.map)
        
    # with open("pareto_front/zdt1_front.json") as optimal_front_data:
    #     optimal_front = json.load(optimal_front_data)
    # Use 500 of the 1000 points in the json file
    # optimal_front = sorted(optimal_front[i] for i in range(0, len(optimal_front), 2))
    
    #pop, stats = main(ff,3)
    x,y=sciunit_optimize(ff,3)
    #print(stats)
    brute_force_optimize(ff)
    print('pareto front top value in pf hall of fame')
    print(x,y)
    #print(pop)

    # pop.sort(key=lambda x: x.fitness.values)
    
    # print(stats)
    # print("Convergence: ", convergence(pop, optimal_front))
    # print("Diversity: ", diversity(pop, optimal_front[0], optimal_front[-1]))
    
    # import matplotlib.pyplot as plt
    # import numpy
    
    # front = numpy.array([ind.fitness.values for ind in pop])
    # optimal_front = numpy.array(optimal_front)
    # plt.scatter(optimal_front[:,0], optimal_front[:,1], c="r")
    # plt.scatter(front[:,0], front[:,1], c="b")
    # plt.axis("tight")
    # plt.show()
