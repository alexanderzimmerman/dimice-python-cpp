from scipy import interpolate
from matplotlib.mlab import griddata
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import field
import body

# @todo: plot frames with Paraview

def plot_frame(interpolator, data, old_state, state, step):
    xi_grid, yi_grid = grid_sample_points(data)
    ui = interpolator(xi_grid, yi_grid)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim(-2., 2.)
    plt.ylim(-2, 2.25)
    plt.gca().set_aspect('equal', adjustable='box')
    cp = plt.contour(xi_grid, yi_grid, ui.reshape(xi_grid.shape),
                     (0.8*field.temperature, field.material['melting temperature']),
                     colors=('k', 'b'))
    plt.clabel(cp, inline=True, fontsize=10)
    points = body.close_curve(body.get_hull_points(old_state))
    plt.plot(points[:, 0], points[:, 1], '--y', label='Old State')
    points = body.close_curve(body.get_hull_points(state))
    plt.plot(points[:, 0], points[:, 1], '-r', label='Current State')
    plt.legend()
    plt.title('Step '+str(step))
    plt.savefig('trajectory_frame_'+str(step))
    plt.cla()


def plot_contour_and_data(xi_grid, yi_grid, ui_grid, data):
    # Plot the structured sample
    plt.interactive(False)
    plt.subplot(1, 1, 1)
    plt.pcolor(xi_grid, yi_grid, ui_grid, cmap=cm.jet)
    plt.scatter(data[:, 0], data[:, 1], 10, data[:, 2], cmap=cm.jet)
    plt.axis('equal')
    plt.colorbar()
    plt.draw()
    plt.show()


def plot_interpolator_and_data(interpolator, data):
    xi_grid, yi_grid = grid_sample_points(data)
    query_points = np.column_stack((xi_grid.flatten(), yi_grid.flatten()))
    ui = interpolator(query_points)
    plot_contour_and_data(xi_grid, yi_grid, ui.reshape(xi_grid.shape), data)
    plt.show()


def grid_sample_points(data):
    # Interpolate data on to structured grid
    x = data[:, 0]
    y = data[:, 1]
    ni = 100
    xi = np.linspace(min(x), max(x), ni)
    yi = np.linspace(min(y), max(y), ni)
    xi_grid, yi_grid = np.meshgrid(xi, yi)
    return xi_grid, yi_grid


def make_interpolator(scattered_data, resolution=100, plot=False):
    # This is an inefficient an inaccurate substitute for natural neighbor interpolation on to scattered points.
    # Make a gridded natural neighbor interpolation
    data = scattered_data
    xi_grid, yi_grid = grid_sample_points(data)
    ui_grid = mlab.griddata(data[:, 0], data[:, 1], data[:, 2], xi_grid, yi_grid)  # Natural neighbor interpolation
    # Make an interpolator that can be called with scattered points
    # @todo: The natural neighbor interpolation looks great, and then this grid interpolator fails completely.
    # Or maybe the plotting wrong.
    xi = np.linspace(min(data[:, 0]), max(data[:, 0]), resolution)
    yi = np.linspace(min(data[:, 1]), max(data[:, 1]), resolution)
    interpolator = interpolate.RegularGridInterpolator(points=(xi, yi), values=ui_grid, bounds_error=False)
    if plot:
        ui_grid = interpolator(np.column_stack((xi_grid.flatten(), yi_grid.flatten())))
        plots.plot_contour_and_data(xi_grid, yi_grid, ui_grid.reshape(xi_grid.shape), data)
    return interpolator
