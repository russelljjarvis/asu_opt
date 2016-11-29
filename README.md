#Neuronunitopt
A development project that integrates neuronunit with DEAP Genetic Algorithm Optomization.

## Instructions for building etc.

To run this program first enter download the [docker-stacks tree associated with the dev branch.](https://github.com/scidash/docker-stacks/tree/dev "Title").

Instructions for getting the image are at the [README.md](https://github.com/scidash/docker-stacks/blob/dev/README.md "Title").

Get the image corresponding to the build: neuronunit-scoop-deap

# Build
Then build the Dockerfile in this directory which uses the docker-stacks as its foundation. You can use a command similar or the same as:
`sudo docker build -t deapscoop1 .` 

# Run:
```sudo docker run -v `pwd`:/home/mnt -it deapscoop1 bash```
then inside the docker image:
execute: `mnt`
`python AIBS.py`

# Other commands that are useful for interactive Development and Monkey patching:

```sudo docker run -v `pwd`:/home/mnt -it deapscoop1```, mounts local the local file system, without entering the image.


If your intention is not to run a notebook at all, but to develop inside the docker environment, you can use:
```sudo docker run -it -v `pwd`:/home/mnt deapscoop1 bash```

Which may be equivalent to:
```sudo docker run -v `pwd`:/home/mnt -it deapscoop1 bash```

If the volume has already been mounted once, however you want to open a second terminal window into it:
`sudo docker run -it deapscoop1 bash`



One of several ways to invoke a locally based notebook:

While you are in this directory mount it as a local file system and run the python code via the image:

```sudo docker run -it -p 8888:8888 -v `pwd`:/home/mnt deapscoop1 bash```

Or equivalently:

```sudo docker run -itp 8888:8888 -v `pwd`:/home/mnt deapscoop1 /bin/bash```

The flag `-p` means use port `8888`. The flag `-i` means interactive. The flag `-v` means mount volume.

From inside the docker image you can navigate to the appropriate directory. In this case its `/home/jovyan/work/git`, and then run the following command: `nb`
This is a BASH alias for the command: `jupyter-notebook --ip=* --no-browser`

Subsequently to see a list of all notebook(s) in the directory open the following URL in your browser:
`http://localhost:8888/tree`


Question:

How do you know that the program is solving both objective functions when only one of them is plotted. Answer: Need to fix in the future, such a 2D matrix of the error surface is made. Such that each element of the matrix represents the simple linear sum f(x,y). 

The following is not applicable in the current development stage, but will be applicable later:

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



