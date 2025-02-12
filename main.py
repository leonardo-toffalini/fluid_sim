import pygame as pg
import numpy as np
import tyro
from dataclasses import dataclass
from engine import draw_grid, add_source, diffuse_bad, diffuse


@dataclass
class Args:
    WIDTH: int = 800
    HEIGHT: int = 600
    cell_size: int = 50


def main(args):
    pg.init()

    # note, that grid has 2 extra rows and columns, these are the boundaries
    rows, cols = 2 + args.HEIGHT // args.cell_size, 2 + args.WIDTH // args.cell_size
    grid = np.zeros(shape=(rows, cols))
    source = np.zeros_like(grid)
    source[rows // 2, cols // 2] = 10
    grid = add_source(grid, source, 1)

    screen = pg.display.set_mode((args.WIDTH, args.HEIGHT))
    pg.display.set_caption("Fluid simulation")

    running = True
    clock = pg.time.Clock()

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill((25, 25, 25))
        grid = diffuse(grid, 0.00015, 1)
        grid = add_source(grid, source, 1)
        draw_grid(grid, args.cell_size)
        pg.display.flip()
        clock.tick(60)

    pg.quit()


if __name__ == "__main__":
    args = tyro.cli(Args)
    main(args)
