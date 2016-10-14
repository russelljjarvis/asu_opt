import pdb
import numpy as np




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
    def __init__(self):
        self.param_values=None
    '''
	A place holder class, not the real thing
	'''
	

OBJ_SIZE = 1 #single weighted objective function.
NDIM = 1 #single dimensional optimization problem


def ff(xx):
    return 3-(xx-2)**2


def calc_error(individual, previous_best, ff):
    #model=model(xx)
    score=ff(individual[0])    
    individual.sciunitscore=score

    #score = sciunitjudge(model)
    if score > previous_best:
       #current_best  = score
       best_params = individual
       return (0, score) #return error =0, and current best_score
    else:
       return (abs(previous_best-score), previous_best) # a nominally large error


def sciunitjudge(individual,ff,previous_best):
    '''
    sciunit_judge is pretending to take the model individual and return the quality of the model f(X).
    '''	
    
    assert type(individual[0])==float# protect input.    

    #above is a place holder for below
    #score = self.judge(model)
    
    #individual.stored_value=ev  
    
	#in multidimensional opt problems, extra dimensions are indexible in
	#individual, ie individual[0] is simply DIM==1
    
    #model.param_values = indvidual[0]
    
    (error,previous_best)=calc_error(individual, previous_best,ff)

    #however calculation of the error function must be updated to match ff.
    #ie if it is known that the maxima is significantly greater than 0,
    #differencing the observed chromosome value with 0 (as is done below) will no longer work.

 
    #total_error is the quality of the model f(x)
    return error, 
    #(best_params, best_score, model)
        


def sciunit_optimize(bl,bu,ff,seed=None):
    BOUND_LOW=bl
    BOUND_UP=bu

    random.seed(seed)
    NGEN = 6#250
    #Warning, the algorithm below is sensitive to certain muttiples in the population size
    #which is denoted by MU.
    #The mutiples of 100 work, many numbers will not work
    #TODO write a proper exception handling method.
    #TODO email the DEAP list about this issue too.
    MU = 200#population size
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
    return (pop[0].stored_value,pop[0][0],ff)

    #print("Final population hypervolume is %f" % hypervolume(pop, [11.0]))

    #This is analogous to found via optimization:
    #found x coordinate of parabola, ycoodinate of parabola
    #        best_params, best_score, model
    
class Test:
    def __init__(self,ff):
        self.ff = ff#place holder
   
    def judge(self,model=None):
        pass # already implemented, returns a score
   
    def optimize(self,model=None):
        # not implemented yet, this is what I need to do with your code
        dir()
        pdb.set_trace()
        toolbox.register("map", futures.map)

        best_params = None
        best_score = -np.inf
        BOUND_LOW=np.min(range_of_possible_param_values)
        BOUND_UP=np.max(range_of_possible_param_values)
        import hidden_deap_config  

        #other params to the GA such as number of dimensions, number of
        #generations,
        #population size.
        #mutation rate, cross over rate.
        #NGEN and pop_size will likely need to increase in proportion to
        #the number of dimensions in the optimization problem and
        #how difficult the error surface is.
        best_params, best_score, model =sciunit_optimize(self.ff,seed=None)
        #best_params, best_score, model = call_to_the_GA(bl, bu,other_ga_params ...)
        return (best_params, best_score, model)
  

if __name__ == "__main__":
    #The following line confuses scoop. It may want sciunit_optimize to be called main        
    
    brute_force_optimize(ff)
    #logbook,y,x=sciunit_optimize(ff,3)
    #best_params, best_score, model = sciunit_optimize(ff,3)
    t=Test(ff)
    best_params, best_score, model=t.optimize()

    print('pareto front top value in pf hall of fame')
    print('xcoordinate',x,'ycoordinate',y)

