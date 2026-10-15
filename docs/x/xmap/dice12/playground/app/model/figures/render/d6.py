
from build123d import Vertex

from render.model import Model
from render.d import D

class D6(D):

    def __init__(self, model: Model):
        super().__init__(model)
        self.m = model
        self.base = self.cube()

    def cube(self):
        vertices = [
            Vertex(-self.m.edge / 2, -self.m.edge / 2,  self.m.edge / 2),
            Vertex(-self.m.edge / 2,  self.m.edge / 2,  self.m.edge / 2),
            Vertex( self.m.edge / 2,  self.m.edge / 2,  self.m.edge / 2),
            Vertex( self.m.edge / 2, -self.m.edge / 2,  self.m.edge / 2),
            Vertex(-self.m.edge / 2, -self.m.edge / 2, -self.m.edge / 2),
            Vertex(-self.m.edge / 2,  self.m.edge / 2, -self.m.edge / 2),
            Vertex( self.m.edge / 2,  self.m.edge / 2, -self.m.edge / 2),
            Vertex( self.m.edge / 2, -self.m.edge / 2, -self.m.edge / 2)
        ]
        top    = [3, 2, 1, 0]
        bottom = [4, 5, 6, 7]
        left   = [0, 1, 5, 4]
        right  = [2, 3, 7, 6]
        front  = [4, 7, 3, 0]
        back   = [1, 2, 6, 5]
        faces  = [top, right, front, left, back, bottom]

        return self.get(vertices, faces)
