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
                5.0 * self.m.amount
                )

    def _generate_edge_flanges(self, faces, width):
        """
        Создает прямоугольные фланцы вдоль каждого уникального ребра.

        Условие:
        - ребро проходит через центр фланца;
        - фланец находится под одинаковыми углами к смежным граням,
        то есть его плоскость является биссектором двугранного угла.
        """

        flange_faces = []
        edge_data = {}

        # ------------------------------------------------------------
        # Шаг 1: собираем уникальные рёбра и смежные с ними грани
        # ------------------------------------------------------------
        for face in faces:
            for edge in face.edges():
                v1, v2 = edge.vertices()[0], edge.vertices()[1]

                pt1 = (round(v1.X, 6), round(v1.Y, 6), round(v1.Z, 6))
                pt2 = (round(v2.X, 6), round(v2.Y, 6), round(v2.Z, 6))

                key = tuple(sorted([pt1, pt2]))

                if key not in edge_data:
                    edge_data[key] = {
                        "edge": edge,
                        "faces": []
                    }

                # защищаемся от дублей
                if not any(f is face for f in edge_data[key]["faces"]):
                    edge_data[key]["faces"].append(face)

        # ------------------------------------------------------------
        # Шаг 2: строим фланец для каждого уникального ребра
        # ------------------------------------------------------------
        for data in edge_data.values():
            edge = data["edge"]
            adjacent_faces = data["faces"]

            p1 = Vector(
                edge.vertices()[0].X,
                edge.vertices()[0].Y,
                edge.vertices()[0].Z
            )

            p2 = Vector(
                edge.vertices()[1].X,
                edge.vertices()[1].Y,
                edge.vertices()[1].Z
            )

            v_edge = p2 - p1

            # if v_edge.length < 1e-9:
            #     continue

            v_edge = v_edge.normalized()

            # --------------------------------------------------------
            # Определяем нормаль плоскости фланца
            # --------------------------------------------------------
            if len(adjacent_faces) >= 2:
                n1 = adjacent_faces[0].normal_at()
                n2 = adjacent_faces[1].normal_at()

                # Биссекторная нормаль двугранного угла.
                # Если грани ориентированы согласованно наружу,
                # обычно используется n1 + n2.
                n_bisector = n1 - n2

                # Если нормали почти противоположны,
                # пытаемся использовать альтернативный биссектор.
                if n_bisector.length < 1e-6:
                    n_bisector = n1 + n2

                # Убираем компоненту вдоль ребра,
                # чтобы нормаль фланца была перпендикулярна ребру.
                n_flange = n_bisector - v_edge * n_bisector.dot(v_edge)

                # if n_flange.length < 1e-6:
                #     # Вырожденный случай: выбираем вспомогательный вектор
                #     if abs(v_edge.Z) < 0.9:
                #         aux = Vector(0, 0, 1)
                #     else:
                #         aux = Vector(1, 0, 0)

                #     n_flange = v_edge.cross(aux)

                n_flange = n_flange.normalized()

            # elif len(adjacent_faces) == 1:
            #     # Если смежная грань только одна,
            #     # можно построить фланец перпендикулярно этой грани.
            #     n_face = adjacent_faces[0].normal_at()

            #     n_flange = n_face - v_edge * n_face.dot(v_edge)

            #     if n_flange.length < 1e-6:
            #         if abs(v_edge.Z) < 0.9:
            #             aux = Vector(0, 0, 1)
            #         else:
            #             aux = Vector(1, 0, 0)

            #         n_flange = v_edge.cross(aux)

            #     n_flange = n_flange.normalized()

            # else:
            #     continue

            v_width = n_flange * width 
            # v_edge.cross(n_flange).normalized() * (width / 2.0)

            # Вершины прямоугольника.
            # Исходное ребро проходит через центр фланца.
            f_v1 = Vertex(p1 - v_width)
            f_v2 = Vertex(p1 + v_width)
            f_v3 = Vertex(p2 + v_width)
            f_v4 = Vertex(p2 - v_width)

            # Рёбра фланца
            e1 = Edge.make_line(f_v1, f_v4)
            e2 = Edge.make_line(f_v4, f_v3)
            e3 = Edge.make_line(f_v3, f_v2)
            e4 = Edge.make_line(f_v2, f_v1)

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
    #     unique_edges = {}

    #     # Шаг 1: Извлекаем все уникальные ребра из переданных граней
    #     for face in faces:
    #         for edge in face.edges():
    #             # Сортируем координаты вершин для создания уникального ключа ребра
    #             v1, v2 = edge.vertices()[0], edge.vertices()[1]
    #             pt1 = (round(v1.X, 6), round(v1.Y, 6), round(v1.Z, 6))
    #             pt2 = (round(v2.X, 6), round(v2.Y, 6), round(v2.Z, 6))
    #             key = tuple(sorted([pt1, pt2]))
                
    #             if key not in unique_edges:
    #                 unique_edges[key] = edge

    #     # Шаг 2: Строим прямоугольный фланец для каждого уникального ребра
    #     for edge in unique_edges.values():
    #         p1 = Vector(edge.vertices()[0].X, edge.vertices()[0].Y, edge.vertices()[0].Z)
    #         p2 = Vector(edge.vertices()[1].X, edge.vertices()[1].Y, edge.vertices()[1].Z)
            
    #         # Вектор вдоль самого ребра
    #         v_edge = p2 - p1
            
    #         # Центр ребра (он же задает нормаль из начала координат)
    #         edge_center = (p1 + p2) * 0.5
    #         v_normal = edge_center.normalized()
            
    #         # Вектор ширины фланца, перпендикулярный ребру и нормали
    #         v_width = v_edge.cross(v_normal).normalized() * (width / 2.0)
            
    #         # Смещаем вершины исходного ребра в обе стороны для формирования прямоугольника
    #         f_v1 = Vertex(p1 - v_width)
    #         f_v2 = Vertex(p1 + v_width)
    #         f_v3 = Vertex(p2 + v_width)
    #         f_v4 = Vertex(p2 - v_width)
            
    #         # Создаем ребра новой прямоугольной грани
    #         e1 = Edge.make_line(f_v1, f_v4)
    #         e2 = Edge.make_line(f_v4, f_v3)
    #         e3 = Edge.make_line(f_v3, f_v2)
    #         e4 = Edge.make_line(f_v2, f_v1)
            
    #         # Строим Wire и Face
    #         flange_wire = Wire([e1, e2, e3, e4])
    #         flange_face = Face(flange_wire)
            
    #         flange_faces.append(flange_face)
        
    #     return flange_faces
    