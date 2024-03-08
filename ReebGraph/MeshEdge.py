class MeshEdge:
  def __init__(self, start_index : int, end_index : int):
    self.start = start_index  # Source vertex index
    self.end = end_index      # Target vertex index
    self.number_of_triangles: int = 0   # Number of triangles in mesh edge
    self.arc_sets: list[int] = [] # Indices of RG Edges that map to this edge

  # Check that the both mesh edges contain the same start and end
  def __eq__(self, other: object) -> bool:
    return other.start == self.start and other.end == self.end

  # To string
  def __str__(self) -> str:
    return "(" + str(self.start) + " " + str(self.end) + " " + str(self.arc_sets) + ")"
  
  def adjust_reeb_indices(self, _a1 : int):
    print("\t\t\tadjusting indicies down", self.arc_sets)
    for i in range(len(self.arc_sets)):
      if self.arc_sets[i] > _a1:
        self.arc_sets[i] -= 1
    print("\t\t\tafter adj down:", self.arc_sets)
        
  
  # Inserts a arc index into the arc_set
  def insert(self, index : int) -> None:
    print("\t\tInserting",index, "into", self.arc_sets)
    self.arc_sets.append(index)
    print("\t\t", self.arc_sets)
  
  # Erases an arc_set index
  def erase(self, index : int) -> None:
    print("\t\tErasing", index, "from", self.arc_sets)
    self.arc_sets.remove(index)
    print("\t\t", self.arc_sets)

  
  # Returns the arc set
  def get_arc_set(self) -> list[int]:
    return self.arc_sets
  
  # Return the starting point of mesh edge
  def get_start(self) -> int:
    return self.start
  
  # Return the end of the mesh edge
  def get_end(self) -> int:
    return self.end
  
  # Increment number of triangles
  def increment_number_of_triangles(self) -> None:
    self.number_of_triangles += 1

  def decrement_number_of_triangles(self) -> None:
    self.number_of_triangles -= 1

  # Addes triangles to the current arc set
  def add_triangles(self, new_triangles : list[int]) -> None:
    self.arc_sets.extend(new_triangles)