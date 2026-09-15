
from build123d import Vertex, Edge, Face, Wire, Shell, Solid

from render.model import Model

class D6:

    def __init__(self, model: Model):

        self.m = model
        self.base = self.cube()

    def cube(self) -> Solid:
        
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

        return Solid(shell)
