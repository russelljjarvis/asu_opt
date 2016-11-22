
# coding: utf-8

# In[1]:

def use_dev_packages(dev_packages,path):
    """Prepends items in dev_packages to sys.path, and assumes there are in     
    the user's HOME/Dropbox/dev directory.                                      
    Format for dev_packages items is repo/package.                              
    """
    HOME = os.path.expanduser('~')
    sp = os.path.join(HOME,'Dropbox/python3/lib/python3.4/site-packages')
    if os.path.exists(sp) and sp not in sys.path:
	    sys.path.append(sp)
    for i,package in enumerate(dev_packages):
        if package.split('/')[-1] not in sys.path[len(dev_packages)-i]:
            sys.path.insert(1,os.path.join(HOME,'Dropbox/dev/',package))
            
    print('this method is not effective yet')

import os, sys
path=os.getcwd()
#use_dev_packages(['neuronunit','scidash/sciunit','neuroml/pyNeuroML'],path)




# In[2]:
#get_ipython().magic('matplotlib notebook')
import numpy as np
import matplotlib.pyplot as plt
import quantities as pq
import sciunit
import neuronunit
#from neuronunit import aibs
import pdb

from neuronunit.models.reduced import ReducedModel


# In[3]:

# Replace this with your model path.  
# This example is from https://github.com/OpenSourceBrain/IzhikevichModel.
HOME = os.path.expanduser('~')
LEMS_MODEL_PATH = os.path.join(os.getcwd(),'LEMS_2007One.xml')
model = ReducedModel(LEMS_MODEL_PATH,name='vanilla')
print(LEMS_MODEL_PATH)

# In[21]:

#vm=np.zeros(13)
from neuronunit.capabilities import spike_functions
#waveforms = spike_functions.get_spike_waveforms(vm)
#np.max(waveforms.data,axis=1)


# In[23]:

#np.max(np.array(waveforms),axis=1)


# In[26]:

#np.max(waveforms,axis=1)


# In[4]:

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
#I would like to cache instead of downloading, but I don't know how.
#from allensdk.core.cell_types_cache import CellTypesCache as ctc
#exp_p=ctc.get_ephys_sweeps(dataset_id)

#ctc = CellTypesCache()

ct = CellTypesApi()
experiment_params = ct.get_ephys_sweeps(dataset_id)
cmd = ct.get_ephys_features(dataset_id)
sweep_ids=cmd['rheobase_sweep_id'] #Retrieva all of the sweeps corresponding to finding rheobase.

#found_exp=[]
def get_sp(experiment_params,sweep_ids):
    '''
    get sweep parameter
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
    '''
    if kind == str('rheobase'):
        sp=get_sp(experiment_params,sweep_ids)
        value = sp['stimulus_absolute_amplitude']
        value = np.round(value,2) # Round to nearest hundredth of a pA.
        value *= pq.pA # Apply units.  
        return {'value': value}              
              

observation=get_value_dict(experiment_params,sweep_ids)


tests += [nu_tests.RheobaseTest(observation=observation)]
    
test_class_params = [(nu_tests.InputResistanceTest,None),
                     (nu_tests.TimeConstantTest,None),
                     (nu_tests.CapacitanceTest,None),
                     (nu_tests.RestingPotentialTest,None),
                     (nu_tests.InjectedCurrentAPWidthTest,None),
                     (nu_tests.InjectedCurrentAPAmplitudeTest,None),
                     (nu_tests.InjectedCurrentAPThresholdTest,None)]

for cls,params in test_class_params:
    observation = cls.neuroelectro_summary_observation(neuron)
    tests += [cls(observation,params=params)]
    
def update_amplitude(test,tests,score):
    rheobase = score.prediction['value']
    for i in [3,4,5]:
        tests[i].params['injected_square_current']['amplitude'] = rheobase*1.01 # Set current injection to just suprathreshold
    
hooks = {tests[0]:{'f':update_amplitude}}
suite = sciunit.TestSuite("vm_suite",tests,hooks=hooks)


# In[5]:

model = ReducedModel(LEMS_MODEL_PATH,name='vanilla')
suite.judge(model)


# In[9]:

test = nu_tests.TimeConstantTest


# In[5]:

models = []
for vr in np.linspace(-75,-50,6):
    model = ReducedModel(LEMS_MODEL_PATH, 
                         name='V_rest=%dmV' % vr, 
                         attrs={'//izhikevich2007Cell':
                                    {'vr':'%d mV' % vr}
                               })
    #model.skip_run = True
    models.append(model)
score_matrix = suite.judge(models, verbose=False)
score_matrix.show_mean = True
score_matrix.sortable = True
score_matrix


# In[20]:

from neo.core import AnalogSignal
x = AnalogSignal([1,2,3],units='mV',sampling_period=0.001*pq.s)
np.array(x)


# In[10]:

import matplotlib as mpl
mpl.rcParams['font.size'] = 20
vm = score_matrix[tests[3]][4].related_data['vm'].rescale('mV') # Plot the rheobase current (test 3) 
                                                                # from v_rest = -55 mV (model 4)
ax = plt.gca()
ax.plot(vm.times,vm)
y_min = float(vm.min()-5.0*pq.mV)
y_max = float(vm.max()+5.0*pq.mV)
ax.set_xlim(0,1.6)
ax.set_ylim(y_min,y_max)
ax.set_xlabel('Time (s)',size=24)
ax.set_ylabel('Vm (mV)',size=24);
plt.tight_layout()


# In[6]:

"""
for a in np.linspace(0.015,0.045,2):
    for b in np.linspace(-3.5,-0.5,2):
        for C in np.linspace(50,150,3):
            for k in np.linspace(0.4,1.0,3):
                model = ReducedModel(LEMS_MODEL_PATH, 
                             name='a=%.3fperms_b=%.1fnS_C=%dpF_k=%.2f' % (a,b,C,k), 
                             attrs={'//izhikevich2007Cell':
                                        {'b':'%.1f nS' % b,
                                         'a':'%.3f per_ms' % a,
                                         'C':'%d pF' % C,
                                         'k':'%.2f nS_per_mV' % k,
                                         'vr':'-68 mV',
                                         'vpeak':'45 mV'}
                                   })
                #model.skip_run = True
                models3.append(model)
score_matrix3 = suite.judge(models3, verbose=False)
score_matrix3.show_mean = True
score_matrix3.sortable = True
score_matrix3
""";


# In[7]:

"""
models2 = []
for i,a in enumerate(np.linspace(0.015,0.045,7)):
    for j,b in enumerate(np.linspace(-3.5,-0.5,7)):
        model = ReducedModel(LEMS_MODEL_PATH, 
                     name='a=%.3fperms_b=%.1fnS' % (a,b), 
                     attrs={'//izhikevich2007Cell':
                                {'b':'%.1f nS' % b,
                                 'a':'%.3f per_ms' % a,
                                 'C':'150 pF',
                                 'k':'0.70 nS_per_mV',
                                 'vr':'-68 mV',
                                 'vpeak':'45 mV'}
                           })
        #model.skip_run = True
        models2.append(model)
score_matrix2 = suite.judge(models2, verbose=False)
score_matrix2.show_mean = True
score_matrix2.sortable = True
score_matrix2
""";


# In[8]:

"""
import matplotlib as mpl
mpl.rcParams['font.size'] = 18
heatmap = np.zeros((7,7))
for i,a in enumerate(np.linspace(0.015,0.045,7)):
    for j,b in enumerate(np.linspace(-3.5,-0.5,7)):
        for model in score_matrix2.models:
            if model.name == 'a=%.3fperms_b=%.1fnS' % (a,b):
                heatmap[i,j] = 20*(score_matrix2[model].mean() - 0.8070)+0.8070#[tests[0]].score
#heatmap[2,0] = np.nan
plt.pcolor(heatmap,cmap='magma')
plt.yticks(np.arange(7)+0.5,np.linspace(0.015,0.045,7))
plt.ylabel('Izhikevich Parameter $a$')
plt.xticks(np.arange(7)+0.5,np.linspace(-3.5,-0.5,7))
plt.xlabel('Izhikevich Parameter $b$')
cbar = plt.colorbar()
cbar.set_label('Mean Test Score',size=15)
cbar.ax.tick_params(labelsize=15) 
plt.tight_layout()
np.save('heatmap',heatmap)
""";


# In[12]:

"""
from neuronunit.tests.dynamics import TFRTypeTest,BurstinessTest

is_bursty = BurstinessTest(observation={'cv_mean':1.5, 'cv_std':1.0})
score_matrix2 = is_bursty.judge(models)
score_matrix2
""";


# In[13]:

"""
#rickpy.refresh_objects(locals(),modules=None)
rickpy.refresh_objects(locals().copy(),modules=['sciunit','neuronunit'])
isinstance(tests[0],sciunit.Test) # Should print True if successful
""";

