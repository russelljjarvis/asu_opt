
To run this program first enter download the docker-stacks image.
## Instructions are at the README.md:
https://github.com/scidash/docker-stacks.git 

Get the image corresponding to the build.
neuronunit-scoop-deap

navigate to the this trunk directory, and mount this directory as a local file system using:
docker run -v `pwd`:/home/mnt -it deap_build
`ipython -i nsga2.py` 
