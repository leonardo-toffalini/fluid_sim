import pygame as pg
import numpy as np


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
    assert grid.shape == source.shape

    grid_copy = np.copy(grid)  # we copy the original grid to not mutate it
    rows, cols = grid_copy.shape

    for i in range(rows):
        for j in range(cols):
            grid_copy[i, j] += dt * source[i, j]

    return grid_copy


def diffuse_bad(grid: np.ndarray, diff: float, dt: float) -> np.ndarray:
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

    new_grid = set_bound(new_grid)
    return new_grid


def diffuse(grid: np.ndarray, diff: float, dt: float) -> np.ndarray:
    new_grid = np.zeros_like(grid)
    rows, cols = grid.shape
    a = dt * diff * rows * cols

    for k in range(20):
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

    new_grid = set_bound(new_grid)
    return new_grid


def set_bound(grid: np.ndarray) -> np.ndarray:
    new_grid = np.copy(grid)
    rows, cols = grid.shape
    for i in range(rows):
        new_grid[i, 0] = 0
        new_grid[i, cols - 1] = 0

    for j in range(rows):
        new_grid[0, j] = 0
        new_grid[rows - 1, j] = 0

    return new_grid
