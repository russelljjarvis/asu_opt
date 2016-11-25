
FROM scidash/neuronunit-scoop-deap
USER root
#The point of the master branch is to currently reliably reproduce bugs.

RUN pip install git+https://github.com/scidash/neuronunit@dev --process-dependency-links
WORKDIR /home/jovyan/work/scidash/pyNeuroML
RUN pip install git+https://github.com/NeuroML/pyNeuroML --process-dependency-links


WORKDIR /home/jovyan/work/scidash
RUN pip install git+https://github.com/AllenInstitute/AllenSDK@py34_rgerkin --process-dependency-links

RUN pip install git+https://github.com/python-quantities/python-quantities
WORKDIR /home/jovyan/work/scidash/pyNeuroML
RUN pip install git+https://github.com/NeuroML/pyNeuroML --process-dependency-links



RUN apt-get update #such that apt-get install works straight off the bat inside the docker image.

RUN python -c "import pyneuroml"
RUN python -c "import quantities, neuronunit, sciunit"


#I prefer to have password less sudo since it permits me 
#to quickly and easily modify the system interactively post dockerbuild.

RUN apt-get update \
      && apt-get install -y sudo \
      && rm -rf /var/lib/apt/lists/*
RUN echo "jovyan ALL=NOPASSWD: ALL" >> /etc/sudoers

RUN conda install -y matplotlib 
RUN chown -R jovyan $HOME

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


WORKDIR /home/jovyan/mnt
RUN git clone https://github.com/russelljjarvis/sciunitopt.git


USER $NB_USER

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

WORKDIR /home/jovyan/mnt/sciunitopt
ENTRYPOINT python -i /home/jovyan/mnt/sciunitopt/AIBS.py 






