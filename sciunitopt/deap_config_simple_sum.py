
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
#from inspyred.ec import terminators as term

class DeapCapsule:
    '''
    Just a container for hiding implementation, not a very sophisticated one at that.
    '''
    def __init__(self,*args):
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
    def sciunit_optimize(self,test_or_suite,model_path,pop_size,ngen,rov,
                              NDIM=1,OBJ_SIZE=1,seed_in=1):    
        self.ngen = ngen#250
        self.pop_size = pop_size#population size
        self.rov = rov # Range of values

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
                self.sciunitscore=[]#(0,0)
                self.sus0=None
                self.sus1=None
   

        def uniform(low, up, size=None):
            '''
            This is the PRNG distribution that defines the initial
            allele population. Inputs are the maximum and minimal numbers that the PRNG can generate.
            '''
            try:
                return [random.uniform(a, b) for a, b in zip(low, up)]
            except TypeError:
                return [random.uniform(a, b) for a, b in zip([low] * size, [up] * size)]


        #TODO make range_of_values a parameter of the main class method.
        BOUND_LOW=np.min(rov)
        BOUND_UP=np.max(rov)


        toolbox.register("map", futures.map)
        assert NDIM==2
        toolbox.register("attr_float", uniform, BOUND_LOW, BOUND_UP, NDIM)
        toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr_float)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
      

        
        def call2sciunitjudge(individual):#callsciunitjudge
            from neuronunit.models import backends
            #model = ReducedModel(IZHIKEVICH_PATH+str('/LEMS_2007One.xml'),name='vanilla')
            model=backends.NEURONBackend(model_path,
                                         name='V_rest=%dmV' % individual[0], 
                                         attrs={'//izhikevich2007Cell':
                                                {'vr':'%d mV' %individual[0]}
                                            })

                #LEMS_MODEL_PATH,name='vanilla')

            #model = ReducedModel(model_path, 
            #             name='V_rest=%dmV' % individual[0], 
            #             attrs={'//izhikevich2007Cell':
            #                        {'vr':'%d mV' %individual[0]}
            #                   })

            score = test_or_suite.judge(model)
            print("V_rest = %.1f; SortKey = %.3f" % (individual[0],score.sort_key))
            error = -score.sort_key

            #pdb.set_trace()

            #check_error = TestSuite.judge(models=model)#, skip_incapable=True, stop_on_error=True, deep_error=False)
            
            #from sciunit import TestSuite
            #>>> help(TestSuite.judge)
            #Help on function judge in module sciunit:

            #judge(self, models, skip_incapable=True, stop_on_error=True, deep_error=False)


            '''
            sciunit_judge is pretending to take the model individual and return the quality of the model f(X).
            ''' 
            #from scoop.futures import scoop
            #print(scoop.utils.getHosts())
            #print(scoop.utils.cpu_count())
            assert type(individual[0])==float# protect input.            
            assert type(individual[1])==float# protect input.            
            #Linear sum of errors, this is not what I recommend.
            #error=calc_errorf(individual, ff)+calc_errorg(individual, gg)#Previous_best,ff)
            return error, 

        #pdb.set_trace()
        #individual,ff,previous_best
        toolbox.register("evaluate",call2sciunitjudge)#,individual,ff,previous_best)
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
        for gen in range(self.ngen):
            g=gen#TODO refactor 
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
            #error_surface(pop,gen,ff=self.ff)
            # Gather all the fitnesses in one list and print the stats
            fits = [ind.fitness.values[0] for ind in pop]
            #TODO terminate DEAP learning when the population converges to save computation 
            #this will probably involve using term as defined by the import statement above.
            #To be specific using term attributes in a conditional that evaluates to break if true.
            
        record = stats.compile(pop)
        logbook.record(gen=gen, evals=len(invalid_ind), **record)
        print(logbook.stream)
        #error_surface(pop,gen,ff=self.ff)
        return pop#(pop[0][0],pop[0].sus0,ff)

        '''
        Depreciated
        def error_surface(pop,gen,ff=self.ff):
            Plot the population on the error surface at generation number gen.
            solve a trivial parabola by brute force
            plot the function to verify the maxima
            Inputs are DEAP GA population of chromosomes and generation number
            no outputs.
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
            scatter_score=np.array([-ind.sus0 for ind in pop])

            #pdb.set_trace()
            plt.scatter(scatter_pop,scatter_score)
            plt.hold(False)
            plt.savefig('simple_function'+str(gen)+'.png')
        '''  
