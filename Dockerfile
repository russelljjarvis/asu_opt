#FROM scidash/neuron-mpi-neuroml
FROM scidash/neuronunit-scoop-deap

#USER root
#RUN pip install git+https://github.com/rgerkin/rickpy
#RUN pip install git+https://github.com/scidash/neuronunit@dev --process-dependency-links
#RUN pip install git+https://github.com/soravux/scoop
#RUN pip install git+https://github.com/DEAP/deap
#RUN echo "hack clean build this small fraction"
#/home/jovyan/work/scipyopt/

USER root



WORKDIR /home/jovyan/work/git
RUN git clone https://github.com/rgerkin/IzhikevichModel.git

WORKDIR /home/jovyan/work/git
RUN git clone https://github.com/russelljjarvis/sciunitopt.git
WORKDIR /home/jovyan/git/sciunitopt

WORKDIR /home/jovyan/work/git
RUN pip install git+https://github.com/aarongarrett/inspyred

WORKDIR /home/jovyan/work/git
RUN pip install git+https://github.com/AllenInstitute/AllenSDK@py34_rgerkin


#https://github.com/AllenInstitute/AllenSDK/tree/py34_rgerkin


RUN cp -r $HOME/work/git/IzhikevichModel/* .

#I prefer to have password less sudo since it permits me 
#to quickly and easily modify the system interactively post dockerbuild.

RUN apt-get update \
      && apt-get install -y sudo \
      && rm -rf /var/lib/apt/lists/*
RUN echo "jovyan ALL=NOPASSWD: ALL" >> /etc/sudoers


#This is probably a nasty hack and a violation of the idea behind 
#scipy-stacks, but I just trying to make stuff work quickly.

RUN conda install -y matplotlib 

RUN pip install pyneuroml

RUN chown -R jovyan $HOME

USER $NB_USER


#Check if anything broke
RUN nrniv
RUN python -c "import neuron; import sciunit; import neuronunit"
RUN nrnivmodl 
RUN python -c "import scoop; import deap"


WORKDIR /home/jovyan/work/git/sciunitopt

# Wow ipython will not work because of matplotlib problem. Yet Jupyter notebooks work. What is wrong

#does not work: ENTRYPOINT ipython -i simple.py


#ENTRYPOINT python -i simple.py

#uncomment below to test nsga or to test with scoop

#ENTRYPOINT python -i nsga2.py

#ENTRYPOINT python -m scoop nsga2.py
