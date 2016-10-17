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
  
  Not actually used.
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
	Not actually used.
    '''
    def __init__(self):
        self.param_values=None

	






  
            

    
class Test:
    def __init__(self,ff,gg,range_of_values):
        #self.ff = ff#place holder
        self.range_of_values=range_of_values
    def judge(self,model=None):
        pass # already implemented, returns a score
   
    def optimize(self,model=None):
     
        best_params = None
        best_score = None#-np.inf
        #call to the GA.
        #import deap_config
        from deap_config_nsga import deap_capsule
        dc=deap_capsule(ff,gg)
                                          #sciunit_optimize(ff=FF,range_of_values=None,seed_in=1)
                                          #ff,, *args)
        pop_size=12
        ngen=10                                  
        best_params, best_score, model =dc.sciunit_optimize(ff,gg,pop_size,ngen,NDIM=2,OBJ_SIZE=2,self.range_of_values)
        return (best_params, best_score, model)
  




if __name__ == "__main__":
   
    def ff(xx): 
        return 3-(xx-2)**2

    def gg(xx): 
        return 15-(xx-2)**6

    brute_force_optimize(ff)
    #logbook,y,x=sciunit_optimize(ff,3)
    #best_params, best_score, model = sciunit_optimize(ff,3)

    range_of_values=np.linspace(-170,170,10000)
    t=Test(ff,gg,range_of_values)
    best_params, best_score, model=t.optimize()
    print('pareto front top value in pf hall of fame')
    print('best params',best_params,'best_score',best_score, 'model',model)

