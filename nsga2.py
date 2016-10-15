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

class model():
    '''
    A place holder class, not the real thing
	Not actually used.
    '''
    def __init__(self):
        self.param_values=None

    
class Test:
   
    def __init__(self,ff,range_of_values):
        self.ff = ff#place holder
        self.range_of_values=range_of_values

    def judge(self,model=None):
        pass # already implemented, returns a score
   
    def optimize(self):     
        best_params = None
        best_score = None#-np.inf
        #call to the GA.
        from deap_config import deap_capsule
        model=self.ff
        dc=deap_capsule(model)
        dc.tb.register("map", futures.map)
        best_params, best_score, model =dc.sciunit_optimize(self.ff,self.range_of_values)
        return (best_params, best_score, model)
  

if __name__ == "__main__":
   
    def ff(xx): 
        return 3-(xx-2)**2

   
    range_of_values=np.linspace(-170,170,10000)
    t=Test(ff,range_of_values)
    best_params, best_score, model=t.optimize()
    print('pareto front top value in pf hall of fame')
    print('best params',best_params,'best_score',best_score, 'model',model)

