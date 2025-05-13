# Simulation description

### Navier-Stokes equations
The main goal of the program is to solve the Navier-Stokes equations. Albeit the Navier-Stokes equations stand for a continuous space, we can employ ideas from numerical methods to divide the continuous space into a fix length grid.

The described way of simulating fluids is commonly known as Eulerian fluid simulation, in contrast to a Lagrangian fluid simulation that aims to simulate a fluid at the molecular level and cover the particles in a smooth blanket, tricking the beholder into thinking that they are watching a real fluid at work.

Navier-Stokes equations:

$$\frac{\partial u}{\partial t} = -(u \cdot \nabla) u+\nu \nabla^2 u+\mathbf{f}$$

$$\frac{\partial \rho}{\partial t} = -(u \cdot \nabla) \rho+\kappa \nabla^2 \rho+S$$

### Steps of the simulation
We can clearly see that both equations follow the same structure, with the time derivative of the density/velocity being composed of the following:
- Source
- Diffusion
- Advection

Along the lines of [Stam fluid simulation for games](https://graphics.cs.cmu.edu/nsp/course/15-464/Fall09/papers/StamFluidforGames.pdf), we present subroutines for the aforementioned steps.

### Adding sources
The part of ading sources may be the easiest, as it is sufficient to implement a matrix addition. Let $\rho$ be the density matrix and $S$ be the source of densities, then the `add_source` step solely implements $\rho + S$.

### Diffusion
For fluid to diffuse, it means that the density *spreads out*. To implement this idea, imagine the value of a cell spreading out to its edge-neighbours. In mathematical notation this means the following:

$x'_{i,j} = x_{i,j} + a (x_{i-1,j} + x_{i+1,j} \\ + x_{i,j-1} + x_{i,j+1} - 4 \cdot x_{i,j})$

Implementing the above equation is trivial, however, the results may be disappointing, as this method is an unstable explicit method. We can improve the method by transitioning to a stable implicit method. This can be done quite easily by *diffusing backward in time*, which can be stated as follows.

$x_{i,j} = x'_{i,j} - a (x'_{i-1,j} + x'_{i+1,j} \\ + x'_{i,j-1} + x'_{i,j+1} - 4 x'_{i,j})$

Solving for $x'$ we get the subsequent equation, which will be our final equation to implement for the diffusion step.

$x'_{i,j} = x_{i,j} + a (x_{i-1,j} + x_{i+1,j} \\ + x_{i,j-1} + x_{i,j+1} - 4 x_{i,j})/(1 + 4 a)$

The above specifies a system of equations to solve, this could be done with a prepackaged solver, however a faster iterative approach, like Gauss-Seidel works just as fine.

### Advection
Analogous, we can adopt a similar method for the advection solver, by instead of tracing the flow of the value in forwards direction, we can trace the value backwards in time. The `advect` method has the same structure as `diffuse`, with the only change being the system of equations to solve.

### Hodge decomposition
If one were to stop here, they might be surprised with unrealistic fluid behaviour, because they might see sources of velocity which are hard to find in the real world. To patch this mistake we ought to find a way to decompose the velocity field into gradient-free field and into a field which only contains gradients. Luckily such a method exists, it is called the Hodge decomposition, which can be solved by solving the Poisson equation. We will not dvelve into the details, but the implementation can be further explored in the `project` function.


