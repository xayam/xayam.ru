import math
from build123d import Vertex

from render.model import Model
from render.d import D

class D12(D):
    def __init__(self, model: Model):
        super().__init__(model)
        self.m = model
        self.rotate_angle = 58.0
        self.base = self.dodecahedron()

    def dodecahedron(self):
        phi = (1.0 + math.sqrt(5.0)) / 2.0
        s = (phi / 2.0) * self.m.edge
        vertices = [
            Vertex(     s,      s,      s), #  0  
            Vertex(     s,      s,     -s), #  1 
            Vertex(     s,     -s,      s), #  2  
            Vertex(     s,     -s,     -s), #  3 
            Vertex(    -s,      s,      s), #  4 
            Vertex(    -s,      s,     -s), #  5  
            Vertex(    -s,     -s,      s), #  6 
            Vertex(    -s,     -s,     -s), #  7  
            Vertex(     0,  s*phi,  s/phi), #  8 
            Vertex(     0,  s*phi, -s/phi), #  9  
            Vertex(     0, -s*phi,  s/phi), # 10 
            Vertex(     0, -s*phi, -s/phi), # 11 
            Vertex( s/phi,      0,  s*phi), # 12 
            Vertex( s/phi,      0, -s*phi), # 13 
            Vertex(-s/phi,      0,  s*phi), # 14 
            Vertex(-s/phi,      0, -s*phi), # 15 
            Vertex( s*phi,  s/phi,      0), # 16 
            Vertex( s*phi, -s/phi,      0), # 17
            Vertex(-s*phi,  s/phi,      0), # 18 
            Vertex(-s*phi, -s/phi,      0)  # 19 
        ]
        vertices = [vertice for vertice in vertices]
        faces = [
            [ 0, 12,  2, 17, 16], #  0: противоположна грани  6
            [11,  7, 15, 13,  3], #  1: противоположна грани  7
            [ 0, 16,  1,  9,  8], #  2: противоположна грани  8
            [ 1, 13, 15,  5,  9], #  3: противоположна грани  9
            [ 1, 16, 17,  3, 13], #  4: противоположна грани 10 король?
            [ 2, 10, 11,  3, 17], #  5: противоположна грани 11
            [ 5, 15,  7, 19, 18], #  6: противоположна грани  0
            [ 0,  8,  4, 14, 12], #  7: противоположна грани  1
            [19,  7, 11, 10,  6], #  8: противоположна грани  2
            [ 2, 12, 14,  6, 10], #  9: противоположна грани  3
            [ 4, 18, 19,  6, 14], # 10: противоположна грани  4 король?
            [ 4,  8,  9,  5, 18]  # 11: противоположна грани  5 
        ]
         
        return self.get(vertices, faces)
    