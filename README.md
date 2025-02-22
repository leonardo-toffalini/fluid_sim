# Eulerian fluid simulation
This project aims to provide a succint python implementation of the Eulerian fluid simulation 
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

### TODO
- Possible optimization:
    - [ ] Don't copy grid on each function call.
    Instead, pass around two pointers to two grids and only mutate one while we take values from the other, just like double buffer rendering.

- Features:
    - [ ] Add visualization for velocity field
    - [ ] Implement a way to have solid objects in the scene
    - [ ] Add user input for moving solid objects in the scene
    - [ ] Create a nice looking title screen for the simulation


