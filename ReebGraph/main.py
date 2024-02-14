# Window & OpenGl Includes
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Our libraries
import Terrain
import OpenGLHandler
import time


openGLHandler = OpenGLHandler.OpenGLHandler()

terrain = Terrain.Terrain("hill.obj")
terrain.parse_file()

# Render loop
while not glfw.window_should_close(openGLHandler.get_window()):
  # OpenGL update per frame
  openGLHandler.update()

  # Rotate Camera
  openGLHandler.rotate_camera_circle()
  time.sleep(0.05)

  # Render terrain model
  terrain.render()

  # Swap displayed window after re-rendering
  glfw.swap_buffers(openGLHandler.get_window())


glfw.terminate()