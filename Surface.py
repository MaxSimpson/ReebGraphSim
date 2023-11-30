# Imports
import numpy as np
import random

# Generates hills on a 2d mesh
#   num_hill - Number of hills to generate on the terrain
#   hill_peakedness - height of the hills to be generated (sigma)
#   x & y - Mesh of the surface to use as a basis
def generate_hills(num_hills, hill_peakedness, x, y, seed):
  terrain = np.zeros_like(x)
  random.seed(seed)

  x_range = (np.min(x), np.max(x))
  y_range = (np.min(y), np.max(y))

  # Generating hills in range  
  for i in range(num_hills):
    # Generate cordinates for hill
    x_cord = random.randrange(x_range[0], x_range[1])
    y_cord = random.randrange(y_range[0], y_range[1])

    # Add new hill to the mesh
    terrain += (np.exp(-((2*(x - x_cord)**2) + (2*(y - y_cord)**2)) / (2 * hill_peakedness**2)))
  
  return terrain

# Ripple 
def generate_ripple(x, y):
  return np.sin(np.sqrt(x**2 + y**2))
      
# Saddle
def generate_saddle(x, y):
  return x**2 - y**2
        
# Monkey saddle
def generate_monkey_saddle(x, y):
  return x**3 - 3*x*y**2
        
# Egg Crate
def generate_egg_crate(x, y):
  return np.cos(x) * np.cos(y)
        
# Mobius Strip
def generate_mobius_strip(x, y):
  return np.sin(y/2) * np.cos(x) + np.sin(x) * np.cos(y/2)

# Klein Bottle
def generate_klein_bottle(x, y):
  return np.cos(x) * (np.cos(x/2) * np.sin(y) - np.sin(x/2) * np.sin(2*y))

# Bowl
def generate_bowl(x, y):
  return x**2 + y**2 - 1



def generate_flat(x, y):
  return np.zeros_like(x)