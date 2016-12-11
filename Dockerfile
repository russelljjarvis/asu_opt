#author Russell Jarvis rjjarvis@asu.edu
#author Rick Gerkin rgerkin@asu.edu

FROM scidash/neuron-mpi-neuroml

RUN pip install neo
RUN pip install elephant
RUN pip install bs4
RUN pip install quantities
RUN pip install execnet
RUN pip install git+https://github.com/soravux/scoop
RUN pip install git+https://github.com/DEAP/deap
RUN pip install git+https://github.com/rgerkin/rickpy
RUN pip install git+https://github.com/NeuroML/pyNeuroML --process-dependency-links
#Install rgerkin version of AllenSDK
RUN pip install git+https://github.com/rgerkin/AllenSDK@python3.5 --process-dependency-links
#RUN pip install git+https://github.com/python-quantities/python-quantities
RUN python -c "import pyneuroml"

RUN conda install -y pyqt
#RUN conda install -y matplotlib 

RUN mkdir $HOME/work/scidash
ENV WORK_HOME $HOME/work/scidash

RUN git clone -b dev https://github.com/scidash/sciunit.git $WORK_HOME/sciunit
ENV PYTHONPATH=$PYTHONPATH:$WORK_HOME/sciunit
RUN python -c "import sciunit"

RUN git clone -b dev https://github.com/scidash/neuronunit.git $WORK_HOME/neuronunit
ENV PYTHONPATH=$PYTHONPATH:$WORK_HOME/neuronunit
RUN python -c "import neuronunit"
RUN python -c "from neuronunit.models.reduced import ReducedModel"
RUN python -c "import quantities"
RUN python -c "import neuron"
RUN python -c "import pyneuroml"
RUN nrnivmodl 
RUN python -c "import scoop"
RUN python -c "import deap"
RUN nrniv

#The following are convenience aliases
RUN echo 'alias nb="jupyter-notebook --ip=* --no-browser"' >> ~/.bashrc
RUN echo 'alias mnt="cd /home/mnt"' >> ~/.bashrc
RUN echo 'alias erc="emacs ~/.bashrc"' >> ~/.bashrc
RUN echo 'alias src="source ~/.bashrc"' >> ~/.bashrc
RUN echo 'alias egg="cd /opt/conda/lib/python3.5/site-packages/"' >> ~/.bashrc 
RUN echo 'alias nu="cd /home/jovyan/work/scidash/neuronunit"' >> ~/.bashrc
RUN echo 'alias model="cd /work/scidash/neuronunit/neuronunit/models"' >> ~/.bashrc
RUN echo 'alias sciunit="cd /work/scidash/sciunit"' >> ~/.bashrc
RUN echo 'alias nu="python -c "from neuronunit.models.reduced import ReducedModel""'


WORKDIR /home/mnt
RUN pip install execnet

#WORKDIR /home/jovyan/mnt/sciunitopt
#ENTRYPOINT python -i /home/jovyan/mnt/sciunitopt/AIBS.py 






