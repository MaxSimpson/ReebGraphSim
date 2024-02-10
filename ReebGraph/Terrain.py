# Obj Library
import pywavefront

# OpenGL includes
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Terrain:
  def __init__ (self, file):
    # Store file location
    self.file = file

    # Terrain data
    self.vertices = None
    self.faces = None

  def parse_file(self):
    # Load OBJ file
    mesh = pywavefront.Wavefront(self.file, collect_faces=True)

    # Extract vertices, faces, and normals
    self.vertices = mesh.vertices
    self.faces = mesh.mesh_list[0].faces

  def render(self):
    # Draw the mesh
    glBegin(GL_TRIANGLES)
    for face in self.faces:
      glVertex3f(*self.vertices[face[0]])
      glVertex3f(*self.vertices[face[1]])
      glVertex3f(*self.vertices[face[2]])
    glEnd()