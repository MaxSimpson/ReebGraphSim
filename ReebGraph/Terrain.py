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
    self.face_angles = []
    self.max_slope = 45

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

  def clean_file(self):
    # Read the input .obj file
    with open(self.file, 'r') as f:
        lines = f.readlines()

    processed_lines = []
    for line in lines:
        if line.startswith('v '):
            vertex = line.strip().split()
            vertex = [f'{float(v):.4f}' for v in vertex[1:]]  # Skip the 'v'
            processed_line = 'v ' + ' '.join(vertex) + '\n'    # Re-add the 'v'
        else:
            processed_line = line
        processed_lines.append(processed_line)

    # Write the processed lines to the output file
    with open(self.file, 'w') as f:
        f.writelines(processed_lines)

  def parse_file(self):
    # Clean File
    self.clean_file()

    # Load OBJ file
    mesh = pywavefront.Wavefront(self.file, collect_faces=True)

    # Extract vertices, faces, and normals
    self.vertices = mesh.vertices
    self.faces = mesh.mesh_list[0].faces

    self.initialize()

  def set_max_slope(self, new_slope):
    self.max_slope = new_slope

  def insertion_sort(self):
    for i in range(1, len(self.faces)):
        key_angle = self.face_angles[i]
        key_face = self.faces[i]
        j = i - 1
        while j >= 0 and self.face_angles[j] > key_angle:
            self.face_angles[j + 1] = self.face_angles[j]
            self.faces[j + 1] = self.faces[j]
            j -= 1
        self.face_angles[j + 1] = key_angle
        self.faces[j + 1] = key_face



  def decompose(self):
    # Calculate normals
    for face in self.faces:
      self.face_angles.append(round((1 - np.dot(self.normals[face[3]],(0,1,0)))*90,2))

    # Sorts the normals so they are stored faster
    self.insertion_sort()

  def render(self):
    # Draw the mesh
    glBegin(GL_TRIANGLES)
    for i in range(len(self.faces)):
      if(self.face_angles[i] > self.max_slope): 
        break
      glNormal3f(*self.normals[self.faces[i][3]])
      glVertex3f(*self.vertices[self.faces[i][0]])
      glNormal3f(*self.normals[self.faces[i][3]])
      glVertex3f(*self.vertices[self.faces[i][1]])  
      glNormal3f(*self.normals[self.faces[i][3]])
      glVertex3f(*self.vertices[self.faces[i][2]])
    glEnd()