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

terrain = Terrain.Terrain("square.obj")
terrain.parse_file()

terrain.set_max_slope(30)
terrain.decompose()

reebGraph = ReebGraphConstruction.ReebGraph(terrain.get_vertices(), terrain.get_faces())

print("Loading time:", round(time.time() - last_time,2), "s")

# FPS Counter
avg_fps_time = time.time()
last_frame_time = time.time()
frame_counter = 0

# Render loop
while not glfw.window_should_close(openGLHandler.get_window()):
  # Handle key input
  # TODO!!!

  # OpenGL update per frame
  openGLHandler.update()

  # Calculate delta time
  delta_time = time.time() - last_frame_time
  # Rotate Camera
  openGLHandler.rotate_camera_circle(delta_time)

  # Time before rendering
  last_frame_time = time.time()

  # Render terrain model
  terrain.render()

  # Swap displayed window after re-rendering
  glfw.swap_buffers(openGLHandler.get_window())

  # Count FPS
  if time.time() - 5 < avg_fps_time:
    frame_counter += 1
  else:
    print("Avg FPS:",frame_counter/5)
    frame_counter = 0
    avg_fps_time = time.time()

glfw.terminate()