import math
from build123d import Vertex, Edge, Face, Wire, Shell, Solid

from render.model import Model
from render.d import D

class D12(D):
    def __init__(self, model: Model):
        self.m = model
        self.base = self.dodecahedron()

    def dodecahedron(self):
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
        center = Vertex(0, 0, 0) 
        # 12 граней (пятиугольников), индексы версий заданы против часовой стрелки (нормали наружу)
        faces = [
            [0, 12, 2, 17, 16],  # 0: противоположна грани 6
            [11, 7, 15, 13, 3],  # 1: противоположна грани 7
            [0, 16, 1, 9, 8],    # 2: противоположна грани 8
            [1, 13, 15, 5, 9],   # 3: противоположна грани 9
            [1, 16, 17, 3, 13],  # 4: противоположна грани 10 король?
            [2, 10, 11, 3, 17],  # 5: противоположна грани 11
            [5, 15, 7, 19, 18],  # 6: противоположна грани 0
            [0, 8, 4, 14, 12],   # 7: противоположна грани 1
            [19, 7, 11, 10, 6],  # 8: противоположна грани 2
            [2, 12, 14, 6, 10],  # 9: противоположна грани 3
            [4, 18, 19, 6, 14],  # 10: противоположна грани 4 король?
            [4, 8, 9, 5, 18]     # 11: противоположна грани 5 
        ]
        pieces = [[
            (center, vertices[piece[p-1]], vertices[piece[p]])
            for p in range(len(piece))
            ] 
            for piece in faces]
        # fsBlack, fsWhite = [], []
        # for f in range(len(faces)):
        #     fss1, fss2 = [], []
        #     for v in range(len(faces[f])):
        #         fss1.append(Edge.make_line(faces[f][v-1], faces[f][v]))
        #     for v in range(len(faces[f])):
        #         fss2.append(Edge.make_line(faces[f][::-1][v-1], faces[f][::-1][v]))
        #     face1 = Face(Wire(fss1))
        #     fsBlack.append(face1)
        #     face2 = Face(Wire(fss2))
        #     fsWhite.append(face2)
        # faces = [[vertices[v] for v in face] for face in faces_indices]
        # fs1, fs2 = [], []
        # for f in range(0, 6):
        #     fss = []
        #     for v in range(len(faces[f])):
        #         fss.append(Edge.make_line(faces[f][v-1], faces[f][v]))
        #     face = Face(Wire(fss))
        #     fs1.append(face)
        # fs11 = fs1 + fsBlack
        # for f in range(6, len(faces)):
        #     fss = []
        #     for v in range(len(faces[f])):
        #         fss.append(Edge.make_line(faces[f][v-1], faces[f][v]))
        #     face = Face(Wire(fss))
        #     fs2.append(face)
        # fs22 = fs2 + fsWhite
        # shell0 = Shell(fs1 + fs2) 
        # solid0 = Solid(shell0)
        # shell1 = Shell(fs11) 
        # solid1 = Solid(shell1) 
        # shell2 = Shell(fs22)  
        # solid2 = Solid(shell2)  
        return self.get(pieces, vertices, faces)
    