
To run this program first enter download the docker-stacks image.

https://github.com/scidash/docker-stacks.git 

Instructions for getting the image are at the README.md

Get the image corresponding to the build: neuronunit-scoop-deap

navigate to the this trunk directory, and mount this directory as a local file system using:

```docker run -v `pwd`:/home/mnt -it deap_build```
Then navigate to `/home/mnt` and run the file `nsga2.py` with monkey patching enabled by executing:
`ipython -i nsga2.py` 

To run with scoop (in parallel, note this is actually slower for small dimensional problems with small NGEN, and population size, since parallel programs involve interprocess communication related costs).

execute:
`python -m scoop nsga2.py`
