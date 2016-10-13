
To run this program first enter download the docker-stacks image.

https://github.com/scidash/docker-stacks.git 

Instructions for getting the image are at the README.md

Get the image corresponding to the build.
neuronunit-scoop-deap

navigate to the this trunk directory, and mount this directory as a local file system using:
`docker run -v `pwd`:/home/mnt -it deap_build`
Then navigate to `/home/mnt`
and run 
`ipython -i nsga2.py` 
