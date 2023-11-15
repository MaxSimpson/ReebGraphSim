import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
from matplotlib.animation import FuncAnimation
import scipy.ndimage as ndimage

def distance_from_ellipse(x, y, center_x, center_y, x_axis_scale, y_axis_scale):
  # Translate the point and ellipse to the origin
  translated_x = x - center_x
  translated_y = y - center_y
    
  # Calculate the distance from the translated point to the ellipse
  distance = np.sqrt((translated_x / x_axis_scale)**2 + (translated_y / y_axis_scale)**2)
    
  return distance


def plot_3d_function():
    sigma = 1
    curr_level = 0
    # Surface Function
    def surface_func(x, y):
        #terrain = (np.exp(-(x**2 + y**2) / (2 * sigma**2))) + np.sin(x)
        terrain = (np.exp(-((2*x**2) + (2*y**2)) / (2 * sigma**2)))
        
        # Ripple 
        #terrain = np.sin(np.sqrt(x**2 + y**2))
        
        # Saddle
        #terrain = x**2 - y**2
        
        # Monkey saddle
        #terrain = x**3 - 3*x*y**2
        
        # Egg Crate
        #terrain = np.cos(x) * np.cos(y)
        
        # Mobius Strip
        #terrain = np.sin(y/2) * np.cos(x) + np.sin(x) * np.cos(y/2)

        # Klein Bottle
        #terrain = np.cos(x) * (np.cos(x/2) * np.sin(y) - np.sin(x/2) * np.sin(2*y))

        # Bowl
        #terrain = x**2 + y**2 - 1
        
        # Inverted Normal
        #terrain = 1 - np.exp(-(x**2 + y**2) / (2 * sigma**2))
        
        #terrain = np.abs(np.sin(np.sqrt(x**2 + y**2)) / (np.sqrt(x**2 + y**2)))
        
        #terrain = np.ones_like(x)
        
        #crater_center_x = 0.5
        #crater_center_y = 0.5
        #crater_radius = 0.3
        #terrain = np.exp(-((x - crater_center_x)**2 + (y - crater_center_y)**2) / (2 * sigma**2))
        
        return terrain
    
    # Morse Function
    def morse_func(X, Y, Z):
      
      # Ripple (WIP REPLACE LATER)
      #M = np.sin(np.sqrt(x**2 + y**2))
      
      # Max's Morse Function
      
      # Get all local and abs maxima from the terrain Z values
      hill_indices = ndimage.maximum_filter(Z, cval=-np.inf, size=3, mode='constant') == Z
      
      # Store all xyz's in arrays
      # Iterate through them and add them to the morse function as we go
      local_points = (X[hill_indices],Y[hill_indices],Z[hill_indices])
      
      # Set morse function to nothing...
      M = np.zeros_like(Z)
      
      radii = 3
      a = 5
      b = 10
      theta = 0
      
      for i in range(len(local_points[0])):
        x,y,z = local_points[0][i], local_points[1][i], local_points[2][i] # Extracting xyz values
        distance = np.sqrt((X - x)**2 + (Y - y)**2)
        ring = np.exp(-(((X - x)**2 / (a**2)) + ((Y - y)**2 / (b**2))))

        M += ring
      
      
        #ring = np.exp(-((distance - 3)**2) / (2 * 2**2))
      
      return M
  
    # Keypress Callback
    def on_key(event):
      nonlocal curr_level

      # Check if the pressed key is left arrow
      if event.key == 'left':
          curr_level -= 0.1

      # Check if the pressed key is right arrow
      elif event.key == 'right':
          curr_level += 0.1
          
      elif event.key == 'k':
        exit()

    # Simulation params
    x_length = 5
    y_length = 5

    # Generate Surface Values (For Rendering)
    x = np.linspace(-x_length, x_length, 51)
    y = np.linspace(-y_length, y_length, 51)
    X_surf, Y_surf = np.meshgrid(x, y)
    Z_surf = surface_func(X_surf, Y_surf)
    M_surf = morse_func(X_surf, Y_surf, Z_surf)
    
    # Generate Morse Values (For Computation)
    x = np.linspace(-x_length, x_length, 501)
    y = np.linspace(-y_length, y_length, 501)
    X_morse, Y_morse = np.meshgrid(x, y)
    Z_morse = surface_func(X_morse, Y_morse)
    M_morse = morse_func(X_morse, Y_morse, Z_morse)
    
    # Find the indices of the absolute min&max, local min&max, and saddle points
    # Abs
    abs_min_indices = (M_morse == np.min(M_morse))
    abs_max_indices = (M_morse == np.max(M_morse))
    
    # Local
    local_min_indices = np.logical_and(ndimage.minimum_filter(M_morse, cval=np.inf, size=3, mode='constant') == M_morse, ~abs_min_indices)
    local_max_indices = np.logical_and(ndimage.maximum_filter(M_morse, cval=-np.inf, size=3, mode='constant') == M_morse, ~abs_max_indices)

    # Saddle
    grad_x, grad_y = np.gradient(M_morse)

    threshold = 0.000000001 
    critical_points = (np.abs(grad_x) < threshold) & (np.abs(grad_y) < threshold)
    
    hessian_xx, _ = np.gradient(grad_x)
    _, hessian_yy = np.gradient(grad_y)
    hessian_xy = np.gradient(grad_y)[0]
    discriminant = (hessian_xx * hessian_yy) - (hessian_xy**2)
    saddle_points = (discriminant < 0) & critical_points
    saddle_indices = np.nonzero(saddle_points)
    
    # Extract coordinates of minima, maxima, and saddle points
    min_x, min_y, min_z = X_morse[abs_min_indices], Y_morse[abs_min_indices], Z_morse[abs_min_indices]
    max_x, max_y, max_z = X_morse[abs_max_indices], Y_morse[abs_max_indices], Z_morse[abs_max_indices]
    local_min_x, local_min_y, local_min_z = X_morse[local_min_indices], Y_morse[local_min_indices], Z_morse[local_min_indices]
    local_max_x, local_max_y, local_max_z = X_morse[local_max_indices], Y_morse[local_max_indices], Z_morse[local_max_indices]
    saddle_x, saddle_y, saddle_z = X_morse[saddle_indices], Y_morse[saddle_indices], Z_morse[saddle_indices]
    
    # Create the figure and 3D axes
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Callback for key preses
    fig.canvas.mpl_connect('key_press_event', on_key)
    
    # Level Set Lines (Based on Morse Function instead of Z)
    contour = ax.contour(X_surf, Y_surf, Z_surf, levels=[(np.max(Z_surf)+np.min(Z_surf))/2], colors='black', linewidths=1)

    # Plot the surface
    #surf = ax.plot_surface(X_surf, Y_surf, Z_surf, cmap='viridis', facecolors=cm.jet(color_func(X_surf, Y_surf, Z_surf)), rstride=1, cstride=1, alpha=0.5)
    surf = ax.plot_surface(X_surf, Y_surf, Z_surf, cmap='viridis', facecolors=cm.jet((M_surf-np.min(M_surf))/(np.max(M_surf)-np.min(M_surf))), rstride=1, cstride=1, alpha=0.5)
    
    # Draw points at the absolutes, locals, and saddles
    # ax.scatter(min_x, min_y, min_z, color='purple', edgecolors='black', s=75, label='Absolute Minima')
    # ax.scatter(max_x, max_y, max_z, color='red', edgecolors='black', s=75, label='Absolute Maxima')
    # ax.scatter(local_min_x, local_min_y, local_min_z, color='blue', edgecolors='black', s=75, label='Local Minima')
    # ax.scatter(local_max_x, local_max_y, local_max_z, color='orange', edgecolors='black', s=75, label='Local Maxima')
    # ax.scatter(saddle_x, saddle_y, saddle_z, color="green", edgecolors='black', s=75, label='Saddle')
    
    start_level = np.min(Z_surf)+0.01
    end_level = np.max(Z_surf)-0.01
    curr_level = (start_level+end_level)/2
    def update(frame):
      nonlocal curr_level, start_level, end_level, contour
      if curr_level > end_level:
        curr_level = end_level
      elif curr_level < start_level:
        curr_level = start_level
    
      for c in contour.collections:
        c.remove()

      contour = ax.contour(X_surf, Y_surf, Z_surf, levels=[curr_level], colors='black', linewidths=2)
        
    # Create animation
    animation = FuncAnimation(fig, update, interval=10)
    
    # Color scale label
    cbar = fig.colorbar(surf, ax=ax, shrink=0.6, aspect=10)
    
    # Customize the plot (optional)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Morse Function Plot')

    # Show the plot
    plt.show()

# Call the function to generate and display the plot
plot_3d_function()
