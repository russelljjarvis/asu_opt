
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
#from deap.benchmarks.tools import diversity, convergence, hypervolume
from deap import creator
from deap import tools

#Is inspyred what is crashing out matplotlib???
from inspyred.ec import terminators as term

class deap_capsule:
    '''
    Just a container for hiding implementation, not a very sophisticated one at that.
    '''
    def __init__(self,ff, range_of_values=None,*args):
        self.ff=ff
        self.tb = base.Toolbox()
        self.ngen=None
        self.pop_size=None
        #Warning, the algorithm below is sensitive to certain multiples in the population size
        #which is denoted by MU.
        #The mutiples of 100 work, many numbers will not work
        #TODO write a proper exception handling method.
        #TODO email the DEAP list about this issue too.        
        #TODO refactor MU into pop_size 
                             #self.ff,pop_size,ngen,NDIM=1,OBJ_SIZE=1,self.range_of_values
    def sciunit_optimize(self,ff,pop_size,ngen,NDIM=1,OBJ_SIZE=1,range_of_values=None,seed_in=1):
    #def sciunit_optimize(ff=self.ff,range_of_values=None,seed=None):
        
        self.ngen = ngen#250
        self.pop_size = pop_size#population size
        
        toolbox = base.Toolbox()
        creator.create("FitnessMax", base.Fitness, weights=(-1.0,))#Final comma here, important, not a typo, must be a tuple type.
        creator.create("Individual", array.array, typecode='d', fitness=creator.FitnessMax)

        class Individual(list):
            '''
            When instanced the object from this class is used as one unit of chromosome or allele by DEAP.
            Extends list via polymorphism.
            '''
            def __init__(self, *args):
                list.__init__(self, *args)
                self.stored_x=None
                #self.stored_f_x=None
                self.sciunitscore=None
            
        def error_surface(pop,gen,ff=self.ff):
            '''
            Plot the population on the error surface at generation number gen.
            solve a trivial parabola by brute force
            plot the function to verify the maxima
            Inputs are DEAP GA population of chromosomes and generation number
            no outputs.
            '''
            xx=np.linspace(-170,170,10000)
            outf=np.array([ ff(float(i)) for i in xx ])
            optima_bf=outf[np.where(outf==np.max(outf))][0]
            #print('maxima of the curve via brute force:', optima_bf)
            import matplotlib
            matplotlib.use('agg')
            import matplotlib.pyplot as plt
            plt.hold(True)
            plt.plot(xx,outf)
            scatter_pop=np.array([ind for ind in pop])
            #note the error score is inverted bellow such that it aligns with the error surface.
            scatter_score=np.array([-ind.sciunitscore for ind in pop])
            plt.scatter(scatter_pop,scatter_score)
            plt.hold(False)
            plt.savefig('simple_function'+str(gen)+'.png')



        def uniform(low, up, size=None):
            '''
            This is the PRNG distribution that defines the initial
            allele population
            '''
            try:
                return [random.uniform(a, b) for a, b in zip(low, up)]
            except TypeError:
                return [random.uniform(a, b) for a, b in zip([low] * size, [up] * size)]


        #TODO make range_of_values a parameter of the main class method.
        range_of_values=np.linspace(-170,170,10000)
        BOUND_LOW=np.min(range_of_values)
        BOUND_UP=np.max(range_of_values)


        toolbox.register("map", futures.map)
        toolbox.register("attr_float", uniform, BOUND_LOW, BOUND_UP, NDIM)
        toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr_float)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        def calc_error(individual, ff=self.ff):
            '''
            What follows is a rule for generating error functions that should be generalizable 
            to finding all global maximas.
            '''
            value=ff(individual[0])  
            if value>0:
               score = 1/value #the larger the return value the smaller the error, always.
            elif value==0:
               score = 5/4 # zero needs to still return a nominally large error between 2 and 1/2
            elif value <0:
               score = -(value+1)#the smaller the return value the larger the error, always.
            individual.sciunitscore=score
            return score    


        def sciunitjudge(individual,ff=self.ff):#,Previous_best=Previous_best):
            '''
            sciunit_judge is pretending to take the model individual and return the quality of the model f(X).
            ''' 
            from scoop.futures import scoop
            print(scoop.utils.getHosts())
            print(scoop.utils.cpu_count())
            assert type(individual[0])==float# protect input.            
            error=calc_error(individual, ff)#Previous_best,ff)
            return error, 

        #pdb.set_trace()
        #individual,ff,previous_best
        toolbox.register("evaluate",sciunitjudge)#,individual,ff,previous_best)
        toolbox.register("mate", tools.cxSimulatedBinaryBounded, low=BOUND_LOW, up=BOUND_UP, eta=20.0)
        toolbox.register("mutate", tools.mutPolynomialBounded, low=BOUND_LOW, up=BOUND_UP, eta=20.0, indpb=1.0/NDIM)
        #toolbox.register("select", tools.selNSGA2)

        toolbox.register("select", tools.selTournament, tournsize=3)
        #toolbox.register("select", tools.selBEA, tournsize=3)

        #toolbox.register("select", plot_selector, selector=tools.selBest)
        #toolbox.register("select", tools.selIBEA, selector=selIBEA)
        
        seed=1
        random.seed(seed)

        CXPB = 0.9#cross over probability
        MUTPB= 0.2
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", numpy.mean, axis=0)
        stats.register("std", numpy.std, axis=0)
        stats.register("min", numpy.min, axis=0)
        stats.register("max", numpy.max, axis=0)

        logbook = tools.Logbook()
        logbook.header = "gen", "evals", "std", "min", "avg", "max"


        pop = toolbox.population(n=self.pop_size)
        
        print("Start of evolution")
        
        # Evaluate the entire population
        fitnesses = list(map(toolbox.evaluate, pop))
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit
        print("Evaluated individuals",len(pop))

        # Begin the evolution
        for g in range(self.ngen):
            gen=g#TODO refactor 
            print("-- Generation %i --" % g)
            
            # Select the next generation individuals
            offspring = toolbox.select(pop, len(pop))
            # Clone the selected individuals
            offspring = list(map(toolbox.clone, offspring))
        
            # Apply crossover and mutation on the offspring
            for child1, child2 in zip(offspring[::2], offspring[1::2]):

                # cross two individuals with probability CXPB
                if random.random() < CXPB:
                    toolbox.mate(child1, child2)

                    # fitness values of the children
                    # must be recalculated later
                    del child1.fitness.values
                    del child2.fitness.values

            for mutant in offspring:

                # mutate an individual with probability MUTPB
                if random.random() < MUTPB:
                    toolbox.mutate(mutant)
                    del mutant.fitness.values
        
            # Evaluate the individuals with an invalid fitness
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit
            
            print("  Evaluated %i individuals" % len(invalid_ind))
            
            # The population is entirely replaced by the offspring
            pop[:] = offspring
            error_surface(pop,gen,ff=self.ff)
            # Gather all the fitnesses in one list and print the stats
            fits = [ind.fitness.values[0] for ind in pop]
            #TODO terminate DEAP learning when the population converges to save computation 
            #this will probably involve using term as defined by the import statement above.
            #To be specific using term attributes in a conditional that evaluates to break if true.
            
        record = stats.compile(pop)
        logbook.record(gen=gen, evals=len(invalid_ind), **record)
        print(logbook.stream)
        error_surface(pop,gen,ff=self.ff)
        return (pop[0][0],pop[0].sciunitscore,ff)

