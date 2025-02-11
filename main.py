import pygame as pg
import numpy as np


def draw_grid(grid: np.ndarray, cell_width: int, screen: pg.Surface) -> None:
    rows, cols = grid.shape
    for i in range(rows):
        for j in range(cols):
            color = (grid[i, j], grid[i, j], grid[i, j])
            pg.draw.rect(
                screen,
                color,
                pg.Rect(i * cell_width, j * cell_width, cell_width, cell_width),
            )


def main():
    pg.init()

    WIDTH = 800
    HEIGHT = 600

    cell_width = 50
    rows, cols = WIDTH // cell_width, HEIGHT // cell_width
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
        draw_grid(grid, cell_width, screen)
        pg.display.flip()
        clock.tick(60)

    pg.quit()

    pass


if __name__ == "__main__":
    main()
