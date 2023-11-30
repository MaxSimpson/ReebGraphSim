# STD Imports
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import scipy.ndimage as ndimage
import random

# Graph Sim Imports
import Surface
import Morse


def distance_from_ellipse(x, y, center_x, center_y, x_axis_scale, y_axis_scale):
  # Translate the point and ellipse to the origin
  translated_x = x - center_x
  translated_y = y - center_y
    
  # Calculate the distance from the translated point to the ellipse
  distance = np.sqrt((translated_x / x_axis_scale)**2 + (translated_y / y_axis_scale)**2)
    
  return distance


def plot_3d_function():
    # Keypress Callback
    def on_key(event):
      # Exit conditions
      if event.key == 'k' or event.key == 'escape':
        exit()
      

    # Simulation params
    x_length = 5
    y_length = 5

    # Options are: hills, flat, ripple, saddle, monkey saddle, egg crate, mobius strip, klein bottle, bowl
    surface_function = 'hills' 
    # Options are: ring, height, slope
    morse_function = 'slope'
    # Whether to include/render critical values at edges of surface
    critical_values_at_edges = False

    # Hill only
    number_of_hills = 3
    sigma = 3 # Peakedness low is less

    # Same random seed
    seed = random.randrange(1, 300)
    print("\tGenerating terrain - Seed: " + str(seed))

    # Number of hills
    number_of_hills = 3
    # Hill peakedness
    sigma = 3 


    # Generate Surface Values (For Rendering)
    x = np.linspace(-x_length, x_length, 31)
    y = np.linspace(-y_length, y_length, 31)

    X_surf, Y_surf = np.meshgrid(x, y)
    Z_surf = np.zeros_like(x)
     
    # Handle different surface function calls
    if surface_function == 'hills':
      Z_surf = Surface.generate_hills(number_of_hills, sigma, X_surf, Y_surf, seed)
    elif surface_function == 'flat':
      Z_surf = Surface.generate_flat(X_surf, Y_surf)
    elif surface_function == 'ripple':
      Z_surf = Surface.generate_ripple(X_surf, Y_surf)
    elif surface_function == 'saddle':
      Z_surf = Surface.generate_saddle(X_surf, Y_surf)
    elif surface_function == 'monkey saddle':
      Z_surf = Surface.generate_monkey_saddle(X_surf, Y_surf)
    elif surface_function == 'egg crate':
      Z_surf = Surface.generate_egg_crate(X_surf, Y_surf)
    elif surface_function == 'mobius strip':
      Z_surf = Surface.generate_mobius_strip(X_surf, Y_surf)
    elif surface_function == 'klein bottle':
      Z_surf = Surface.generate_klein_bottle(X_surf, Y_surf)
    elif surface_function == 'flat':
      Z_surf = Surface.generate_flat(X_surf, Y_surf)

    # Handle different morse function calls
    M_surf = np.zeros_like(X_surf)
    if morse_function == 'ring':
      M_surf = Morse.ring(X_surf, Y_surf, Z_surf)
    elif morse_function == 'height':
      M_surf = Morse.height(X_surf, Y_surf, Z_surf)
    elif morse_function == 'slope':
      M_surf = Morse.slope(X_surf, Y_surf, Z_surf)

    
    # Find the indices of the absolute min&max, local min&max, and saddle points
    # Absolutes

    abs_min_indices = (M_surf == ndimage.minimum_filter(M_surf, cval=np.inf if critical_values_at_edges else -np.inf, size=3, mode='constant'))
    abs_max_indices = (M_surf == np.max(M_surf))
    
    local_min_indices = None
    local_max_indices = None
    # Locals
    local_min_indices = np.logical_and(ndimage.minimum_filter(M_surf, cval=np.inf if critical_values_at_edges else -np.inf, size=3, mode='constant') == M_surf, ~abs_min_indices)
    local_min_indices = np.logical_and(ndimage.minimum_filter(M_surf, cval=np.inf, size=3, mode='constant') == M_surf, ~abs_min_indices)
    local_max_indices = np.logical_and(ndimage.maximum_filter(M_surf, cval=-np.inf, size=3, mode='constant') == M_surf, ~abs_max_indices)


    # Saddles
    grad_x, grad_y = np.gradient(M_surf)

    # Threshold because small numbers interfere like 1E29
    threshold = 0.000000001 
    critical_points = (np.abs(grad_x) < threshold) & (np.abs(grad_y) < threshold)
    
    hessian_xx, _ = np.gradient(grad_x)
    _, hessian_yy = np.gradient(grad_y)
    hessian_xy = np.gradient(grad_y)[0]
    discriminant = (hessian_xx * hessian_yy) - (hessian_xy**2)
    saddle_points = (discriminant < 0) & critical_points
    saddle_indices = np.nonzero(saddle_points)
    
    # Extract coordinates of minima, maxima, and saddle points
    # Minimas
    min_x, min_y, min_z = X_surf[abs_min_indices], Y_surf[abs_min_indices], Z_surf[abs_min_indices]
    local_min_x, local_min_y, local_min_z = X_surf[local_min_indices], Y_surf[local_min_indices], Z_surf[local_min_indices]
    
    # Maximas
    max_x, max_y, max_z = X_surf[abs_max_indices], Y_surf[abs_max_indices], Z_surf[abs_max_indices]
    local_max_x, local_max_y, local_max_z = X_surf[local_max_indices], Y_surf[local_max_indices], Z_surf[local_max_indices]
    
    # Saddles
    saddle_x, saddle_y, saddle_z = X_surf[saddle_indices], Y_surf[saddle_indices], Z_surf[saddle_indices]
    
    # Create the figure and 3D axes
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Callback for key preses
    fig.canvas.mpl_connect('key_press_event', on_key)
    
    # Plot the surface
    #surf = ax.plot_surface(X_surf, Y_surf, Z_surf, cmap='viridis', facecolors=cm.jet(color_func(X_surf, Y_surf, Z_surf)), rstride=1, cstride=1, alpha=0.5)
    surf = ax.plot_surface(X_surf, Y_surf, Z_surf, cmap='viridis', facecolors=cm.jet((M_surf-np.min(M_surf))/(np.max(M_surf)-np.min(M_surf))), rstride=1, cstride=1, alpha=0.5)
    
    # Draw points at the absolutes, locals, and saddles
    # ax.scatter(min_x, min_y, min_z, color='purple', edgecolors='black', s=75, label='Absolute Minima')
    ax.scatter(local_min_x, local_min_y, local_min_z, color='blue', edgecolors='black', s=75, label='Local Minima')


    # ax.scatter(max_x, max_y, max_z, color='red', edgecolors='black', s=75, label='Absolute Maxima')
    # ax.scatter(local_max_x, local_max_y, local_max_z, color='orange', edgecolors='black', s=75, label='Local Maxima')
    # ax.scatter(saddle_x, saddle_y, saddle_z, color="green", edgecolors='black', s=75, label='Saddle')
    
    # Color scale label
    cbar = fig.colorbar(surf, ax=ax, shrink=0.6, aspect=10)
    
    # Customize the plot (optional)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Morse Function Plot')

    # Show the plot
    plt.show()

# Main method
plot_3d_function()
