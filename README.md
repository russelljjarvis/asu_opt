

To run this program first enter download the docker-stacks tree associated with the dev branch.

https://github.com/scidash/docker-stacks/tree/dev

Instructions for getting the image are at the README.md

Get the image corresponding to the build: neuronunit-scoop-deap

navigate to the this trunk directory, and mount this directory as a local file system using:

The following  line has only been tested in Ubuntu linux, and has not been tested with OSX

```docker run -it -p 8888:8888 -v `pwd`:/home/jovyan/work/scipyopt para-nrn-python bash```
```docker run -v `pwd`:/home/mnt -it deap_build```

Then navigate to `/home/mnt` and run the file `nsga2.py` with by executing:
`ipython -i nsga2.py` 

the -i flag facilitates monkey patching.

To run with scoop (in parallel, note this is actually slower for small dimensional problems with small NGEN, and population size, since parallel programs involve interprocess communication related costs).

execute:
`python -m scoop nsga2.py`
