# Eulerian fluid simulation
This project aims to provide a succinct python implementation of the Eulerian fluid simulation 
described in <http://graphics.cs.cmu.edu/nsp/course/15-464/Fall09/papers/StamFluidforGames.pdf>

### Getting Started
Run the following command:
```sh
python main.py --help
```

### Requirements
For the list of requirements, see `environment.yaml`.

If you are using anaconda or miniconda create a conda environment with the following command:
```sh
conda env create -f environment.yaml
```

### Test scenarios
You can quickly test the program with some pre set up scenarios with the following command:
```sh
python main.py --test-scenario <0|1|2|3|4|5|6>
```

### How it works
You can find a detailed description of the ways of working of the simulation at `simulation.md`.


### Future goals
We spent a lot of effort optimizing the python implementation, but we are still not satisfied with the performance at higher resolutions. Python is not typically used for physics simulations, but we stuck we both are very familiar with python and switching to a more performant lower-level language would have resulted in worse developer experience. 

The easiest way to boost the performance of the code would be to port the projet to C/C++. The more natural path would be to rewrite the project as a shader program, given the nature of this project.

Another aspect we didn't get to work on during this project is to extend the simulation into the third dimension, giving rise to a more real-world like visual of fluids.
