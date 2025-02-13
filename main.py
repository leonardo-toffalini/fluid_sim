import pygame as pg
import numpy as np
import tyro
from dataclasses import dataclass
from engine import draw_grid, add_source, dense_step


@dataclass
class Args:
    WIDTH: int = 800
    HEIGHT: int = 600
    cell_size: int = 10


def main(args):
    pg.init()

    ### Setup
    # note, that grid has 2 extra rows and columns, these are the boundaries
    rows, cols = 2 + args.HEIGHT // args.cell_size, 2 + args.WIDTH // args.cell_size
    grid = np.zeros(shape=(rows, cols))
    source = np.zeros_like(grid)
    source[rows // 3, cols // 2] = 200
    source[rows // 2, cols // 3] = 200
    source[rows // 2, 2 * cols // 3] = 200
    grid = add_source(grid, source, 1)

    screen = pg.display.set_mode((args.WIDTH, args.HEIGHT))
    pg.display.set_caption("Fluid simulation")
    font = pg.font.Font(None, 36)

    running = True
    clock = pg.time.Clock()

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill((25, 25, 25))

        ### Core logic
        grid = dense_step(grid, source, diff=0.00015, dt=1)
        draw_grid(grid, args.cell_size)

        # render fps counter on the screen
        fps = int(clock.get_fps())
        fps_text = font.render(f"FPS {fps}", True, (255, 255, 255))
        screen.blit(fps_text, (10, 10))

        pg.display.flip()
        clock.tick(60)

    pg.quit()


if __name__ == "__main__":
    args = tyro.cli(Args)
    main(args)
