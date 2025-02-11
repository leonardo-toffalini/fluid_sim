import pygame as pg
import numpy as np


def draw_grid(grid: np.ndarray, cell_width: int) -> None:
    screen = pg.display.get_surface()
    grid_height, grid_width = grid.shape

    for y in range(grid_height):
        for x in range(grid_width):
            color = (grid[y, x], grid[y, x], grid[y, x])
            cell = pg.Rect(x * cell_width, y * cell_width, cell_width, cell_width)
            pg.draw.rect(screen, color, cell)


def main():
    pg.init()

    WIDTH = 800
    HEIGHT = 600

    cell_width = 50
    rows, cols = HEIGHT // cell_width, WIDTH // cell_width
    low, high = 25, 225
    grid = np.random.randint(low, high, size=(rows, cols))

    screen = pg.display.set_mode((WIDTH, HEIGHT))
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
        draw_grid(grid, cell_width)
        pg.display.flip()
        clock.tick(60)

    pg.quit()

    pass


if __name__ == "__main__":
    main()
