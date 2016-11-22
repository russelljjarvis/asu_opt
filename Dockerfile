FROM scidash/neuronunit-scoop-deap


USER root


#The purpose of installing and removing is to get all of the right dependencies.
RUN pip install git+https://github.com/scidash/neuronunit@dev --install-option="--prefix=/home/jovyan/work/scidash/neuronunit" --process-dependency-links
RUN rm -rf /opt/conda/lib/python3.5/site-packages/neuronunit
RUN rm -rf neuronunit-0.1.8.5-py3.5.egg-info/

RUN rm -rf /home/jovyan/work/scidash/neuronunit



WORKDIR /home/jovyan/work/scidash

RUN git clone https://github.com/russelljjarvis/neuronunit
#RUN git checkout dev

RUN ln -s /home/jovyan/work/scidash/neuronunit/neuronunit /opt/conda/lib/python3.5/site-packages/neuronunit

RUN python -c "import neuronunit;neuronunit.__file__"

#RUN ln -s /opt/conda/lib/python3.5/site-packages/neuronunit /home/jovyan/work/scidash/neuronunit/neuronunit
#RUN python -c "import neuronunit"



#WORKDIR /home/jovyan/work/scidash/sciunit
#RUN pip install git+https://github.com/scidash/sciunit@dev --install-option="--prefix=$home/jovyan/work/scidash/sciunit" --process-dependency-links
#WORKDIR /home/jovyan/work/scidash/sciunit


WORKDIR /home/jovyan/work/scidash/pyNeuroML
RUN pip install git+https://github.com/NeuroML/pyNeuroML --process-dependency-links

WORKDIR /home/jovyan/work/scidash
RUN pip install git+https://github.com/AllenInstitute/AllenSDK@py34_rgerkin --process-dependency-links
RUN python -c "import sciunit"

#WORKDIR /home/jovyan/work/git
#sudo pip3 install quantities
#RUN pip install git+https://github.com/python-quantities/python-quantities
#WORKDIR /home/jovyan/work/scidash/pyNeuroML
#RUN python setup.py


WORKDIR /home/jovyan/work/git
RUN git clone https://github.com/rgerkin/IzhikevichModel.git

WORKDIR /home/jovyan/work/git
RUN git clone https://github.com/russelljjarvis/sciunitopt.git
WORKDIR /home/jovyan/git/sciunitopt

#Not presently used:
#WORKDIR /home/jovyan/work/git
#RUN pip install git+https://github.com/aarongarrett/inspyred




RUN apt-get update #such that apt-get install works straight off the bat inside the docker image.
RUN cp -r $HOME/work/git/IzhikevichModel/* .

#I prefer to have password less sudo since it permits me 
#to quickly and easily modify the system interactively post dockerbuild.

RUN apt-get update \
      && apt-get install -y sudo \
      && rm -rf /var/lib/apt/lists/*
RUN echo "jovyan ALL=NOPASSWD: ALL" >> /etc/sudoers



RUN conda install -y matplotlib 



RUN chown -R jovyan $HOME
ENV NEURON_HOME "/home/jovyan/neuron/nrn-7.4/x86_64"

#make some of the packages installed in /opt/.../site-packages development versions. By getting write access.
#probably dodgy quick fix.
RUN chown -R jovyan /opt/conda/lib/python3.5/site-packages/neuronunit
RUN chown -R jovyan /opt/conda/lib/python3.5/site-packages/sciunit
#make an alias to change to this directory more readily
#possibly a better idea would be to make symbolic links to the files somewhere with a shorter pathl
#RUN CMD alias egg='cd /opt/conda/lib/python3.5/site-packages/'


#RUN sudo ln -s /opt/conda/lib/python3.5/site-packages/ $HOME/python_code

RUN echo 'alias nb="jupyter-notebook --ip=* --no-browser"' >> ~/.bashrc
RUN echo 'alias mnt="cd /home/mnt"' >> ~/.bashrc
RUN echo 'alias erc="emacs ~/.bashrc"' >> ~/.bashrc
RUN echo 'alias egg="cd /opt/conda/lib/python3.5/site-packages/"' >> ~/.bashrc 
RUN echo 'export NEURON_HOME=/home/jovyan/neuron/nrn-7.4/x86_64"' >> ~/.bashrc
RUN echo 'alias model="cd /work/scidash/neuronunit/neuronunit/models"' >> ~/.bashrc

USER $NB_USER


#Check if anything broke
RUN nrniv
#Line below Not a fair test unless I can supply /tmp/vanilla.xml
#RUN java -Xmx400M  -Djava.awt.headless=true -jar  "/opt/conda/lib/python3.5/site-packages/pyneuroml/lib/jNeuroML-0.8.0-jar-with-dependencies.jar"  "/tmp/vanilla.xml" -neuron -#run -nogui
 
RUN python -c "import neuron; import sciunit"# import neuronunit

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

#export NEURON_HOME=/home/jovyan/neuron/nrn-7.4/x86_64
#Note the line below is required in order for jNeuroML to work inside pyNeuroML.





