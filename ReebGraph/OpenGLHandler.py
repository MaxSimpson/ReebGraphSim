import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class OpenGLHandler:
  def __init__(self):
    # Camera coordinates
    self.camera_coordinates = [0, 0, 5]
    self.camera_target = [0, 0, 0]

    # Initialize GLFW
    if not glfw.init():
      raise Exception("GLFW initialization failed")

    # Set window parameters
    width, height = 800, 600
    self.window = glfw.create_window(width, height, "OpenGL Window", None, None)
    if not self.window:
      glfw.terminate()
      raise Exception("Failed to create GLFW window")

    glfw.make_context_current(self.window)

    glEnable(GL_DEPTH_TEST)

  def get_window(self):
    return self.window
  
  def update(self):
    glfw.poll_events()

    # Clear the screen and depth buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Set up projection matrix
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 800 / 600, 0.1, 100)

    # Set up view matrix
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(*self.camera_coordinates, 0, 0, 0, 0, 1, 0)

    # Set up lighting
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, [0, 1, 1, 0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])

    # Set material properties
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

  def rotate_camera(self):
    self.camera_coordinates[1] += 0.01