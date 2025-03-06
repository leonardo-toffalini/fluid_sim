from typing import Tuple, Annotated, Literal
import pygame as pg
import numpy as np
from numpy.typing import NDArray
import matplotlib.pyplot as plt
from enum import Enum

from utils import generate_perlin_noise_2d, hsl_to_rgb


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


class Dir(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4


class Flow(Enum):
    NONE = 0
    VERTICAL = 1
    HORIZONTAL = 2


class BoundaryOld:
    def apply(self, grid: np.ndarray, b: int) -> None:
        set_bound(grid, b)


class Boundary:
    def __init__(self, bound: np.ndarray):
        self.bound = bound
        self.mask = bound != 0

        zero_mask = 1 - self.bound  # assumes that all elems either 0 or 1
        padded = np.pad(zero_mask, pad_width=1, mode="constant", constant_values=0)

        # TODO: consider 8-neighbour solution
        cnt = (
            padded[:-2, 1:-1] + padded[1:-1, :-2] + padded[1:-1, 2:] + padded[2:, 1:-1]
        )

        # TODO: Handle elements with only solid neighbours
        cnt[cnt != 0] = 1 / cnt[cnt != 0]
        cnt[self.mask == 0] = 0

        self.left = Boundary.shift_and_mask(cnt, Dir.LEFT)
        self.right = Boundary.shift_and_mask(cnt, Dir.RIGHT)
        self.up = Boundary.shift_and_mask(cnt, Dir.UP)
        self.down = Boundary.shift_and_mask(cnt, Dir.DOWN)

    def apply(self, grid: np.ndarray, flow: Flow) -> None:
        m_v, m_h = 1, 1
        if flow == Flow.HORIZONTAL:
            m_h = -1
        if flow == Flow.VERTICAL:
            m_v = -1

        values_in_solids = (
            m_h * Boundary.shift(grid * self.left, Dir.RIGHT)
            + m_h * Boundary.shift(grid * self.right, Dir.LEFT)
            + m_v * Boundary.shift(grid * self.up, Dir.DOWN)
            + m_v * Boundary.shift(grid * self.down, Dir.UP)
        )

        grid[self.mask] = values_in_solids[self.mask]

    @staticmethod
    def shift_and_mask(arr: np.ndarray, dir: Dir) -> np.ndarray:
        shifted = Boundary.shift(arr, dir)
        mask = arr == 0
        shifted *= mask
        return shifted

    @staticmethod
    def shift(arr: np.ndarray, dir: Dir) -> np.ndarray:
        shifted = np.zeros_like(arr)
        if dir == Dir.LEFT:
            shifted[:, :-1] = arr[:, 1:]
        elif dir == Dir.RIGHT:
            shifted[:, 1:] = arr[:, :-1]
        elif dir == Dir.UP:
            shifted[:-1, :] = arr[1:, :]
        elif dir == Dir.DOWN:
            shifted[1:, :] = arr[:-1, :]
        else:
            raise Exception(f"Dir: Invalid enum item '{dir}'")
        return shifted


def add_source(grid: np.ndarray, source: np.ndarray, dt: float) -> None:
    """Returns a new modified grid, where the sources are added to each corresponding cells"""
    assert grid.shape == source.shape
    grid += dt * source


def diffuse(grid: np.ndarray, boundary, b: Flow, diff: float, dt: float) -> np.ndarray:
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

    boundary.apply(new_grid, b)
    return new_grid


def advect(
    grid: np.ndarray, boundary, b: Flow, u: np.ndarray, v: np.ndarray, dt: float
) -> np.ndarray:
    """Returns a new modified grid, where the velocities, u and v, are applied to the grid cell values."""
    new_grid = np.copy(grid)
    rows, cols = grid.shape
    dt0 = dt * rows

    i, j = np.meshgrid(np.arange(1, rows - 1), np.arange(1, cols - 1), indexing="ij")

    x = i - dt0 * u[1:-1, 1:-1]
    y = j - dt0 * v[1:-1, 1:-1]

    np.clip(x, 0.5, rows - 0.5, out=x)
    np.clip(y, 0.5, cols - 0.5, out=y)

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

    boundary.apply(new_grid, b)
    return new_grid


def project(u: np.ndarray, v: np.ndarray, boundary) -> Tuple[np.ndarray, np.ndarray]:
    div = np.zeros_like(u)
    p = np.zeros_like(div)
    rows, cols = div.shape
    h = 1.0 / max(rows, cols)

    up_u = u[:-2, 1:-1]
    down_u = u[2:, 1:-1]
    left_v = v[1:-1, :-2]
    right_v = v[1:-1, 2:]

    div[1:-1, 1:-1] = -0.5 * h * (up_u - down_u + right_v - left_v)

    boundary.apply(div, Flow.NONE)
    boundary.apply(p, Flow.NONE)

    up = p[:-2, 1:-1]
    down = p[2:, 1:-1]
    left = p[1:-1, :-2]
    right = p[1:-1, 2:]

    for _ in range(20):
        p[1:-1, 1:-1] = (div[1:-1, 1:-1] + up + down + left + right) / 4

        boundary.apply(p, Flow.NONE)

    u[1:-1, 1:-1] = u[1:-1, 1:-1] - 0.5 * (up - down) / h
    v[1:-1, 1:-1] = v[1:-1, 1:-1] - 0.5 * (right - left) / h

    boundary.apply(u, Flow.VERTICAL)
    boundary.apply(v, Flow.HORIZONTAL)
    return u, v


def set_bound_bad(grid: np.ndarray) -> np.ndarray:
    new_grid = np.copy(grid)
    rows, cols = grid.shape
    new_grid[:, 0] = 0
    new_grid[:, cols - 1] = 0
    new_grid[0] = 0
    new_grid[rows - 1] = 0

    return new_grid


def set_bound(grid: np.ndarray, b: int, test_body: str = "box") -> None:
    rows, cols = grid.shape
    grid[0, :] = -grid[1, :] if b == 1 else grid[1, :]
    grid[rows - 1, :] = -grid[rows - 2, :] if b == 1 else grid[rows - 2, :]
    grid[:, 0] = -grid[:, 1] if b == 2 else grid[:, 1]
    grid[:, cols - 1] = -grid[:, cols - 2] if b == 2 else grid[:, cols - 2]

    if test_body == "box":
        set_box_bound(grid, b, ((rows // 2) - 2, (cols // 2) - 10), 4, 4)

    grid[0, 0] = 0.5 * (grid[1, 0] + grid[0, 1])
    grid[0, cols - 1] = 0.5 * (grid[1, cols - 1] + grid[0, cols - 2])
    grid[rows - 1, 0] = 0.5 * (grid[rows - 2, 0] + grid[rows - 1, 1])
    grid[rows - 1, cols - 1] = 0.5 * (
        grid[rows - 2, cols - 1] + grid[rows - 1, cols - 2]
    )


def set_box_bound(
    grid: np.ndarray,
    b: int,
    pos: Tuple[int, int],
    width: int,
    height: int,
) -> None:
    box_top = pos[0]
    box_bot = pos[0] + height
    box_left = pos[1]
    box_right = pos[1] + width

    grid[box_top, box_left:box_right] = (
        -grid[box_top + 1, box_left:box_right]
        if b == 1
        else grid[box_top + 1, box_left:box_right]
    )

    grid[box_bot - 1, box_left:box_right] = (
        -grid[box_bot - 2, box_left:box_right]
        if b == 1
        else grid[box_bot - 2, box_left:box_right]
    )

    grid[box_top:box_bot, box_left] = (
        -grid[box_top:box_bot, box_left + 1]
        if b == 2
        else grid[box_top:box_bot, box_left + 1]
    )
    grid[box_top:box_bot, box_right - 1] = (
        -grid[box_top:box_bot, box_right - 2]
        if b == 2
        else grid[box_top:box_bot, box_right - 2]
    )


def dense_step(
    grid: np.ndarray,
    source: np.ndarray,
    u: np.ndarray,
    v: np.ndarray,
    boundary,
    diff: float,
    dt: float,
) -> np.ndarray:
    """Simulates on step for the density simulation. Returns a new modified grid.
    add sources, diffusion, advection"""
    add_source(grid, source, dt)
    grid = diffuse(grid, boundary, Flow.NONE, diff, dt)
    grid = advect(grid, boundary, Flow.NONE, u, v, dt)
    return grid


def vel_step(
    u: np.ndarray,
    v: np.ndarray,
    u_source: np.ndarray,
    v_source: np.ndarray,
    boundary,
    visc: float,
    dt: float,
) -> Tuple[np.ndarray, np.ndarray]:
    add_source(u, u_source, dt)
    add_source(v, v_source, dt)
    u = diffuse(u, boundary, Flow.VERTICAL, visc, dt)
    v = diffuse(v, boundary, Flow.HORIZONTAL, visc, dt)
    u, v = project(u, v, boundary)
    u = advect(u, boundary, Flow.VERTICAL, u, v, dt)
    v = advect(v, boundary, Flow.HORIZONTAL, u, v, dt)
    u, v = project(u, v, boundary)
    return u, v


if __name__ == "__main__":
    m = np.zeros((10, 10))
    # m[4:8, 5:7] = 1
    # m[4, 4] = 1
    m[0, :] = 1
    m[:, 0] = 1

    b = Boundary(m)
    print(b.bound)
    print()
    print(b.left)
    print()
    print(b.right)
    print()
    print(b.up)
    print()
    print(b.down)

    moc = np.arange(100).reshape(m.shape)
    # asd = np.zeros_like(m)
    print(moc)
    b.apply(moc, Flow.VERTICAL)
    print(moc)
