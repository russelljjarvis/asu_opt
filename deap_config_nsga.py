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



#OBJ_SIZE = 1 #single weighted objective function.
#NDIM = 1 #single dimensional optimization problem

class deap_capsule:
    '''
    Just a container for hiding implementation, not a very sophisticated one at that.
    '''
    def __init__(self,ff,gg,range_of_values=None,*args):
        self.ff=ff
        self.gg=gg # a second dummy function to demonstrate multi objective.
        self.tb = base.Toolbox()
        self.ngen=None
        self.pop_size=None


    def sciunit_optimize(self,ff,gg,pop_size,ngen,NDIM=2,OBJ_SIZE=2,range_of_values=None,seed_in=1):
        self.ngen = ngen#250
        #Warning, the algorithm below is sensitive to certain muttiples in the population size
        #which is denoted by MU.
        #The mutiples of 100 work, many numbers will not work
        #TODO write a proper exception handling method.
        #TODO email the DEAP list about this issue too.        
        #TODO refactor MU into pop_size 
        self.pop_size=pop_size#population size
        '''
        range_of_values is not implemented yet, but easily implemented.
        '''
        toolbox = base.Toolbox()
        creator.create("FitnessMax", base.Fitness, weights=(-1.0,-1.0,))#Final comma here, important, not a typo, must be a tuple type.

        creator.create("Individual", array.array, typecode='d', fitness=creator.FitnessMax)

        class Individual(list):
            '''
            This object is used as one unit of chromosome or allele by DEAP.
            '''
            def __init__(self, *args):
                list.__init__(self, *args)
                #self.stored_x=None
                #self.sciunitscore=[0 for i in range(0,2)]
                #SUS== sciunitscore.
                #cannot make the list type contain a nested list.
                #use dictionary type as workaround.
                
                self.sus0=None
                self.sus1=None 
            
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
            scatter_pop=np.array([ind[0] for ind in pop])
            #note the error score is inverted bellow such that it aligns with the error surface.
            scatter_score=np.array([-ind.sciunitscore[0] for ind in pop])
            plt.scatter(scatter_pop,scatter_score)
            plt.hold(False)
            plt.savefig('simple_function'+str(gen)+'.png')




        def uniform(low, up, size=None):
            assert size==2
            '''
            This is the PRNG distribution that defines the initial
            allele population. Inputs are the maximum and minimal numbers that the PRNG can generate.
            '''
            try:
                return [random.uniform(a, b) for a, b in zip(low, up)]
            except TypeError:
                return [random.uniform(a, b) for a, b in zip([low] * size, [up] * size)]

        range_of_values=np.linspace(-170,170,10000)
        BOUND_LOW=np.min(range_of_values)
        BOUND_UP=np.max(range_of_values)


        toolbox.register("attr_float", uniform, BOUND_LOW, BOUND_UP, NDIM)
        toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr_float)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)


        def calc_errorf(individual, ff=self.ff):
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

            #individual.sus0=score
            #pdb.set_trace()
            individual.sciunitscore[0]=score
            
            #individual.stored_f_x=None                
            return score        

        def calc_errorg(individual, gg=self.gg):
            '''
            What follows is a rule for generating error functions that should be generalizable 
            to finding all global maximas.
            '''
            value=gg(individual[1])  
            if value>0:
               score = 1/value #the larger the return value the smaller the error, always.
            elif value==0:
               score = 5/4 # zero needs to still return a nominally large error between 2 and 1/2
            elif value <0:
               score = -(value+1)#the smaller the return value the larger the error, always.
            #individual.sus1 =score
            individual.sciunitscore[1]=score

            return score  




        def sciunitjudge(individual,ff=self.ff,gg=self.gg):#,Previous_best=Previous_best):
            '''
            sciunit_judge is pretending to take the model individual and return the quality of the model f(X).
            ''' 
            assert type(individual[0])==float# protect input.            
            assert type(individual[1])==float# protect input.            
            #In the NSGA version the error returned from objective function
            #Needs to be a list or a tuple.
            #pdb.set_trace()

            print( calc_errorf(individual, ff),calc_errorg(individual, gg) )
            error=( calc_errorf(individual, ff),calc_errorg(individual, gg) )
            return error
        toolbox.register("evaluate",sciunitjudge)#,individual,ff,previous_best)

        toolbox.register("mate", tools.cxSimulatedBinaryBounded, low=BOUND_LOW, up=BOUND_UP, eta=20.0)
        toolbox.register("mutate", tools.mutPolynomialBounded, low=BOUND_LOW, up=BOUND_UP, eta=20.0, indpb=1.0/NDIM)
        toolbox.register("select", tools.selNSGA2)

        random.seed(seed_in)
       
        CXPB = 0.9#cross over probability

        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", numpy.mean, axis=0)
        stats.register("std", numpy.std, axis=0)
        stats.register("min", numpy.min, axis=0)
        stats.register("max", numpy.max, axis=0)

        logbook = tools.Logbook()
        logbook.header = "gen", "evals", "std", "min", "avg", "max"

        pop = toolbox.population(n=self.pop_size)
        

        #Its really stupid that a data type should have to be defined inside the container, after
        #Its instanced, but I don't understand enough OOPython to know why, and or how to fix it.        
        #blah=[ ind.sciunitscore={} for ind in pop ]
        #ind.sciunitscore={} 


        for ind in pop:
            ind.sciunitscore={} 
        

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
        error_surface(pop,gen,ff=self.ff)
        
        #record = stats.compile(pop)
        #logbook.record(gen=0, evals=len(invalid_ind), **record)
        #print(logbook.stream)

        stats_fit = tools.Statistics(key=lambda ind: ind.fitness.values)
        stats_size = tools.Statistics(key=len)
        mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
        record = mstats.compile(pop)

        # Begin the generational process
        for gen in range(1,self.ngen):
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
            pop = toolbox.select(offspring, self.pop_size)
            
            #logbook.record(gen=gen, evals=len(invalid_ind), **record)
            #print(logbook.stream)
            error_surface(pop,gen,ff=self.ff)
               #(best_params, best_score, model)
        print(record)
        pdb.set_trace()       
        return (pop[0][0],pop[0].sciunitscore[0],ff)

