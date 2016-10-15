FROM scidash/neuron-mpi-neuroml

USER root

RUN pip install git+https://github.com/rgerkin/rickpy
RUN pip install git+https://github.com/scidash/neuronunit@dev --process-dependency-links
RUN pip install git+https://github.com/soravux/scoop
RUN pip install git+https://github.com/DEAP/deap
	
USER $NB_USER

RUN nrniv
RUN python -c "import neuron; import sciunit; import neuronunit"
RUN nrnivmodl 
RUN python -c "import scoop; import deap"


WORKDIR /home/docker/git
RUN git clone https://github.com/russelljjarvis/sciunitopt.git
WORKDIR /home/docker/git/sciunitopt
ENTRYPOINT python -m scoop nsga2.py