FROM scidash/neuron-mpi-neuroml

USER root
RUN pip install git+https://github.com/soravux/scoop
RUN pip install git+https://github.com/DEAP/deap
RUN pip install git+https://github.com/rgerkin/rickpy

WORKDIR /home/jovyan/work/scidash/pyNeuroML
RUN pip install git+https://github.com/NeuroML/pyNeuroML --process-dependency-links
RUN pip install neo elephant

WORKDIR /home/jovyan/work/scidash
RUN pip install git+https://github.com/AllenInstitute/AllenSDK@py34_rgerkin --process-dependency-links
#RUN python -c "import sciunit"


#Install some bloat ware temporarily.
#To be deleted in the future.
#stripathy/AIBS_cell_types is just a good test of some of the functionality of packages trying to get working 
#here:
WORKDIR /home/jovyan/work/scidash
RUN git clone https://github.com/stripathy/AIBS_cell_types.git

RUN pip install git+https://github.com/python-quantities/python-quantities
WORKDIR /home/jovyan/work/scidash/pyNeuroML
RUN pip install git+https://github.com/NeuroML/pyNeuroML --process-dependency-links
RUN python -c "import pyneuroml"
#The purpose behind the seemingly redundant steps below is to make development copies of the code.
#These development copies

RUN conda install -y pyqt
RUN conda install -y matplotlib 


RUN pip install bs4

WORKDIR /home/jovyan/work/scidash

RUN git clone -b dev https://github.com/scidash/sciunit.git
WORKDIR /home/jovyan/work/scidash/sciunit
RUN ln -s /home/jovyan/work/scidash/sciunit/sciunit /opt/conda/lib/python3.5/site-packages/sciunit
RUN python -c "import sciunit"

WORKDIR /home/jovyan/work/scidash
RUN git clone -b dev https://github.com/russelljjarvis/neuronunit.git
#RUN pip install git+https://github.com/scidash/neuronunit
#WORKDIR /home/jovyan/work/scidash/neuronunit
RUN ln -s /home/jovyan/work/scidash/neuronunit/neuronunit /opt/conda/lib/python3.5/site-packages


RUN python -c "import neuronunit"
RUN python -c "from neuronunit.models.reduced import ReducedModel"






RUN apt-get update #such that apt-get install works straight off the bat inside the docker image.
#RUN apt-get install -y python3-setuptools
RUN python -c "import quantities, neuronunit, sciunit"


#I prefer to have password less sudo since it permits me 
#to quickly and easily modify the system interactively post dockerbuild.

 


#Test jNeuroML, which is called from pyNeuroML.
#Line below Not a fair test unless I can supply the file /tmp/vanilla.xml
#RUN java -Xmx400M  -Djava.awt.headless=true -jar  "/opt/conda/lib/python3.5/site-packages/pyneuroml/lib/jNeuroML-0.8.0-jar-with-dependencies.jar"  "/tmp/vanilla.xml" -neuron -#run -nogui

#Check if anything broke 
RUN python -c "import neuron; import sciunit; import neuronunit; import pyneuroml"
RUN nrnivmodl 
RUN python -c "import scoop; import deap"
RUN nrniv


#Finish up in a directory that easily interfaces with on the host operating system.

#Uncomment the following two lines if you don't want to log in to the docker image interactively.

RUN pip install django

#https://github.com/russelljjarvis/ChannelWormDjango
#RUN pip install git+https://github.com/openworm/ChannelWorm.git
RUN git clone https://github.com/russelljjarvis/ChannelWorm.git 
RUN ln -s /home/jovyan/work/scidash/ChannelWorm/channelworm /opt/conda/lib/python3.5/site-packages/channelworm
RUN python -c "import channelworm"


WORKDIR /home/jovyan/work/scidash
RUN git clone https://github.com/NeuralEnsemble/neuroConstruct.git 

WORKDIR /home/jovyan/work/scidash/neuroConstruct
#RUN ./updatenC.sh
#RUN echo NC_HOME
RUN bash nC.sh -make
RUN bash nCenv.sh
RUN echo 'export NC_HOME=home/jovyan/work/scidash/neuroConstruct' >> ~/.bashrc

#RUN bash nC.sh
#RUN << open nC.sh and change NC_HOME >>

RUN ln -s /home/jovyan/work/scidash/neuroConstruct/pythonnC /opt/conda/lib/python3.5/site-packages/pythonnC

RUN python -c "import pythonnC" 




#The following are convenience aliases
#once inside the image make it such that a notebook can be created using 
#the dockerimage python, but the hosts browser and the hosts mounted file system.
RUN echo 'alias nb="jupyter-notebook --ip=* --no-browser"' >> ~/.bashrc
RUN echo 'alias mnt="cd /home/mnt"' >> ~/.bashrc
RUN echo 'alias erc="emacs ~/.bashrc"' >> ~/.bashrc
RUN echo 'alias src="source ~/.bashrc"' >> ~/.bashrc
RUN echo 'alias egg="cd /opt/conda/lib/python3.5/site-packages/"' >> ~/.bashrc 
RUN echo 'alias nu="cd /home/jovyan/work/scidash/neuronunit"' >> ~/.bashrc
#Note the line below is required in order for jNeuroML to work inside pyNeuroML.
ENV NEURON_HOME "/home/jovyan/neuron/nrn-7.4/x86_64" #This line is not effective so the 
#next line is a hack, that achieves the same objectives as those embodied in the command above:
RUN echo 'export NEURON_HOME=/home/jovyan/neuron/nrn-7.4/x86_64' >> ~/.bashrc
RUN echo 'alias model="cd /work/scidash/neuronunit/neuronunit/models"' >> ~/.bashrc
RUN echo 'alias sciunit="cd /work/scidash/sciunit"' >> ~/.bashrc
RUN echo 'alias nu="python -c "from neuronunit.models.reduced import ReducedModel""'
RUN echo "DJANGO_SETTINGS_MODULE=myproject.settings.production"> ~/.bashrc

RUN apt-get update \
      && apt-get install -y sudo \
      && rm -rf /var/lib/apt/lists/*
RUN echo "jovyan ALL=NOPASSWD: ALL" >> /etc/sudoers


RUN chown -R jovyan $HOME

USER $NB_USER
WORKDIR /home/mnt
RUN pip install execnet

#WORKDIR /home/jovyan/mnt/sciunitopt
#ENTRYPOINT python -i /home/jovyan/mnt/sciunitopt/AIBS.py 






