import numpy as np 

class Graph():
  def __init__(self, vertices_list=[]):
    self.vertices = np.array(vertices_list)
    self.edges = np.zeros(shape=(len(self.vertices), len(self.vertices)))

  def get_adjacents(self, vertice_index):
    """
      Using the self.edges return a np.array with the index of the 
    vertices that are adjacent of the "vertice_index" of the paramenter.
    """
    adjacents = []
    for index in len(self.edges):
      if self.edges[vertice_index][index] == 1:
        adjacents.append(index)
    return np.array(adjacents)

  def greed(self):
    pass

  def ldo(self):
    pass

  def sdo(self):
    pass