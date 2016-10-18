The output of this program is a series of png images. Each file names is indexed by iterations of generation. By clicking through the series of images you can watch a GA population converge around an optima of a trivial error function.

Question: How do you know that the program is solving both objective functions when only one of them is plotted. Answer: Need to fix in the future, such a 2D matrix of the error surface is made. Such that each element of the matrix represents the simple linear sum f(x,y). 

The program can be run with or without scoop (see more on that below).

The program in the Dockerfile build context has only been tested in Ubuntu linux, and has not been tested with OSX

## Instructions for building, deploying etc.

To run this program first enter download the docker-stacks tree associated with the dev branch.

`https://github.com/scidash/docker-stacks/tree/dev`

Instructions for getting the image are at the README.md

Get the image corresponding to the build: neuronunit-scoop-deap

Then build the Dockerfile in this directory which uses the docker-stacks as its foundation. You can use a command similar or the same as:
`sudo docker build -t deapscoop1 .` 

While you are in this directory mount it as a local file system and run the python code via the image:

```sudo docker run -it -p 8888:8888 -v `pwd`:/home/jovyan/work/scipyopt deapscoop1 bash```

Other commands that are useful for interactive Development and Monkey patching:

```docker run -v `pwd`:/home/mnt -it deapscoop1```, mounts local the local file system, without entering the image.

```docker run -it -p 8888:8888 -v `pwd`:/home/jovyan/work/scipyopt deapscoop1 bash```

Once the program has finished, you can stick around you can even edit the file `/home/jovyan/work/scipyopt/nsga2.py` with emacs or rerun it by executing:
`ipython -i nsga2.py`, where the `-i` flag facilitates monkey patching.
 
Its probably better to edit the file on the host system if powerful graphical editors are your thing.

To run with scoop (in parallel, note this is actually slower for small dimensional problems with small `NGEN`, and population size, since parallel programs involve interprocess communication related costs).

execute:
`python -m scoop nsga2.py`

To run the simple linear sum example use:
`python -i simple.py`
This example doesn't actually have multiple objective functions, however extending the example such that it is multiobjective should be straight forward.

You can also uncomment the appropriate line in the Dockerfile to run scoop.
