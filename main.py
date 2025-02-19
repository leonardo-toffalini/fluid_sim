import pygame as pg
import numpy as np
import tyro
from dataclasses import dataclass
from engine import add_source, draw_grid, dense_step, vel_step
import engine
from utils import pos_to_index, circle_source


@dataclass
class Args:
    WIDTH: int = 800
    HEIGHT: int = 600
    test_scenario: int = 1
    cell_size: int = 10


def main(args):
    pg.init()

    ### Setup
    # note, that grid has 2 extra rows and columns, these are the boundaries
    rows, cols = 2 + args.HEIGHT // args.cell_size, 2 + args.WIDTH // args.cell_size
    match args.test_scenario:
        case 1:
            grid, source, u_source, v_source = engine.test_scenario_1(rows, cols)
        case 2:
            grid, source, u_source, v_source = engine.test_scenario_2(rows, cols)
        case 3:
            grid, source, u_source, v_source = engine.test_scenario_3(rows, cols)
        case x:
            assert False, f"There is no test scenario with number {x}"

    u = np.zeros_like(grid)
    v = np.zeros_like(grid)

    screen = pg.display.set_mode((args.WIDTH, args.HEIGHT))
    pg.display.set_caption("Fluid simulation")
    font = pg.font.Font(None, 36)

    running = True
    clock = pg.time.Clock()

    while running:
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
            ui_source = circle_source(grid, mouse_i, mouse_j, radius=5, weight=20)
            grid = add_source(grid, ui_source, dt=1.0)

        # diff equation solver
        u, v = vel_step(u, v, u_source, v_source, visc=0.1, dt=1)
        grid = dense_step(grid, source, u, v, diff=0.0001, dt=1)
        draw_grid(grid, args.cell_size)

        # render fps counter on the screen
        fps = int(clock.get_fps())
        fps_text = font.render(f"FPS {fps}", True, (255, 255, 255))
        screen.blit(fps_text, (10, 10))

        pg.draw.circle(screen, (255, 0, 0), (mouse_x, mouse_y), 5)

        pg.display.flip()
        clock.tick(60)

    pg.quit()


if __name__ == "__main__":
    args = tyro.cli(Args)
    main(args)
