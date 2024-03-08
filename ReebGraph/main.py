# Window & OpenGl Includes
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Standard libraries
import time

# Our libraries
import Terrain
import OpenGLHandler
import ReebGraphConstruction

last_time = time.time()

openGLHandler = OpenGLHandler.OpenGLHandler()


terrain = Terrain.Terrain("2square.obj")
terrain.parse_file()

terrain.set_max_slope(30)
terrain.decompose()

reebGraph = ReebGraphConstruction.ReebGraph(terrain.get_vertices(), terrain.get_faces())

# Establish key callbacks
def key_callback(window, key, scancode, action, mods):
  if key == glfw.KEY_Q and action == glfw.PRESS:
    glfw.set_window_should_close(window, True)  # Close the window if 'Q' key is pressed
  elif key == glfw.KEY_W:
    terrain.change_max_slope(1)
  elif key == glfw.KEY_S:
    terrain.change_max_slope(-1)

# Set the key callback function
glfw.set_key_callback(openGLHandler.get_window(), key_callback)

print("Loading time:", round(time.time() - last_time,2), "s")

# FPS Counter
avg_fps_time = time.time()
last_frame_time = time.time()
frame_counter = 0

# Render loop
while not glfw.window_should_close(openGLHandler.get_window()):
  # OpenGL update per frame
  openGLHandler.update()

  # Calculate delta time
  delta_time = time.time() - last_frame_time
  # Rotate Camera
  openGLHandler.rotate_camera_circle(delta_time)

  # Time before rendering
  last_frame_time = time.time()

  # Render terrain model
  # terrain.render(wireframe=True)

  # Rendering Reeb Graph
  reebGraph.render() 

  # Swap displayed window after re-rendering
  glfw.swap_buffers(openGLHandler.get_window())

  # Count FPS
  if time.time() - 5 < avg_fps_time:
    frame_counter += 1
  else:
    # print("Avg FPS:",frame_counter/5)
    frame_counter = 0
    avg_fps_time = time.time()

glfw.terminate()