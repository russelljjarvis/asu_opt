FROM scidash/neuron-mpi-neuroml

USER root

RUN pip install git+https://github.com/rgerkin/rickpy
RUN pip install git+https://github.com/scidash/neuronunit@dev --process-dependency-links
RUN pip install git+https://github.com/soravux/scoop
RUN pip install git+https://github.com/DEAP/deap



#RUN echo "hack clean build this small fraction"
#RUN echo $USER 

USER root

WORKDIR /home/jovyan/git
RUN git clone https://github.com/rgerkin/IzhikevichModel.git

WORKDIR /home/jovyan/git
RUN git clone https://github.com/russelljjarvis/sciunitopt.git
WORKDIR /home/jovyan/git/sciunitopt

RUN cp -r $HOME/git/IzhikevichModel/* .

#I prefer to have password less sudo since it permits me 
#to quickly and easily modify the system interactively post dockerbuild.

RUN apt-get update \
      && apt-get install -y sudo \
      && rm -rf /var/lib/apt/lists/*
RUN echo "jovyan ALL=NOPASSWD: ALL" >> /etc/sudoers

RUN chown -R jovyan $HOME

USER $NB_USER

RUN nrniv
RUN python -c "import neuron; import sciunit; import neuronunit"
RUN nrnivmodl 
RUN python -c "import scoop; import deap"


WORKDIR /home/jovyan/git/sciunitopt

ENTRYPOINT python -i nsga2.py
#uncomment below to test with scoop
#ENTRYPOINT python -m scoop nsga2.py
