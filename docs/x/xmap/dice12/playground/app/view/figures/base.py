import numpy as np

from config import *


class DiceBase(BasePartObject):
    def __init__(self, count_faces: int, edge: float):
        supported = {6, 12}
        if count_faces not in supported:
            raise ValueError(f"Support only {supported} faces, you input count_faces={count_faces}")
        self.count_faces = count_faces
        self.edge = edge
        self.dice = None
        self.svg_scaling = None
        self.svg_rotating = None
        self.init()
        
    def init(self):
        if self.count_faces == 6:
            self._build_cube()
            self.svg_scaling = d6_svg_scaling
            self.svg_rotating = d6_svg_rotating
        elif self.count_faces == 12:
            self._build_dodecahedron()
        super().__init__(part=self.dice)
           
    def _build_cube(self):
        vertices = [
            Vertex(0.0, 0.0, self.edge),
            Vertex(0.0, self.edge, self.edge),
            Vertex(self.edge, self.edge, self.edge),
            Vertex(self.edge, 0.0, self.edge),
            Vertex(0.0, 0.0, 0.0),
            Vertex(0.0, self.edge, 0.0),
            Vertex(self.edge, self.edge, 0.0),
            Vertex(self.edge, 0.0, 0.0)
        ]
        top = [0, 1, 2, 3]
        bottom = [4, 5, 6, 7]
        left = [0, 1, 5, 4]
        right = [2, 3, 7, 6]
        front = [0, 3, 7, 4]
        back = [1, 2, 6, 5]
        faces = [top, right, front, left, back, bottom]
        faces = [[vertices[v] for v in face] for face in faces]
        fs = []
        for f in range(len(faces)):
             fss = []
             for v in range(len(faces[f])):
               fss.append(Edge.make_line(faces[f][v-1], faces[f][v]))
             fs.append(Face(Wire(fss)))
        shell = Shell(fs)
        self.dice = Solid(shell)
                   
    def _build_dodecahedron(self):
        pass
