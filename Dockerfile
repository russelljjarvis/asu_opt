FROM scidash/neuronunit-scoop-deap
USER root

RUN pip install git+https://github.com/scidash/neuronunit@dev --install-option="--prefix=/home/jovyan/work/scidash/neuronunit" --process-dependency-links
WORKDIR /home/jovyan/work/scidash/pyNeuroML
RUN pip install git+https://github.com/NeuroML/pyNeuroML --process-dependency-links

WORKDIR /home/jovyan/work/scidash
RUN pip install git+https://github.com/AllenInstitute/AllenSDK@py34_rgerkin --process-dependency-links
RUN python -c "import sciunit"
RUN pip install git+https://github.com/python-quantities/python-quantities


RUN apt-get update #such that apt-get install works straight off the bat inside the docker image.
RUN apt-get install -y python3-setuptools
RUN python -c "import quantities, neuronunit, sciunit"


#I prefer to have password less sudo since it permits me 
#to quickly and easily modify the system interactively post dockerbuild.

RUN apt-get update \
      && apt-get install -y sudo \
      && rm -rf /var/lib/apt/lists/*
RUN echo "jovyan ALL=NOPASSWD: ALL" >> /etc/sudoers

RUN conda install -y matplotlib 
RUN chown -R jovyan $HOME

#The following are convenience 
RUN echo 'alias nb="jupyter-notebook --ip=* --no-browser"' >> ~/.bashrc
RUN echo 'alias mnt="cd /home/mnt"' >> ~/.bashrc
RUN echo 'alias erc="emacs ~/.bashrc"' >> ~/.bashrc
RUN echo 'alias egg="cd /opt/conda/lib/python3.5/site-packages/"' >> ~/.bashrc 

#Note the line below is required in order for jNeuroML to work inside pyNeuroML.
ENV NEURON_HOME "/home/jovyan/neuron/nrn-7.4/x86_64" #This line is not effective so hack:
RUN echo 'export NEURON_HOME=/home/jovyan/neuron/nrn-7.4/x86_64' >> ~/.bashrc
RUN echo 'alias model="cd /work/scidash/neuronunit/neuronunit/models"' >> ~/.bashrc

USER $NB_USER

#Test jNeuroML, which is called from pyNeuroML.
#Line below Not a fair test unless I can supply the file /tmp/vanilla.xml
#RUN java -Xmx400M  -Djava.awt.headless=true -jar  "/opt/conda/lib/python3.5/site-packages/pyneuroml/lib/jNeuroML-0.8.0-jar-with-dependencies.jar"  "/tmp/vanilla.xml" -neuron -#run -nogui

#Check if anything broke 
RUN python -c "import neuron; import sciunit; import neuronunit"
RUN nrnivmodl 
RUN python -c "import scoop; import deap"
RUN nrniv

#Finish up in a directory that easily interfaces with on the host operating system.
WORKDIR /home/mnt

#Not presently used, but will be later in development:
#WORKDIR /home/jovyan/work/git
#RUN pip install git+https://github.com/aarongarrett/inspyred

#WORKDIR /home/jovyan/work/git
#RUN git clone https://github.com/rgerkin/IzhikevichModel.git

#WORKDIR /home/jovyan/work/git
#RUN git clone https://github.com/russelljjarvis/sciunitopt.git
#WORKDIR /home/jovyan/git/sciunitopt

ENTRYPOINT python -i /home/mnt/AIBS.py 






