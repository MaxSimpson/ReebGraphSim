# Window & OpenGl Includes
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


# Our libraries
import Terrain
import OpenGLHandler
import time

last_time = time.time()

openGLHandler = OpenGLHandler.OpenGLHandler()

terrain = Terrain.Terrain("hill.obj")
terrain.parse_file()

terrain.set_max_slope(30)
terrain.decompose()

print("Loading time:", round(time.time() - last_time,2), "s")

# FPS Counter
last_time = time.time()
frame_counter = 0

# Render loop
while not glfw.window_should_close(openGLHandler.get_window()):
  # Handle key input

  # OpenGL update per frame
  openGLHandler.update()

  # Rotate Camera
  openGLHandler.rotate_camera_circle()
  # time.sleep(0.05)

  # Render terrain model
  terrain.render()

  # Swap displayed window after re-rendering
  glfw.swap_buffers(openGLHandler.get_window())

  # Count FPS
  if time.time() - 5 < last_time:
    frame_counter += 1
  else:
    print("Avg FPS:",frame_counter/5)
    frame_counter = 0
    last_time = time.time()

glfw.terminate()