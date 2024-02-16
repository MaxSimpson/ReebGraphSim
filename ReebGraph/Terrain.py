# Obj Library
import pywavefront

# OpenGL includes
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Numpy include
import numpy as np

class Terrain:
  def __init__ (self, file):
    # Store file location
    self.file = file

    # Terrain data
    self.vertices = None
    self.faces = None
    self.normals = []

  def calculate_face_normal(self, vertex1, vertex2, vertex3):
    # Calculate two vectors from the vertices
    vector1 = np.array(vertex2) - np.array(vertex1)
    vector2 = np.array(vertex3) - np.array(vertex1)

    # Calculate the cross product of the two vectors
    cross_product = np.cross(vector1, vector2)

    # Normalize the resulting vector to get the face normal
    face_normal = cross_product / np.linalg.norm(cross_product)

    return tuple(face_normal)

  # Compute normals
  def initialize(self):
    for i in range(len(self.faces)):
      self.normals.append(self.calculate_face_normal(self.vertices[self.faces[i][0]], self.vertices[self.faces[i][1]], self.vertices[self.faces[i][2]]))
      self.faces[i] = (*self.faces[i], len(self.normals) - 1)


  def parse_file(self):
    # Load OBJ file
    mesh = pywavefront.Wavefront(self.file, collect_faces=True)

    # Extract vertices, faces, and normals
    self.vertices = mesh.vertices
    self.faces = mesh.mesh_list[0].faces

    self.initialize()


  def render(self):
    # Draw the mesh
    glBegin(GL_TRIANGLES)
    for face in self.faces:
      glNormal3f(*self.normals[face[3]])
      glVertex3f(*self.vertices[face[0]])
      glNormal3f(*self.normals[face[3]])
      glVertex3f(*self.vertices[face[1]])
      glNormal3f(*self.normals[face[3]])
      glVertex3f(*self.vertices[face[2]])
    glEnd()