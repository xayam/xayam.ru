from build123d import Vertex, Rot, Edge, Face, Wire, Shell, Solid

class D:

    center: Vertex | None = None

    def __init__(self):
        self.center = Vertex(0.0, 0.0, 0.0)
        self.rotate = Rot(Y=0)

    def get(self, vertices, faces):
        pieces = [[
                    (self.center, vertices[piece[p-1]], vertices[piece[p]])
                    for p in range(len(piece))
                    ] 
                    for piece in faces]
        faces0, solids0 = [], []
        for p in range(len(pieces)):
            face, face0 = [], []
            for vs in pieces[p]:
                fs = []
                for v in range(len(vs)):
                    fs.append(Edge.make_line(vs[v-1], vs[v]))   
                face.append(Face(Wire(fs)))
            for v in range(len(faces[p])):  
                face0.append(Edge.make_line(vertices[faces[p][v-1]], vertices[faces[p][v]]))
            face0 = Face(Wire(face0))
            faces0.append(face0)
            face.append(face0)
            shell = Shell(face) 
            solid = Solid(shell)
            solids0.append(solid) 
        return faces0, solids0