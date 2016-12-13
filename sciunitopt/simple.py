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

import os, sys
#get_ipython().magic('matplotlib notebook')
import numpy as np
import matplotlib.pyplot as plt
import quantities as pq
import sciunit
import neuronunit
#from neuronunit import aibs
import pickle as pickle
import pdb

from neuronunit.models.reduced import ReducedModel


HOME = os.path.expanduser('~')
LEMS_MODEL_PATH = os.path.join(os.getcwd(),'LEMS_2007One.xml')
model = ReducedModel(LEMS_MODEL_PATH,name='vanilla')

from neuronunit.capabilities import spike_functions
#waveforms = spike_functions.get_spike_waveforms(vm)
#np.max(waveforms.data,axis=1)


#np.max(np.array(waveforms),axis=1)
#np.max(waveforms,axis=1)


import quantities as pq
from neuronunit import tests as nu_tests, neuroelectro
neuron = {'nlex_id': 'nifext_50'} # Layer V pyramidal cell

tests = []

dataset_id = 354190013  # Internal ID that AIBS uses for a particular Scnn1a-Tg2-Cre 
                        # Primary visual area, layer 5 neuron.
#observation = aibs.get_observation(dataset_id,'rheobase')
from allensdk.api.queries.cell_types_api import CellTypesApi
from allensdk.ephys.extract_cell_features import get_square_stim_characteristics,\
                                                 get_sweep_from_nwb
from allensdk.core import nwb_data_set

ct = CellTypesApi()

def get_sp(experiment_params,sweep_ids):
    '''
    get sweep parameter
    TODO: move method into neuronunit/aibs.py, as this is a fix for that file.    
    '''
    sweep_num = None
    for sp in experiment_params:
       for i in sweep_ids:
          if sp['id']==i:
              sweep_num = sp['sweep_number']
              found_sp=sp
              break
    if sweep_num is None:
        found_sp=None          
        raise Exception('Sweep with ID %d not found in dataset with ID %d.' % (sweep_id, dataset_id))
    return found_sp


def get_value_dict(experiment_params,sweep_ids,kind=str('rheobase')):
    '''
    return values
    TODO: move method into neuronunit/aibs.py, as this is a fix for that file.
    '''
    if kind == str('rheobase'):
        sp=get_sp(experiment_params,sweep_ids)
        value = sp['stimulus_absolute_amplitude']
        value = np.round(value,2) # Round to nearest hundredth of a pA.
        value *= pq.pA # Apply units.  
        return {'value': value}              
              


#save some time by pickle loading the content if its available. 
#using allensdk cache would be preferable, but I don't yet understand the syntax.


if os.path.exists(str(os.getcwd())+"/observations.pickle"):
    print('attempting to recover from pickled file')
    with open('observations.pickle', 'rb') as handle:
        observation = pickle.load(handle)

else:
    print('checked path:')
    print(str(os.getcwd())+"/observation.pickle")
    print('no pickled file down loading time intensive')
    experiment_params = ct.get_ephys_sweeps(dataset_id)
    cmd = ct.get_ephys_features(dataset_id)
    sweep_ids=cmd['rheobase_sweep_id'] #Retrieva all of the sweeps corresponding to finding rheobase.
    observation=get_value_dict(experiment_params,sweep_ids)
    with open('observations.pickle', 'wb') as handle:
        pickle.dump(observation, handle)


#Compare differences between Allen Brain derived observations, Neuroelectro derived recordings and 
#Izkevitch model



tests += [nu_tests.RheobaseTest(observation=observation)]
#Edited out below:   
#
                      
test_class_params = [(nu_tests.InputResistanceTest,None),
                     (nu_tests.TimeConstantTest,None),
                     (nu_tests.CapacitanceTest,None)]
                     
                     #,
                     #(nu_tests.RestingPotentialTest,None),   
                     #(nu_tests.InjectedCurrentAPWidthTest,None),
                     #(nu_tests.InjectedCurrentAPAmplitudeTest,None),
                     #(nu_tests.InjectedCurrentAPThresholdTest,None)]


print('neuronunit_generated these tests')
for cls,params in test_class_params:
    print('neuronunit_generated these tests')
    observation = cls.neuroelectro_summary_observation(neuron)
    tests += [cls(observation,params=params)]
    print(observation)
    print(tests)
    print(cls,params)

    
def update_amplitude(test,tests,score):
    rheobase = score.prediction['value']
    #for i in [3,4,5]:
    #    tests[i].params['injected_square_current']['amplitude'] = rheobase*1.01 # Set current injection to just suprathreshold
    
hooks = {tests[0]:{'f':update_amplitude}}


import pdb
print(tests)
print(hooks)
print(dir(sciunit.TestSuite))

test=tests[0]

suite = sciunit.TestSuite("vm_suite",test,hooks=hooks)


# In[5]:
#print('failed here')
#model = ReducedModel(LEMS_MODEL_PATH,name='vanilla')
#suite.judge(model)


# In[9]:

test = nu_tests.TimeConstantTest



 

class Test:
    def __init__(self,range_of_values):
        #self.ff = ff#place holder
        self.range_of_values=range_of_values
    def judge(self,model=None):
        pass # already implemented, returns a score
   
    def optimize(self,model=None):
    
    
        best_params = None
        best_score = None#-np.inf
        #call to the GA.
        from deap_config_simple_sum import deap_capsule
        dc=deap_capsule()
        pop_size=12
        ngen=20                                  
        best_params, best_score, model =dc.sciunit_optimize(tests,hooks,pop_size,ngen,NDIM=2,OBJ_SIZE=2,range_of_values=self.range_of_values)
        return (best_params, best_score, model)

  

if __name__ == "__main__":
   

   
    range_of_values=np.linspace(-170,170,10000)
    t=Test(range_of_values)
    best_params, best_score, model=t.optimize()
    print('pareto front top value in pf hall of fame')
    print('best params',best_params,'best_score',best_score, 'model',model)
    
    
 

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

	
   
    

