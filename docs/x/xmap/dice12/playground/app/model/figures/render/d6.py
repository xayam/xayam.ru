
from build123d import Vertex, Edge, Face, Wire, Shell, Solid

from render.model import Model
from render.d import D

class D6(D):

    def __init__(self, model: Model):

        self.m = model
        self.base = self.cube()

    def cube(self):
        
        vertices = [
            Vertex(0.0, 0.0, self.m.edge),
            Vertex(0.0, self.m.edge, self.m.edge),
            Vertex(self.m.edge, self.m.edge, self.m.edge),
            Vertex(self.m.edge, 0.0, self.m.edge),
            Vertex(0.0, 0.0, 0.0),
            Vertex(0.0, self.m.edge, 0.0),
            Vertex(self.m.edge, self.m.edge, 0.0),
            Vertex(self.m.edge, 0.0, 0.0)
        ]
        center = Vertex(self.m.edge / 2, self.m.edge / 2, self.m.edge / 2)
        top = [3, 2, 1, 0]
        bottom = [4, 5, 6, 7]
        left = [0, 1, 5, 4]
        right = [2, 3, 7, 6]
        front = [4, 7, 3, 0]
        back = [1, 2, 6, 5]
        faces = [top, right, front, left, back, bottom]
        pieces = [[
            (center, vertices[piece[p-1]], vertices[piece[p]])
            for p in range(len(piece))
            ] 
            for piece in faces]
        return self.get(pieces, vertices, faces)
