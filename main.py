import pygame as pg
import pygame.freetype
import numpy as np
import time
import tyro
from dataclasses import dataclass
from engine import add_source, GridDrawer, dense_step, vel_step, SolidsHandler
import utils
from enum import Enum
from utils import (
    pos_to_index,
    circle_source,
)


class DrawMode(Enum):
    SOURCE = 0
    PLACE_SOLID = 1
    ERASE_SOLID = 2


class VisType(Enum):
    DENS = 0
    VEL = 1


class DrawState:
    def __init__(self):
        self.mode = DrawMode.SOURCE
        self.mode_token = 'SOURCE'
        self.vis_type = VisType.DENS

    def handle_state_change(self, event):
        if event.type == pg.KEYUP:
            if event.key == pg.K_s:
                self.mode = DrawMode.SOURCE
                self.mode_token = 'SOURCE'
            elif event.key == pg.K_w:
                self.mode = DrawMode.PLACE_SOLID
                self.mode_token = 'SOLID'
            elif event.key == pg.K_e:
                self.mode = DrawMode.ERASE_SOLID
                self.mode_token = 'ERASE'
            elif event.key == pg.K_SPACE:
                if self.vis_type == VisType.DENS:
                    self.vis_type = VisType.VEL
                else:
                    self.vis_type = VisType.DENS

@dataclass
class Args:
    WIDTH: int = 1200
    HEIGHT: int = 900
    test_scenario: int = 1
    cell_size: int = 10
    diff: float = 1e-5
    visc: float = 1e-4
    debug_print: bool = False


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
    solids_handler = SolidsHandler(solids)
    draw_state = DrawState()

    running = True
    clock = pg.time.Clock()

    while running:
        t0 = time.perf_counter()
        dt = 1  # delta time should not be hardcoded
        mouse_x, mouse_y = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            else:
                draw_state.handle_state_change(event)

        screen.fill((6, 9, 10))

        ### Core logic
        # UI input
        buttons = pg.mouse.get_pressed()
        if buttons[0]:  # left mouse button
            mouse_j, mouse_i = pos_to_index(
                mouse_x, mouse_y, args.cell_size, args.WIDTH, args.HEIGHT
            )
            if draw_state.mode == DrawMode.SOURCE:
                ui_source = circle_source(grid, mouse_i, mouse_j, radius=5, weight=15)
                add_source(grid, ui_source, dt=dt)
            elif draw_state.mode == DrawMode.PLACE_SOLID:
                solids_handler.add_solid(mouse_i, mouse_j, 3)
            elif draw_state.mode == DrawMode.ERASE_SOLID:
                solids_handler.erase_solid(mouse_i, mouse_j, 3)

        # diff equation solver
        t1 = time.perf_counter()
        u, v = vel_step(u, v, u_source, v_source, solids_handler, visc=args.visc, dt=dt)
        t2 = time.perf_counter()
        grid = dense_step(grid, source, u, v, solids_handler, diff=args.diff, dt=dt)
        t3 = time.perf_counter()
        if draw_state.vis_type == VisType.DENS:
            grid_drawer.draw_grid(grid)
        elif draw_state.vis_type == VisType.VEL:
            grid_drawer.draw_velocity_field(u, v)

        t4 = time.perf_counter()
        # render fps counter on the screen
        fps = int(clock.get_fps())
        font.render_to(screen, (10, 10), f"FPS {fps}", (255, 255, 255))
        font.render_to(screen, (args.WIDTH - 100, 10), draw_state.mode_token, (255, 255, 255))

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
