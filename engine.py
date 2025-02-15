from typing import Tuple
import pygame as pg
import numpy as np

from utils import apply_kernel, generate_perlin_noise_2d


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
    grid_copy = grid + dt * source
    return grid_copy


def diffuse_bad(grid: np.ndarray, b: int, diff: float, dt: float) -> np.ndarray:
    """Returns a new modified grid, where each cell's value is diffused. This method can be unstable."""
    new_grid = np.zeros_like(grid)
    rows, cols = grid.shape
    a = dt * diff * rows * cols
    kernel = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])

    new_grid[1:-1, 1:-1] = grid[1:-1, 1:-1] + a * apply_kernel(grid[1:-1, 1:-1], kernel)

    new_grid = set_bound(new_grid, b)
    return new_grid


def diffuse(grid: np.ndarray, b: int, diff: float, dt: float) -> np.ndarray:
    """Returns a new modified grid, where each cell's value is diffused."""
    new_grid = np.zeros_like(grid)
    rows, cols = grid.shape
    a = dt * diff * rows * cols

    for _ in range(20):
        up = new_grid[:-2, 1:-1]
        down = new_grid[2:, 1:-1]
        left = new_grid[1:-1, :-2]
        right = new_grid[1:-1, 2:]

        new_grid[1:-1, 1:-1] = (grid[1:-1, 1:-1] + a * (up + down + left + right)) / (
            1 + 4 * a
        )

    new_grid = set_bound(new_grid, b)
    return new_grid


def advect(
    grid: np.ndarray, b: int, u: np.ndarray, v: np.ndarray, dt: float
) -> np.ndarray:
    """Returns a new modified grid, where the velocities, u and v, are applied to the grid cell values."""
    new_grid = np.copy(grid)
    rows, cols = grid.shape
    dt0 = dt * rows

    i, j = np.meshgrid(np.arange(1, rows - 1), np.arange(1, cols - 1), indexing="ij")

    x = i - dt0 * u[1:-1, 1:-1]
    y = j - dt0 * v[1:-1, 1:-1]

    x = np.clip(x, 0.5, rows - 0.5)
    y = np.clip(y, 0.5, cols - 0.5)

    # Calculate indices and weights
    i0 = x.astype(int)
    j0 = y.astype(int)
    i1 = i0 + 1
    j1 = j0 + 1
    s1 = x - i0
    s0 = 1 - s1
    t1 = y - j0
    t0 = 1 - t1

    # Perform bilinear interpolation
    new_grid[1:-1, 1:-1] = s0 * (t0 * grid[i0, j0] + t1 * grid[i0, j1]) + s1 * (
        t0 * grid[i1, j0] + t1 * grid[i1, j1]
    )

    new_grid = set_bound(new_grid, b)
    return new_grid


def project(u: np.ndarray, v: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    div = np.zeros_like(u)
    p = np.zeros_like(div)
    rows, cols = div.shape
    h = 1.0 / max(rows, cols)

    up_u = p[:-2, 1:-1]
    down_u = p[2:, 1:-1]
    left_v = p[1:-1, :-2]
    right_v = p[1:-1, 2:]

    div[1:-1, 1:-1] = -0.5 * h * (up_u - down_u + right_v - left_v)


    div = set_bound(div, 0)
    p = set_bound(p, 0)

    for _ in range(20):
        up = p[:-2, 1:-1]
        down = p[2:, 1:-1]
        left = p[1:-1, :-2]
        right = p[1:-1, 2:]

        p[1:-1, 1:-1] = (div[1:-1, 1:-1] + up + down + left + right) / 4

        p = set_bound(p, 0)

    up = p[:-2, 1:-1]
    down = p[2:, 1:-1]
    left = p[1:-1, :-2]
    right = p[1:-1, 2:]

    u[1:-1, 1:-1] = u[1:-1, 1:-1] - 0.5 * (up - down) / h
    v[1:-1, 1:-1] = v[1:-1, 1:-1] - 0.5 * (right - left) / h

    u = set_bound(u, 1)
    v = set_bound(v, 2)
    return u, v


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
    grid = diffuse(grid, 0, diff, dt)
    grid = advect(grid, 0, u, v, dt)
    return grid


def vel_step(
    u: np.ndarray, v: np.ndarray, visc: float, dt: float
) -> Tuple[np.ndarray, np.ndarray]:
    u = diffuse(u, 1, visc, dt)
    v = diffuse(v, 2, visc, dt)
    u, v = project(u, v)
    u = advect(u, 1, u, v, dt)
    v = advect(v, 2, u, v, dt)
    u, v = project(u, v)
    return u, v
