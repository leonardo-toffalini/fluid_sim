from enum import Enum
from typing import Tuple, Annotated, Literal
import pygame as pg
import numpy as np
from numpy.typing import NDArray
import matplotlib.pyplot as plt

from utils import generate_perlin_noise_2d, hsl_to_rgb


class Flow(Enum):
    NO_FLOW = 0
    VERTICAL = 1
    HORIZONTAL = 2


class GridDrawer:
    """
    grid drawer class that contains:
      - Precomputed hsl -> rgb table with precision of 0.1
      - Precomputed cells to be colored individually
    """

    hsl_to_rgb_table = [hsl_to_rgb(180, 61, l / 10) for l in range(1001)]

    def __init__(self, grid_height: int, grid_width: int, cell_width: int):
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.cell_width = cell_width
        self.cells = self._make_cells()
        self.vel_cmap = plt.get_cmap("RdBu")
        self.screen = pg.display.get_surface()

    def _make_cells(self) -> np.ndarray:
        ret = np.empty(shape=(self.grid_height, self.grid_width), dtype=pg.Rect)
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                cell = pg.Rect(
                    (x - 1) * self.cell_width,
                    (y - 1) * self.cell_width,
                    self.cell_width,
                    self.cell_width,
                )
                ret[y, x] = cell
        return ret

    def draw_grid(self, grid: Annotated[NDArray[np.int8], Literal[2]]) -> None:
        np.clip(grid, 0, 255, out=grid)  # inplace
        l = (grid / 255) * 1000

        # keep in mind that the first and last rows and columns are boundaries, so they dont need to be drawn
        for y in range(1, self.grid_height - 1):
            for x in range(1, self.grid_width - 1):
                color = self.hsl_to_rgb_table[
                    int(l[y, x])
                ]  # TODO: consider proper rounding
                pg.draw.rect(self.screen, color, self.cells[y, x])

    def draw_velocity_field(
        self,
        u: Annotated[NDArray[np.int8], Literal[2]],
        v: Annotated[NDArray[np.int8], Literal[2]],
    ) -> None:
        grid = u * u + v * v
        grid_height, grid_width = grid.shape

        y, x = np.mgrid[1 : grid_height - 1, 1 : grid_width - 1]
        vals = 10000 * grid[1:-1, 1:-1]
        colors = self.vel_cmap(vals)
        colors_rgb = (colors[:, :, :3] * 255).astype(int)

        for y in range(1, grid_height - 1):
            for x in range(1, grid_width - 1):
                c_rgb = tuple(colors_rgb[y - 1, x - 1])
                pg.draw.rect(self.screen, c_rgb, self.cells[y, x])


def add_source(grid: np.ndarray, source: np.ndarray, dt: float) -> None:
    """Returns a new modified grid, where the sources are added to each corresponding cells"""
    assert grid.shape == source.shape
    grid += dt * source


def diffuse(grid: np.ndarray, b: Flow, diff: float, dt: float) -> np.ndarray:
    """Returns a new modified grid, where each cell's value is diffused."""
    new_grid = np.zeros_like(grid)
    rows, cols = grid.shape
    a = dt * diff * rows * cols

    up = new_grid[:-2, 1:-1]
    down = new_grid[2:, 1:-1]
    left = new_grid[1:-1, :-2]
    right = new_grid[1:-1, 2:]

    for _ in range(20):
        new_grid[1:-1, 1:-1] = (grid[1:-1, 1:-1] + a * (up + down + left + right)) / (
            1 + 4 * a
        )

    set_bound(new_grid, b)
    return new_grid


def advect(
    grid: np.ndarray, b: Flow, u: np.ndarray, v: np.ndarray, dt: float
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

    set_bound(new_grid, b)
    return new_grid


def project(u: np.ndarray, v: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    div = np.zeros_like(u)
    p = np.zeros_like(div)
    rows, cols = div.shape
    h = 1.0 / max(rows, cols)

    up_u = u[:-2, 1:-1]
    down_u = u[2:, 1:-1]
    left_v = v[1:-1, :-2]
    right_v = v[1:-1, 2:]

    div[1:-1, 1:-1] = -0.5 * h * (up_u - down_u + right_v - left_v)

    set_bound(div, Flow.NO_FLOW)
    set_bound(p, Flow.NO_FLOW)

    up = p[:-2, 1:-1]
    down = p[2:, 1:-1]
    left = p[1:-1, :-2]
    right = p[1:-1, 2:]

    for _ in range(20):
        p[1:-1, 1:-1] = (div[1:-1, 1:-1] + up + down + left + right) / 4

        set_bound(p, Flow.NO_FLOW)

    u[1:-1, 1:-1] = u[1:-1, 1:-1] - 0.5 * (up - down) / h
    v[1:-1, 1:-1] = v[1:-1, 1:-1] - 0.5 * (right - left) / h

    set_bound(u, Flow.VERTICAL)
    set_bound(v, Flow.HORIZONTAL)
    return u, v


def set_bound_bad(grid: np.ndarray) -> np.ndarray:
    new_grid = np.copy(grid)
    rows, cols = grid.shape
    new_grid[:, 0] = 0
    new_grid[:, cols - 1] = 0
    new_grid[0] = 0
    new_grid[rows - 1] = 0

    return new_grid


def set_bound(grid: np.ndarray, b: Flow, test_body: str = "circle") -> None:
    rows, cols = grid.shape
    horizontal_multiplier, vertical_multiplier = 1, 1

    if b == Flow.VERTICAL:
        vertical_multiplier = -1
    elif b == Flow.HORIZONTAL:
        horizontal_multiplier = -1

    grid[0, :] = vertical_multiplier * grid[1, :]
    grid[rows - 1, :] = vertical_multiplier * grid[rows - 2, :]
    grid[:, 0] = horizontal_multiplier * grid[:, 1]
    grid[:, cols - 1] = horizontal_multiplier * grid[:, cols - 2]

    if test_body == "box":
        set_box_bound(grid, b, ((rows // 2) - 2, (cols // 2) - 10), 4, 4)
    elif test_body == "circle":
        set_box_bound(grid, b, ((rows // 2) - 2, (cols // 2) - 10), 10, 4)
        set_box_bound(grid, b, ((rows // 2) - 5, (cols // 2) - 7), 4, 10)
        set_box_bound(grid, b, ((rows // 2) - 4, (cols // 2) - 9), 8, 8)

    grid[0, 0] = 0.5 * (grid[1, 0] + grid[0, 1])
    grid[0, cols - 1] = 0.5 * (grid[1, cols - 1] + grid[0, cols - 2])
    grid[rows - 1, 0] = 0.5 * (grid[rows - 2, 0] + grid[rows - 1, 1])
    grid[rows - 1, cols - 1] = 0.5 * (
        grid[rows - 2, cols - 1] + grid[rows - 1, cols - 2]
    )


def set_box_bound(
    grid: np.ndarray,
    b: Flow,
    pos: Tuple[int, int],
    width: int,
    height: int,
) -> None:
    box_top = pos[0]
    box_bot = pos[0] + height
    box_left = pos[1]
    box_right = pos[1] + width

    horizontal_multiplier, vertical_multiplier = 1, 1

    if b == Flow.VERTICAL:
        vertical_multiplier = -1
    elif b == Flow.HORIZONTAL:
        horizontal_multiplier = -1

    grid[box_top, box_left:box_right] = (
        vertical_multiplier * grid[box_top + 1, box_left:box_right]
    )

    grid[box_bot - 1, box_left:box_right] = (
        vertical_multiplier * grid[box_bot - 2, box_left:box_right]
    )

    grid[box_top:box_bot, box_left] = (
        horizontal_multiplier * grid[box_top:box_bot, box_left + 1]
    )

    grid[box_top:box_bot, box_right - 1] = (
        horizontal_multiplier * grid[box_top:box_bot, box_right - 2]
    )

    grid[box_top+1:box_bot-1, box_left+1:box_right-1] = 0


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
    add_source(grid, source, dt)
    grid = diffuse(grid, Flow.NO_FLOW, diff, dt)
    grid = advect(grid, Flow.NO_FLOW, u, v, dt)
    return grid


def vel_step(
    u: np.ndarray,
    v: np.ndarray,
    u_source: np.ndarray,
    v_source: np.ndarray,
    visc: float,
    dt: float,
) -> Tuple[np.ndarray, np.ndarray]:
    add_source(u, u_source, dt)
    add_source(v, v_source, dt)
    u = diffuse(u, Flow.VERTICAL, visc, dt)
    v = diffuse(v, Flow.HORIZONTAL, visc, dt)
    u, v = project(u, v)
    u = advect(u, Flow.VERTICAL, u, v, dt)
    v = advect(v, Flow.HORIZONTAL, u, v, dt)
    u, v = project(u, v)
    return u, v
