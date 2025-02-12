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
- [ ] Read the following paper: <http://graphics.cs.cmu.edu/nsp/course/15-464/Fall09/papers/StamFluidforGames.pdf>

- [ ] Implement moving densities
    - [ ] Add sources
    - [ ] Add diffusion
        - Maybe try both diffusion methods, naive and Gauss-Seidel
    - [ ] Add advection

- [ ] Implement evolving velocities

- [ ] Possible optimization:
    Don't copy grid on each function call.
    Instead, pass around two pointers to two grids and only mutate one while we take values from the other, just like double buffer rendering.
