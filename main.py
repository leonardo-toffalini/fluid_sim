import pygame as pg
import pygame.freetype
import numpy as np
import time
import tyro
from dataclasses import dataclass
from engine import add_source, GridDrawer, dense_step, vel_step, Boundary, BoundaryOld
import utils
from utils import (
    pos_to_index,
    circle_source,
)


@dataclass
class Args:
    WIDTH: int = 800
    HEIGHT: int = 600
    test_scenario: int = 1
    cell_size: int = 10
    diff: float = 1e-6
    visc: float = 1e-4
    debug_print: bool = False
    vis_type: str = "dens"


def main(args):
    pygame.freetype.init()

    ### Setup
    # note, that grid has 2 extra rows and columns, these are the boundaries
    rows, cols = 2 + args.HEIGHT // args.cell_size, 2 + args.WIDTH // args.cell_size

    grid, source, u_source, v_source, solids = utils.get_test_scenario(
        args.test_scenario, rows, cols
    )

    u = np.zeros_like(grid)
    v = np.zeros_like(grid)

    screen = pg.display.set_mode((args.WIDTH, args.HEIGHT))
    pg.display.set_caption("Fluid simulation")
    font = pygame.freetype.SysFont("monospace", 26)
    grid_drawer = GridDrawer(rows, cols, args.cell_size)
    boundary = Boundary(solids)

    running = True
    clock = pg.time.Clock()

    while running:
        t0 = time.perf_counter()
        dt = 1  # delta time should not be hardcoded
        mouse_x, mouse_y = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill((6, 9, 10))

        ### Core logic
        # UI input
        buttons = pg.mouse.get_pressed()
        if buttons[0]:  # left mouse button
            mouse_j, mouse_i = pos_to_index(
                mouse_x, mouse_y, args.cell_size, args.WIDTH, args.HEIGHT
            )
            ui_source = circle_source(grid, mouse_i, mouse_j, radius=3, weight=12)
            add_source(grid, ui_source, dt=dt)

        # diff equation solver
        t1 = time.perf_counter()
        u, v = vel_step(u, v, u_source, v_source, boundary, visc=args.visc, dt=dt)
        t2 = time.perf_counter()
        grid = dense_step(grid, source, u, v, boundary, diff=args.diff, dt=dt)
        t3 = time.perf_counter()
        if args.vis_type == "dens":
            grid_drawer.draw_grid(grid)
        elif args.vis_type == "vel":
            grid_drawer.draw_velocity_field(u, v)

        t4 = time.perf_counter()
        # render fps counter on the screen
        fps = int(clock.get_fps())
        font.render_to(screen, (10, 10), f"FPS {fps}", (255, 255, 255))

        if args.debug_print:

            def print_time(text, time, row, tab=15):
                font.render_to(
                    screen,
                    (10, 10 + row * 30),
                    f"{text}:{' '* (tab - len(text))}{time * 1e3:5.2f}ms",
                    (255, 255, 255),
                )

            print_time("UI handle time", t1 - t0, 1)
            print_time("vel_step time", t2 - t1, 2)
            print_time("dense_step time", t3 - t2, 3)
            print_time("render time", t4 - t3, 4)

        pg.display.flip()
        clock.tick(120)

    pg.quit()


if __name__ == "__main__":
    args = tyro.cli(Args)
    main(args)
