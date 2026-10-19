
import math

from build123d import Vertex, Rot, Edge, Face, Wire, Shell, Solid, Vector, Axis

class D:

    center: Vertex | None = None
    rotate_axis: Axis | None = None
    rotate_angle: float | None = None

    def __init__(self, model):
        self.m = model
        self.center = Vertex(0.0, 0.0, 0.0)
        self.rotate_axis = Axis.X

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
        return faces0, solids0, \
            self._generate_edge_flanges(
                faces0, 
                5.0 * self.m.amount
                ), \
            self._generate_corners(
                vertices, 
                faces, 
                10.0 * self.m.amount
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
            v_edge = v_edge.normalized()
            # --------------------------------------------------------
            # Определяем нормаль плоскости фланца
            # --------------------------------------------------------
            if len(adjacent_faces) >= 2:
                n1 = adjacent_faces[0].normal_at()
                n2 = adjacent_faces[1].normal_at()
                # Биссекторная нормаль двугранного угла.
                n_bisector = n1 - n2
                # Убираем компоненту вдоль ребра,
                # чтобы нормаль фланца была перпендикулярна ребру.
                n_flange = n_bisector - v_edge * n_bisector.dot(v_edge)
                n_flange = n_flange.normalized()
            v_width = n_flange * width 
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

    def _generate_corners(self, vertices, faces, width):
        """
        Создаёт квадратные фланцы на каждой уникальной вершине.

        Условие:
        - квадрат проходит через центр вершины;
        - плоскость квадрата находится под одинаковыми углами
        ко всем смежным граням настолько, насколько это возможно.

        Для произвольной вершины с множеством смежных граней точное
        равенство углов может быть невозможно, поэтому используется
        усреднённая нормаль смежных граней.
        """

        eps = 1e-9
        half = abs(float(width)) / 2.0

        if half < eps:
            return []

        # ------------------------------------------------------------
        # Вспомогательные функции
        # ------------------------------------------------------------
        def vlen(v):
            return math.sqrt(v.dot(v))

        def normalize(v):
            length = vlen(v)
            if length < eps:
                return None
            return v.normalized()

        def perp_to_axis(v, axis):
            """Возвращает компоненту вектора, перпендикулярную оси."""
            return v - axis * v.dot(axis)

        def as_vector(obj):
            """Vertex/Vector -> Vector."""
            return Vector(obj.X, obj.Y, obj.Z)

        # ------------------------------------------------------------
        # Центр модели
        # ------------------------------------------------------------
        if self.center is not None:
            center = as_vector(self.center)
        else:
            center = Vector(0.0, 0.0, 0.0)

        # ------------------------------------------------------------
        # Шаг 1: уникальные вершины
        # ------------------------------------------------------------
        unique_points = []
        coord_to_canon = {}
        orig_to_canon = []

        for v in vertices:
            p = as_vector(v)
            key = (round(p.X, 6), round(p.Y, 6), round(p.Z, 6))

            if key not in coord_to_canon:
                coord_to_canon[key] = len(unique_points)
                unique_points.append(p)

            orig_to_canon.append(coord_to_canon[key])

        # ------------------------------------------------------------
        # Шаг 2: собираем нормали граней для каждой вершины
        # и соседние вершины для ориентации квадрата
        # ------------------------------------------------------------
        adjacent_normals = [[] for _ in unique_points]
        adjacent_neighbors = [[] for _ in unique_points]

        def add_neighbor(i, j):
            if i == j:
                return
            if j not in adjacent_neighbors[i]:
                adjacent_neighbors[i].append(j)

        for face_indices in faces:
            if len(face_indices) < 3:
                continue

            pts = []
            canon = []
            valid = True

            for idx in face_indices:
                if idx < 0:
                    idx += len(vertices)

                if idx < 0 or idx >= len(vertices):
                    valid = False
                    break

                pts.append(as_vector(vertices[idx]))
                canon.append(orig_to_canon[idx])

            if not valid:
                continue

            # Удаляем повторяющиеся подряд вершины
            clean_pts = []
            clean_canon = []

            for p, c in zip(pts, canon):
                if not clean_canon or c != clean_canon[-1]:
                    clean_pts.append(p)
                    clean_canon.append(c)

            # Если первая и последняя совпадают, убираем замыкание
            if len(clean_canon) > 1 and clean_canon[0] == clean_canon[-1]:
                clean_pts.pop()
                clean_canon.pop()

            if len(clean_pts) < 3:
                continue

            pts = clean_pts
            canon = clean_canon
            m = len(pts)

            # --------------------------------------------------------
            # Нормаль polygon через метод Newell
            # --------------------------------------------------------
            nx = 0.0
            ny = 0.0
            nz = 0.0

            for i in range(m):
                a = pts[i]
                b = pts[(i + 1) % m]

                nx += (a.Y - b.Y) * (a.Z + b.Z)
                ny += (a.Z - b.Z) * (a.X + b.X)
                nz += (a.X - b.X) * (a.Y + b.Y)

            face_normal = Vector(nx, ny, nz)

            # Центр грани
            centroid = Vector(0.0, 0.0, 0.0)
            for p in pts:
                centroid = centroid + p
            centroid = centroid * (1.0 / m)

            # Ориентируем нормаль наружу от центра модели
            if face_normal.dot(centroid - center) < 0.0:
                face_normal = face_normal * -1.0

            face_normal = normalize(face_normal)

            if face_normal is None:
                continue

            # Добавить нормаль каждой вершине этой грани
            seen_vertices = []
            for c in canon:
                if c not in seen_vertices:
                    seen_vertices.append(c)
                    adjacent_normals[c].append(face_normal)

            # Соседние вершины для выбора направления сторон квадрата
            for k, c in enumerate(canon):
                prev_c = canon[k - 1]
                next_c = canon[(k + 1) % m]

                add_neighbor(c, prev_c)
                add_neighbor(c, next_c)

        # ------------------------------------------------------------
        # Шаг 3: строим квадрат в каждой уникальной вершине
        # ------------------------------------------------------------
        corner_faces = []

        for i, point in enumerate(unique_points):
            normals = adjacent_normals[i]

            if not normals:
                continue

            # --------------------------------------------------------
            # Нормаль квадрата
            # --------------------------------------------------------
            normal_sum = Vector(0.0, 0.0, 0.0)

            for n in normals:
                normal_sum = normal_sum + n

            corner_normal = normalize(normal_sum)

            radial = normalize(point - center)

            if corner_normal is None:
                if radial is not None:
                    corner_normal = radial
                else:
                    corner_normal = Vector(0.0, 0.0, 1.0)
            else:
                # Знак нормали не меняет плоскость, но делает результат
                # более стабильным и направленным наружу.
                if radial is not None and corner_normal.dot(radial) < 0.0:
                    corner_normal = corner_normal * -1.0

            corner_normal = normalize(corner_normal)

            if corner_normal is None:
                continue

            # --------------------------------------------------------
            # Выбор направления X внутри плоскости квадрата.
            # Сначала пробуем использовать направления соседних рёбер.
            # --------------------------------------------------------
            u_sum = Vector(0.0, 0.0, 0.0)
            first_u = None

            for j in adjacent_neighbors[i]:
                d = unique_points[j] - point
                d = perp_to_axis(d, corner_normal)
                du = normalize(d)

                if du is not None:
                    if first_u is None:
                        first_u = du
                    u_sum = u_sum + du

            u_dir = normalize(u_sum)

            if u_dir is None:
                u_dir = first_u

            if u_dir is None:
                if radial is not None:
                    u_dir = normalize(perp_to_axis(radial, corner_normal))

            if u_dir is None:
                if abs(corner_normal.Z) < 0.9:
                    aux = Vector(0.0, 0.0, 1.0)
                else:
                    aux = Vector(1.0, 0.0, 0.0)

                u_dir = normalize(corner_normal.cross(aux))

                if u_dir is None:
                    aux = Vector(0.0, 1.0, 0.0)
                    u_dir = normalize(corner_normal.cross(aux))

            if u_dir is None:
                continue

            # --------------------------------------------------------
            # Второе направление в плоскости квадрата
            # --------------------------------------------------------
            v_dir = normalize(corner_normal.cross(u_dir))

            if v_dir is None:
                continue

            # --------------------------------------------------------
            # Вершины квадрата
            # --------------------------------------------------------
            q1 = Vertex(point - u_dir * half - v_dir * half)
            q2 = Vertex(point + u_dir * half - v_dir * half)
            q3 = Vertex(point + u_dir * half + v_dir * half)
            q4 = Vertex(point - u_dir * half + v_dir * half)

            e1 = Edge.make_line(q1, q2)
            e2 = Edge.make_line(q2, q3)
            e3 = Edge.make_line(q3, q4)
            e4 = Edge.make_line(q4, q1)

            corner_wire = Wire([e1, e2, e3, e4])
            corner_face = Face(corner_wire)

            corner_faces.append(corner_face)

        return corner_faces
    