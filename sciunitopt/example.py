
# coding: utf-8

# In[1]:

# Replace this with your model path.  
# This example is from https://github.com/OpenSourceBrain/IzhikevichModel.
LEMS_MODEL_PATH = '/Users/rgerkin/Dropbox/dev/osb/IzhikevichModel/NeuroML2/LEMS_WhichModel.xml'


# In[2]:

get_ipython().magic('matplotlib inline')
import os,sys
from pyneuroml import pynml


# In[3]:

results = pynml.run_lems_with_jneuroml(os.path.split(LEMS_MODEL_PATH)[1], 
                             verbose=False, load_saved_data=True, nogui=True, 
                             exec_in_dir=os.path.split(LEMS_MODEL_PATH)[0],
                             plot=True)

