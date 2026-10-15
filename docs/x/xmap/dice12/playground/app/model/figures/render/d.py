from build123d import Vertex, Rot, Edge, Face, Wire, Shell, Solid, Vector, Color

class D:

    center: Vertex | None = None

    def __init__(self, model):
        self.m = model
        self.center = Vertex(0.0, 0.0, 0.0)
        self.rotate = Rot(Y=0.0)

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
        return faces0, solids0 \
            , self._generate_edge_flanges(
                faces0, 
                self.m.amount
                )
    
    def _generate_edge_flanges(self, faces, width):
        """
        Создает прямоугольные грани вдоль каждого уникального ребра faces.
        Ребро проходит через центр новой грани.
        Новая грань перпендикулярна нормали из начала координат (0,0,0).
        """
        flange_faces = []
        unique_edges = {}

        # Шаг 1: Извлекаем все уникальные ребра из переданных граней
        for face in faces:
            for edge in face.edges():
                # Сортируем координаты вершин для создания уникального ключа ребра
                v1, v2 = edge.vertices()[0], edge.vertices()[1]
                pt1 = (round(v1.X, 6), round(v1.Y, 6), round(v1.Z, 6))
                pt2 = (round(v2.X, 6), round(v2.Y, 6), round(v2.Z, 6))
                key = tuple(sorted([pt1, pt2]))
                
                if key not in unique_edges:
                    unique_edges[key] = edge

        # Шаг 2: Строим прямоугольный фланец для каждого уникального ребра
        for edge in unique_edges.values():
            p1 = Vector(edge.vertices()[0].X, edge.vertices()[0].Y, edge.vertices()[0].Z)
            p2 = Vector(edge.vertices()[1].X, edge.vertices()[1].Y, edge.vertices()[1].Z)
            
            # Вектор вдоль самого ребра
            v_edge = p2 - p1
            
            # Центр ребра (он же задает нормаль из начала координат)
            edge_center = (p1 + p2) * 0.5
            v_normal = edge_center.normalized()
            
            # Вектор ширины фланца, перпендикулярный ребру и нормали
            v_width = v_edge.cross(v_normal).normalized() * (width / 2.0)
            
            # Смещаем вершины исходного ребра в обе стороны для формирования прямоугольника
            f_v1 = Vertex(p1 - v_width)
            f_v2 = Vertex(p1 + v_width)
            f_v3 = Vertex(p2 + v_width)
            f_v4 = Vertex(p2 - v_width)
            
            # Создаем ребра новой прямоугольной грани
            e1 = Edge.make_line(f_v1, f_v4)
            e2 = Edge.make_line(f_v4, f_v3)
            e3 = Edge.make_line(f_v3, f_v2)
            e4 = Edge.make_line(f_v2, f_v1)
            
            # Строим Wire и Face
            flange_wire = Wire([e1, e2, e3, e4])
            flange_face = Face(flange_wire)
            
            flange_faces.append(flange_face)
        
        return flange_faces

    # def _generate_edge_flanges(self, faces, width):
    #     """
    #     Создает прямоугольные грани вдоль каждого уникального ребра faces.
    #     Ребро проходит через центр новой грани.
    #     Новая грань перпендикулярна нормали из начала координат (0,0,0).
    #     """
    #     flange_faces = []

    #     # код здесь
        
    #     return flange_faces
    