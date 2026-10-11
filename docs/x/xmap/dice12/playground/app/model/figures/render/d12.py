import math
from build123d import Vertex, Edge, Face, Wire, Shell, Solid, Color, Compound
from render.model import Model

class D12:
    def __init__(self, model: Model):
        self.m = model
        base = self.dodecahedron()
        self.base = base
        # self.base_result = base[1]

    def dodecahedron(self) -> Solid:
        phi = (1.0 + math.sqrt(5.0)) / 2.0
        s = (phi / 2.0) * self.m.edge
        vertices = [
            Vertex( s,  s,  s),             # 0
            Vertex( s,  s, -s),             # 1
            Vertex( s, -s,  s),             # 2
            Vertex( s, -s, -s),             # 3
            Vertex(-s,  s,  s),             # 4
            Vertex(-s,  s, -s),             # 5
            Vertex(-s, -s,  s),             # 6
            Vertex(-s, -s, -s),             # 7
            Vertex( 0,  s*phi,  s/phi),     # 8
            Vertex( 0,  s*phi, -s/phi),     # 9
            Vertex( 0, -s*phi,  s/phi),     # 10
            Vertex( 0, -s*phi, -s/phi),     # 11
            Vertex( s/phi,  0,  s*phi),     # 12
            Vertex( s/phi,  0, -s*phi),     # 13
            Vertex(-s/phi,  0,  s*phi),     # 14
            Vertex(-s/phi,  0, -s*phi),     # 15
            Vertex( s*phi,  s/phi,  0),     # 16
            Vertex( s*phi, -s/phi,  0),     # 17
            Vertex(-s*phi,  s/phi,  0),     # 18
            Vertex(-s*phi, -s/phi,  0)      # 19
        ]
        # 12 граней (пятиугольников), индексы версий заданы против часовой стрелки (нормали наружу)
        faces_indices = [
            [0, 12, 2, 17, 16],  # 0: противоположна грани 11
            [3, 13, 15, 7, 11],  # 7: противоположна грани 1
            [0, 16, 1, 9, 8],    # 2: противоположна грани 9
            [1, 13, 15, 5, 9],   # 3: противоположна грани 6
            [1, 16, 17, 3, 13],  # 4: противоположна грани 10
            [2, 10, 11, 3, 17],  # 5: противоположна грани 8
            [5, 15, 7, 19, 18],  # 11: противоположна грани 0
            [0, 8, 4, 14, 12],   # 1: противоположна грани 7
            [6, 10, 11, 7, 19],  # 9: противоположна грани 2
            [2, 12, 14, 6, 10],  # 6: противоположна грани 3
            [4, 18, 19, 6, 14],  # 10: противоположна грани 4
            [4, 8, 9, 5, 18]     # 8: противоположна грани 5 
        ]
        faces = [[vertices[v] for v in face] for face in faces_indices]
        fs1, fs2 = [], []
        for f in range(0, 6):
            fss = []
            for v in range(len(faces[f])):
                fss.append(Edge.make_line(faces[f][v-1], faces[f][v]))
            face = Face(Wire(fss))
            fs1.append(face)
        for f in range(6, len(faces)):
            fss = []
            for v in range(len(faces[f])):
                fss.append(Edge.make_line(faces[f][v-1], faces[f][v]))
            face = Face(Wire(fss))
            fs2.append(face)
        shell1 = Shell(fs1) 
        solid1 = Solid(shell1) 
        solid1.color = Color(self.m.base_color)
        solid1.label=f"Faces d12, color '{self.m.base_color}'"
        shell2 = Shell(fs2)  
        solid2 = Solid(shell2) 
        solid2.color = Color(self.m.main_color)
        solid2.label = f"Faces d12, color '{self.m.main_color}'"  
        return [Compound(children=[solid1, solid2]), solid1, solid2]
    