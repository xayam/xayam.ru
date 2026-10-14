from build123d import Edge, Face, Wire, Shell, Solid

class D:

    def __init__(self):
        pass

    def get(self, pieces, vertices, faces):
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