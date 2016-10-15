import pdb
import numpy as np

import random
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




def sobf(ff):
  '''
  sciunit optimize via brute force.
  takes a function as an input returns the coordinates of an optima. 
  '''
  x_best = None
  y_best = -np.inf
  for x in np.linspace(-170,170,10000):
    y = sciunitjudge(f,x)
    if y > y_best:
      y_best = y
      x_best = x
  return x_best,y_best

def brute_force_optimize(ff):
    '''
    solve a trivial parabola by brute force
    plot the function to verify the maxima
    '''
    xx=np.linspace(-170,170,10000)
    outf=np.array([ ff(float(i)) for i in xx ])
    optima_bf=outf[np.where(outf==np.max(outf))][0]
    print('maxima of the curve via brute force:', optima_bf)
    import matplotlib
    matplotlib.use('agg')
    import matplotlib.pyplot as plt
    plt.plot(xx,outf)
    plt.savefig('simple_function.png')
    return optima_bf


class model():
    '''
    A place holder class, not the real thing
    '''
    def __init__(self):
        self.param_values=None

	

OBJ_SIZE = 1 #single weighted objective function.
NDIM = 1 #single dimensional optimization problem


#def ff(xx):
#    return 3-(xx-2)**2

def FF(xx): #hack make this a global scope variable
    return 3-(xx-2)**2




def sciunit_optimize(ff=FF,range_of_values=None,seed=None):
    toolbox = base.Toolbox()
    creator.create("FitnessMax", base.Fitness, weights=(-1.0,))#Final comma here, important, not a typo, must be a tuple type.
    creator.create("Individual", array.array, typecode='d', fitness=creator.FitnessMax)

    class Individual(list):
        def __init__(self, *args):
            list.__init__(self, *args)
            self.stored_x=None
            self.stored_f_x=None
            self.sciunitscore=None
        '''
        This object is used as one unit of chromosome or allele by DEAP.
        '''
        
    def error_surface(pop,gen,ff=FF):
        '''
        solve a trivial parabola by brute force
        plot the function to verify the maxima
        '''
        xx=np.linspace(-170,170,10000)
        outf=np.array([ ff(float(i)) for i in xx ])
        optima_bf=outf[np.where(outf==np.max(outf))][0]
        print('maxima of the curve via brute force:', optima_bf)
        import matplotlib
        matplotlib.use('agg')
        import matplotlib.pyplot as plt
        plt.hold(True)
        plt.plot(xx,outf)
        for ind in pop:
           #pdb.set_trace()
           plt.scatter(ind[0],ind.sciunitscore)
        plt.hold(False)
        plt.savefig('simple_function'+str(gen)+'.png')
        #return optima_bf, xx, outf



    def uniform(low, up, size=None):
        '''
        This is the PRNG distribution that defines the initial
        allele population
        '''
        try:
            return [random.uniform(a, b) for a, b in zip(low, up)]
        except TypeError:
            return [random.uniform(a, b) for a, b in zip([low] * size, [up] * size)]

    range_of_values=np.linspace(-170,170,10000)
    BOUND_LOW=np.min(range_of_values)
    BOUND_UP=np.max(range_of_values)


    toolbox.register("map", futures.map)
    toolbox.register("attr_float", uniform, BOUND_LOW, BOUND_UP, NDIM)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr_float)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    def calc_error(individual, ff=FF):
        score=ff(individual[0])    
        individual.sciunitscore=score
        #individual.stored_x=individual[0]
        individual.stored_f_x=None
            
        #print(individual.sciunitscore)
        return abs(0-score)


    def sciunitjudge(individual,ff=FF):#,Previous_best=Previous_best):
        '''
        sciunit_judge is pretending to take the model individual and return the quality of the model f(X).
        ''' 
        assert type(individual[0])==float# protect input.            
        error=calc_error(individual, ff)#Previous_best,ff)
        return error, 

    #pdb.set_trace()
    #individual,ff,previous_best
    toolbox.register("evaluate",sciunitjudge)#,individual,ff,previous_best)

    toolbox.register("mate", tools.cxSimulatedBinaryBounded, low=BOUND_LOW, up=BOUND_UP, eta=20.0)
    toolbox.register("mutate", tools.mutPolynomialBounded, low=BOUND_LOW, up=BOUND_UP, eta=20.0, indpb=1.0/NDIM)
    toolbox.register("select", tools.selNSGA2)
    seed=1
    random.seed(seed)
    NGEN = 105#250
    #Warning, the algorithm below is sensitive to certain muttiples in the population size
    #which is denoted by MU.
    #The mutiples of 100 work, many numbers will not work
    #TODO write a proper exception handling method.
    #TODO email the DEAP list about this issue too.
    MU = 12#population size
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
    gen=0
    error_surface(pop,gen,ff=FF)
    
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
        #was this: pop = toolbox.select(pop + offspring, MU)
        pop = toolbox.select(offspring, MU)
        record = stats.compile(pop)
        logbook.record(gen=gen, evals=len(invalid_ind), **record)
        print(logbook.stream)
        error_surface(pop,gen,ff=FF)
           #(best_params, best_score, model)
    return (pop[0][0],pop[0].sciunitscore,ff)

  
            

    
class Test:
    def __init__(self,ff,range_of_values):
        self.ff = ff#place holder
        self.range_of_values=range_of_values
    def judge(self,model=None):
        pass # already implemented, returns a score
   
    def optimize(self,model=None):
        # not implemented yet, this is what I need to do with your code

        best_params = None
        best_score = -np.inf
        best_params, best_score, model =sciunit_optimize(self.ff,self.range_of_values,seed=None)
        #best_params, best_score, model = call_to_the_GA(bl, bu,other_ga_params ...)
        return (best_params, best_score, model)
  




if __name__ == "__main__":
    #The following line confuses scoop. It may want sciunit_optimize to be called main        
    
    brute_force_optimize(FF)
    #logbook,y,x=sciunit_optimize(ff,3)
    #best_params, best_score, model = sciunit_optimize(ff,3)
    range_of_values=np.linspace(-170,170,10000)
    t=Test(FF,range_of_values)
    best_params, best_score, model=t.optimize()
    print('pareto front top value in pf hall of fame')
    print('best params',best_params,'best_score',best_score, 'model',model)

