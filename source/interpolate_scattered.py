from matplotlib import mlab
from scipy import interpolate
import numpy as np
import plots
import interpolate_structured


def make_interpolator(scattered_data, resolution=100, plot=False):
    # This is an inefficient an inaccurate substitute for natural neighbor interpolation on to scattered points.
    # Make a gridded natural neighbor interpolation
    data = scattered_data
    xi_grid, yi_grid = interpolate_structured.grid_sample_points(data)
    ui_grid = mlab.griddata(data[:, 0], data[:, 1], data[:, 2], xi_grid, yi_grid)  # Natural neighbor interpolation
    # Make an interpolator that can be called with scattered points
    xi = np.linspace(min(data[:, 0]), max(data[:, 0]), resolution)
    yi = np.linspace(min(data[:, 1]), max(data[:, 1]), resolution)
    interpolator = interpolate.RegularGridInterpolator((xi, yi), ui_grid, bounds_error=False)
    if plot:
        plots.plot_contour_and_data(xi_grid, yi_grid, ui_grid, data)
    return interpolator
