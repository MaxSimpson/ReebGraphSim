# Imports
import numpy as np
import scipy.ndimage as ndimage

def height(x, y, z):
  return z
   
def slope(x, y, z):
  # Compute partial derivatives of height function
  dz_dx = np.gradient(z, axis=0)
  dz_dy = np.gradient(z, axis=1)
  
  # Compute slope magnitude
  slope_magnitude = np.sqrt(dz_dx**2 + dz_dy**2)
  
  return slope_magnitude

def ring(X, Y, Z): 
  # Get all local and abs maxima from the terrain Z values
  hill_indices = ndimage.maximum_filter(Z, cval=-np.inf, size=3, mode='constant') == Z
  
  # Store all xyz's in arrays
  # Iterate through them and add them to the morse function as we go
  local_points = (X[hill_indices],Y[hill_indices],Z[hill_indices])
  
  # Set morse function to nothing...
  M = np.zeros_like(Z)
  
  radii = 2
  a = 1
  b = 1
  theta = 0
  
  for i in range(len(local_points[0])):
    x,y,z = local_points[0][i], local_points[1][i], local_points[2][i] # Extracting xyz values

    ring = np.exp(-(((X - x)**2 / (a**2)) + ((Y - y)**2 / (b**2))))

    M += ring
  
  return M