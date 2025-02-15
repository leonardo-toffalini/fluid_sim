from typing import Tuple
import pygame as pg
import numpy as np

from utils import generate_perlin_noise_2d


def test_scenario_1(
    rows: int, cols: int
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Sets up a test scenario where there is a strip of sources in the middle of the left edge,
    and there is only constant right directed, laminar wind.

    Returns:
        grid, source, u, v
    """
    grid = np.zeros(shape=(rows, cols))
    u = np.zeros_like(grid)
    v = np.ones_like(grid) / 25
    source = np.zeros_like(grid)
    source[(rows // 2) - 3 : (rows // 2) + 3, 1] = 200

    return grid, source, u, v


def test_scenario_2(
    rows: int, cols: int
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Sets up a test scenario where there are three dot sources in the middle with no wind.

    Returns:
        grid, source, u, v
    """
    grid = np.zeros(shape=(rows, cols))
    u = np.zeros_like(grid)
    v = np.zeros_like(grid)
    source = np.zeros_like(grid)
    source[2 * rows // 3, cols // 2] = 200
    source[rows // 2, cols // 3] = 200
    source[rows // 2, 2 * cols // 3] = 200

    return grid, source, u, v


def test_scenario_3(
    rows: int, cols: int
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Sets up a test scenario where there is a strip of sources in the middle of the left edge,
    and there is right facing wind with perlin noise.

    Returns:
        grid, source, u, v
    """
    grid = np.zeros(shape=(rows, cols))
    u = np.zeros_like(grid)
    print(grid.shape)
    noise = generate_perlin_noise_2d(grid.shape, res=(2, 2))
    v = np.ones_like(grid) / 200 + noise / 30
    source = np.zeros_like(grid)
    source[(rows // 2) - 3 : (rows // 2) + 3, 1] = 200

    return grid, source, u, v


def clamp(low, high, val):
    return max(low, min(high, val))


def draw_grid(grid: np.ndarray, cell_width: int) -> None:
    screen = pg.display.get_surface()
    grid_height, grid_width = grid.shape

    # keep in mind that the first and last rows and columns are boundaries, so they dont need to be drawn
    for y in range(1, grid_height - 1):
        for x in range(1, grid_width - 1):
            c = clamp(0, 255, grid[y, x])
            color = (c, c, c)
            cell = pg.Rect(
                (x - 1) * cell_width, (y - 1) * cell_width, cell_width, cell_width
            )
            pg.draw.rect(screen, color, cell)


def add_source(grid: np.ndarray, source: np.ndarray, dt: float) -> np.ndarray:
    """Returns a new modified grid, where the sources are added to each corresponding cells"""
    assert grid.shape == source.shape

    grid_copy = np.copy(grid)  # we copy the original grid to not mutate it
    rows, cols = grid_copy.shape

    for i in range(rows):
        for j in range(cols):
            grid_copy[i, j] += dt * source[i, j]

    return grid_copy


def diffuse_bad(grid: np.ndarray, diff: float, dt: float) -> np.ndarray:
    """Returns a new modified grid, where each cell's value is diffused. This method can be unstable."""
    new_grid = np.zeros_like(grid)
    rows, cols = grid.shape
    a = dt * diff * rows * cols

    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            new_grid[i, j] = grid[i, j] + a * (
                grid[i - 1, j]
                + grid[i + 1, j]
                + grid[i, j - 1]
                + grid[i, j + 1]
                - 4 * grid[i, j]
            )

    new_grid = set_bound(new_grid, 0)
    return new_grid


def diffuse(grid: np.ndarray, diff: float, dt: float) -> np.ndarray:
    """Returns a new modified grid, where each cell's value is diffused."""
    new_grid = np.zeros_like(grid)
    rows, cols = grid.shape
    a = dt * diff * rows * cols

    for _ in range(20):
        for i in range(1, rows - 1):
            for j in range(1, cols - 1):
                new_grid[i, j] = (
                    grid[i, j]
                    + a
                    * (
                        new_grid[i - 1, j]
                        + new_grid[i + 1, j]
                        + new_grid[i, j - 1]
                        + new_grid[i, j + 1]
                    )
                ) / (1 + 4 * a)

    new_grid = set_bound(new_grid, 0)
    return new_grid


def advect(grid: np.ndarray, u: np.ndarray, v: np.ndarray, dt: float) -> np.ndarray:
    """Returns a new modified grid, where the velocities, u and v, are applied to the grid cell values."""
    new_grid = np.copy(grid)
    rows, cols = grid.shape
    dt0 = dt * rows

    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            x = i - dt0 * u[i, j]
            y = j - dt0 * v[i, j]
            x = clamp(0.5, rows - 0.5, x)
            y = clamp(0.5, cols - 0.5, y)
            i0 = int(x)
            j0 = int(y)
            i1 = i0 + 1
            j1 = j0 + 1
            s1 = x - i0
            s0 = 1 - s1
            t1 = y - j0
            t0 = 1 - t1
            new_grid[i, j] = s0 * (t0 * grid[i0, j0] + t1 * grid[i0, j1]) + s1 * (
                t0 * grid[i1, j0] + t1 * grid[i1, j1]
            )

    new_grid = set_bound(new_grid, 0)
    return new_grid


def set_bound_bad(grid: np.ndarray) -> np.ndarray:
    new_grid = np.copy(grid)
    rows, cols = grid.shape
    new_grid[:, 0] = 0
    new_grid[:, cols - 1] = 0
    new_grid[0] = 0
    new_grid[rows - 1] = 0

    return new_grid


def set_bound(grid: np.ndarray, b: int) -> np.ndarray:
    new_grid = np.copy(grid)
    rows, cols = grid.shape
    new_grid[0, :] = -grid[1, :] if b == 1 else grid[1, :]
    new_grid[rows - 1, :] = -grid[rows - 2, :] if b == 1 else grid[rows - 2, :]
    new_grid[:, 0] = -grid[:, 1] if b == 2 else grid[:, 1]
    new_grid[:, cols - 1] = -grid[:, cols - 2] if b == 2 else grid[:, cols - 2]

    new_grid[0, 0] = 0.5 * (grid[1, 0] + grid[0, 1])
    new_grid[0, cols - 1] = 0.5 * (grid[1, cols - 1] + grid[0, cols - 2])
    new_grid[rows - 1, 0] = 0.5 * (grid[rows - 2, 0] + grid[rows - 1, 1])
    new_grid[rows - 1, cols - 1] = 0.5 * (
        grid[rows - 2, cols - 1] + grid[rows - 1, cols - 2]
    )

    return new_grid


def dense_step(
    grid: np.ndarray,
    source: np.ndarray,
    u: np.ndarray,
    v: np.ndarray,
    diff: float,
    dt: float,
) -> np.ndarray:
    """Simulates on step for the density simulation. Returns a new modified grid.
    add sources, diffusion, advection"""
    grid = add_source(grid, source, dt)
    grid = diffuse(grid, diff, dt)
    grid = advect(grid, u, v, dt)
    return grid
