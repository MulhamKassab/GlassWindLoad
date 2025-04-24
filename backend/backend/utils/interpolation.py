import numpy as np
from scipy.interpolate import griddata

def interpolate_nfl_griddata(length, width, ar, json_x, json_y, json_nfl):
    """
    Interpolates the NFL value at (length, width) using griddata.

    Args:
        length (float): Glass length (normalized)
        width (float): Glass width (normalized)
        ar (float): Aspect ratio = length / width
        json_x (list): List of X values from NFL JSON
        json_y (list): List of Y values from NFL JSON
        json_nfl (list): Corresponding NFL values

    Returns:
        tuple: (interpolated_nfl, xi, yi, zi)
            - interpolated_nfl: float or NaN
            - xi, yi: 2D meshgrid
            - zi: Interpolated surface grid
    """
    # Force length to be the longer side just in case (redundant safety)
    if length < width:
        length, width = width, length

    points = np.array(list(zip(json_x, json_y)))
    values = np.array(json_nfl)

    interpolated_nfl = griddata(points, values, (length, width), method='cubic')

    # Create mesh grid for visualization if needed
    xi = np.linspace(min(json_x), max(json_x), 100)
    yi = np.linspace(min(json_y), max(json_y), 100)
    xi, yi = np.meshgrid(xi, yi)
    zi = griddata(points, values, (xi, yi), method='cubic')

    return interpolated_nfl, xi, yi, zi
