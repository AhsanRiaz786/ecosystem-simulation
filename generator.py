import itertools
import numpy as np
import random as rnd
import matplotlib.pyplot as plt
from settings import *

def __perlin__(x: np.ndarray, y: np.ndarray, seed: int = 0) -> list:
    """Generates Perlin noise for given x and y coordinates.

    Args:
        x (numpy.ndarray): The x coordinates.
        y (numpy.ndarray): The y coordinates.
        seed (int, optional): The random seed. Defaults to 0.

    Returns:
        list: The generated Perlin noise values.
    """
    np.random.seed(seed)
    p = np.arange(256, dtype=int)  # permutation array
    np.random.shuffle(p)  # shuffle shuffle permutations
    p = np.stack(
        [p, p]
    ).flatten()  # 2d array turned 1d for easy dot product interpolations

    xg, yg = x.astype(int), y.astype(int)  # grid coords
    xv, yv = x - xg, y - yg  # distance vector coords

    # gradient vector coordinates top left, top right, bottom left, bottom right
    tl = __gradient__(p[p[xg] + yg], xv, yv)
    tr = __gradient__(p[p[xg] + yg + 1], xv, yv - 1)
    bl = __gradient__(p[p[xg + 1] + yg + 1], xv - 1, yv - 1)
    br = __gradient__(p[p[xg + 1] + yg], xv - 1, yv)

    f1, f2 = __fade__(xv), __fade__(yv)  # fade function

    # linear interpolation
    x1 = __lerp__(tl, br, f1)
    x2 = __lerp__(tr, bl, f1)
    return __lerp__(x1, x2, f2)

def __lerp__(a: float, b: float, x: float) -> float:
    """Linear interpolation.

    Args:
        a (float): The start value.
        b (float): The end value.
        x (float): The interpolation factor.

    Returns:
        float: The interpolated value.
    """
    return a + x * (b - a)

def __fade__(t: float) -> float:
    """Calculates the fade value for Perlin noise.

    Args:
        t (float): The input value.

    Returns:
        float: The calculated fade value.
    """
    return 6 * t**5 - 15 * t**4 + 10 * t**3

def __gradient__(h: int, x: float, y: float):
    """Calculates the gradient vectors and the dot product.

    Args:
        h (int): The hash value.
        x (float): The x coordinate.
        y (float): The y coordinate.
    """
    vectors = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])
    g = vectors[h % 4]
    return g[:, :, 0] * x + g[:, :, 1] * y

def generate_plot(gseed: int = None) -> list:
    """Generates a plot of Perlin noise.

    Args:
        gseed (int, optional): The random seed in case a map needs to be recreated. Defaults to none.

    Returns:
        list: The generated plot.
    """
    p = np.zeros((50, 50))
    for i in range(4):
        freq = 2**i
        lin = np.linspace(0, freq, 50, endpoint=False)
        x, y = np.meshgrid(lin, lin)
        seed = rnd.randint(0, 999999999) if gseed is None else gseed
        p = __perlin__(x, y, seed=seed) / freq + p

    return p

def generate_map(gseed: int = None) -> list:
    """Generates a map using Perlin noise.

    Args:
        gseed (int, optional): The random seed in case a map needs to be recreated. Defaults to none.

    Returns:
        list: The generated map.
    """
    MIN_LAND_PERCENT = 0.65  # Minimum percentage of land tiles required

    while True:
        p = generate_plot(gseed)
        randmap = np.zeros((50, 50))
        land_tiles = []
        for y, x in itertools.product(range(50), range(50)):
            if -0.05 < p[y][x] < 0.4:
                randmap[y][x] = 2.0
                land_tiles.append((y, x))
            else:
                randmap[y][x] = 5.0

        land_percent = len(land_tiles) / (50 * 50)
        if land_percent >= MIN_LAND_PERCENT:
            break

    b_needed = int(len(land_tiles) * B_PERCENT)
    h_needed = int(len(land_tiles) * H_PERCENT)
    c_needed = int(len(land_tiles) * C_PERCENT)
    o_needed = int(len(land_tiles) * O_PERCENT)
    for _ in range(b_needed):
        coord = rnd.choice(land_tiles)
        land_tiles.remove(coord)
        randmap[coord[0]][coord[1]] = 0.0

    for _ in range(h_needed):
        coord = rnd.choice(land_tiles)
        land_tiles.remove(coord)
        randmap[coord[0]][coord[1]] = 3.0

    for _ in range(c_needed):
        coord = rnd.choice(land_tiles)
        land_tiles.remove(coord)
        randmap[coord[0]][coord[1]] = 1.0

    for _ in range(o_needed):
        coord = rnd.choice(land_tiles)
        land_tiles.remove(coord)
        randmap[coord[0]][coord[1]] = 4.0

    return randmap

def main() -> None:
    """Main function to generate and display a plot of Perlin noise."""
    p = generate_plot()
    plt.imshow(p, origin="upper")
    plt.show()

if __name__ == "__main__":
    main()