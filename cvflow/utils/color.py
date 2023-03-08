from colorsys import rgb_to_hsv, hsv_to_rgb

import numpy as np


def generate_farthest_colors(n: int) -> list[tuple[float, float, float]]:
    """
    Generate n colors that are as far apart as possible in HSV space.

    Args:
        n: Number of colors to generate.

    Returns:
        List of RGB colors.
    """
    hues = np.linspace(0, 1, n, endpoint=False)
    colors = [hsv_to_rgb(h, 1, 1) for h in hues]
    colors = [(int(r * 255), int(g * 255), int(b * 255)) for r, g, b in colors]
    return colors
