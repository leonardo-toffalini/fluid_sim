import numpy as np
from typing import Tuple


def fill_circle(arr, i, j, R, val):
    height, width = arr.shape
    y, x = np.ogrid[:height, :width]
    dist_from_center = np.sqrt((x - j) ** 2 + (y - i) ** 2)
    mask = dist_from_center <= R
    arr[mask] = val * dist_from_center[mask]
    return arr


def circle_source(
    grid: np.ndarray, mouse_i: int, mouse_j: int, radius: int = 5, weight: int = 20
):
    source = np.zeros_like(grid)
    return fill_circle(source, mouse_i, mouse_j, radius, weight)


def pos_to_index(pos_x, pos_y, cell_size, grid_width, grid_height):
    i = pos_x // cell_size
    j = pos_y // cell_size

    # Ensure the indices are within the grid bounds
    i = max(0, min(i, grid_width - 1))
    j = max(0, min(j, grid_height - 1))

    return i, j


def hue_to_rgb(p, q, t):
    if t < 0:
        t += 1
    if t > 1:
        t -= 1
    if t < 1 / 6:
        return p + (q - p) * 6 * t
    if t < 1 / 2:
        return q
    if t < 2 / 3:
        return p + (q - p) * (2 / 3 - t) * 6
    return p


def unsigned_byte(x: float) -> int:
    return min(max(int(x), 0), 255)


def hsl_to_rgb(h, s, l):
    h = h / 360.0
    s = s / 100.0
    l = l / 100.0

    if s == 0:
        r = g = b = l
    else:
        q = l * (1 + s) if l < 0.5 else l + s - l * s
        p = 2 * l - q
        r = hue_to_rgb(p, q, h + 1 / 3)
        g = hue_to_rgb(p, q, h)
        b = hue_to_rgb(p, q, h - 1 / 3)

    return unsigned_byte(r * 255), unsigned_byte(g * 255), unsigned_byte(b * 255)


def generate_perlin_noise_2d(shape, res):
    def f(t):
        return 6 * t**5 - 15 * t**4 + 10 * t**3

    delta = (res[0] / shape[0], res[1] / shape[1])
    d = (shape[0] // res[0], shape[1] // res[1])
    grid = np.mgrid[0 : res[0] : delta[0], 0 : res[1] : delta[1]].transpose(1, 2, 0) % 1

    # Gradients
    angles = 2 * np.pi * np.random.rand(res[0] + 1, res[1] + 1)
    gradients = np.dstack((np.cos(angles), np.sin(angles)))
    g00 = gradients[0:-1, 0:-1].repeat(d[0], 0).repeat(d[1], 1)
    g10 = gradients[1:, 0:-1].repeat(d[0], 0).repeat(d[1], 1)
    g01 = gradients[0:-1, 1:].repeat(d[0], 0).repeat(d[1], 1)
    g11 = gradients[1:, 1:].repeat(d[0], 0).repeat(d[1], 1)

    # Ramps
    n00 = np.sum(np.dstack((grid[:, :, 0], grid[:, :, 1])) * g00, 2)
    n10 = np.sum(np.dstack((grid[:, :, 0] - 1, grid[:, :, 1])) * g10, 2)
    n01 = np.sum(np.dstack((grid[:, :, 0], grid[:, :, 1] - 1)) * g01, 2)
    n11 = np.sum(np.dstack((grid[:, :, 0] - 1, grid[:, :, 1] - 1)) * g11, 2)

    # Interpolation
    t = f(grid)
    n0 = n00 * (1 - t[:, :, 0]) + t[:, :, 0] * n10
    n1 = n01 * (1 - t[:, :, 0]) + t[:, :, 0] * n11
    return np.sqrt(2) * ((1 - t[:, :, 1]) * n0 + t[:, :, 1] * n1)


def generate_fractal_noise_2d(shape, res, octaves=1, persistence=0.5):
    noise = np.zeros(shape)
    frequency = 1
    amplitude = 1
    for _ in range(octaves):
        noise += amplitude * generate_perlin_noise_2d(
            shape, (frequency * res[0], frequency * res[1])
        )
        frequency *= 2
        amplitude *= persistence
    return noise


def test_scenario_0(
    rows: int, cols: int
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Sets up an empty test scenario"""
    grid = np.zeros(shape=(rows, cols))
    u = np.zeros_like(grid)
    v = np.zeros_like(grid)
    source = np.zeros_like(grid)
    return grid, source, u, v


def test_scenario_1(
    rows: int, cols: int
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Sets up a test scenario where there is a strip of sources in the middle of the left edge,
    and there is only constant right directed, laminar wind.

    :return grid, source, u, v
    """
    grid = np.zeros(shape=(rows, cols))
    u = np.zeros_like(grid)
    v = np.ones_like(grid)
    source = np.zeros_like(grid)
    source[(rows // 2) - 3 : (rows // 2) + 3, 1] = 200

    return grid, source, u, v


def test_scenario_2(
    rows: int, cols: int
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Sets up a test scenario where there are three dot sources in the middle with no wind.

    Returns:
        grid, source, u, v
    """
    grid = np.zeros(shape=(rows, cols))
    u = np.zeros_like(grid)
    v = np.zeros_like(grid)
    source = np.zeros_like(grid)
    source[2 * rows // 3, cols // 2] = 200
    source[rows // 2, cols // 3] = 200
    source[rows // 2, 2 * cols // 3] = 200

    return grid, source, u, v


def test_scenario_3(
    rows: int, cols: int
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Sets up a test scenario where there is a strip of sources in the middle of the left edge,
    and there is right facing wind with perlin noise.

    Returns:
        grid, source, u, v
    """
    grid = np.zeros(shape=(rows, cols))
    u = np.zeros_like(grid)
    noise = generate_perlin_noise_2d(grid.shape, res=(2, 2))
    v = np.ones_like(grid) / 2 + noise
    source = np.zeros_like(grid)
    source[(rows // 2) - 3 : (rows // 2) + 3, 1] = 200

    return grid, source, u, v
