import pygame as pg
import numpy as np
import tyro
from dataclasses import dataclass


@dataclass
class Args:
    WIDTH: int = 800
    HEIGHT: int = 600
    cell_size: int = 50


def clamp(low, high, val):
    return max(low, min(high, val))


def draw_grid(grid: np.ndarray, cell_width: int) -> None:
    screen = pg.display.get_surface()
    grid_height, grid_width = grid.shape

    for y in range(grid_height):
        for x in range(grid_width):
            c = clamp(0, 255, grid[y, x])
            color = (c, c, c)
            cell = pg.Rect(x * cell_width, y * cell_width, cell_width, cell_width)
            pg.draw.rect(screen, color, cell)


def add_source(grid: np.ndarray, source: np.ndarray, dt: float) -> np.ndarray:
    assert grid.shape == source.shape

    grid_copy = np.copy(grid)  # we copy the original grid to not mutate it
    rows, cols = grid_copy.shape

    for i in range(rows):
        for j in range(cols):
            grid_copy[i, j] += dt * source[i, j]

    return grid_copy


def main(args):
    pg.init()

    rows, cols = args.HEIGHT // args.cell_size, args.WIDTH // args.cell_size
    low, high = 25, 225
    grid = np.zeros(shape=(rows, cols))
    source = np.ones_like(grid)

    screen = pg.display.set_mode((args.WIDTH, args.HEIGHT))
    pg.display.set_caption("Fluid simulation")

    running = True
    clock = pg.time.Clock()

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill((25, 25, 25))
        # uncomment to make hangya foci
        # grid = np.random.randint(low, high, size=(rows, cols))
        grid = add_source(grid, source, 1)
        draw_grid(grid, args.cell_size)
        pg.display.flip()
        clock.tick(60)

    pg.quit()


if __name__ == "__main__":
    args = tyro.cli(Args)
    main(args)
