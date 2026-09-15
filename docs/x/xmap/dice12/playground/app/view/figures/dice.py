from typing import List
from base import *


class Dice(DiceBase):
    def __init__(self, count_faces: int, svg_files: List[str], edge: float):
        self.svg_files = svg_files
        self.parts = []
        self._face_planes = []
        super().__init__(count_faces=count_faces, edge=edge)
        self._apply_svgs()
    
    def _apply_svgs(self):
        self._apply_figures()
        self._apply_rings()
        self._apply_sides()
        self._apply_fillets()
        self._apply_corners()

    def _apply_figures(self):
        all_faces = self.dice.faces()
        with BuildPart() as figures:
            if len(all_faces) < self.count_faces:
                print(f"Warning: Not enough faces found ({len(all_faces)}) for {self.count_faces} SVGs")
            for i, (face, svg_file) in enumerate(zip(all_faces[:self.count_faces], self.svg_files)):
                print(f"--- Processing face {i} with SVG: {svg_file}")
                face_plane = Plane(face)
                self._face_planes.append(face_plane) 
                with BuildSketch(face_plane):
                    try:
                        raw_svg = import_svg(svg_file)
                        svg_compound = Compound(raw_svg)
                        bbox = svg_compound.bounding_box()
                        bbox_center = bbox.center()
                        face_bounds = face.bounding_box()
                        face_size = max(face_bounds.size.X, face_bounds.size.Y, face_bounds.size.Z)
                        svg_size = max(bbox.size.X, bbox.size.Y, bbox.size.Z)
                    except Exception as e:
                        print(f"Error processing SVG {svg_file}: {e}")
                    finally:
                        print(f"SVG Bounding Box: {bbox}")
                        print(f"Raw SVG import result type: {type(raw_svg)}, content: {raw_svg}")
                        print(f"Face size: {face_size}, SVG size: {svg_size}")
                    svg_compound = svg_compound.translate(
                        vector=-bbox_center,
                        transform=True
                        )
                    if svg_size > 0 and face_size > 0:
                        scale_factor = (face_size * self.svg_scaling[i]) / svg_size
                        print(f"Scaling SVG by factor: {scale_factor}")
                        svg_compound = scale(
                            objects=svg_compound, 
                            by=scale_factor, 
                            mode=Mode.PRIVATE
                            )
                    svg_compound = svg_compound.rotate(
                        axis=Axis.Z, 
                        angle=self.svg_rotating[i],
                        transform=True
                        )
                    add(svg_compound)
                    c = Circle(0.99 * face_size / 2, mode=Mode.PRIVATE)
                    self.parts.append({
                        "ring": c, 
                        "figure": svg_compound, 
                        "size": face_size,
                        "face": face
                        })
                extrude(amount=EXTRUDE_AMOUNT, mode=Mode.ADD) 
                print(f"Successfully extruded SVG on face {i}")
        print(f"Successfully extruded self.figures")
        self.figures = figures

    def _apply_rings(self):
        with BuildPart() as rings:
            for i in range(len(self.parts)):
                face_plane = self._face_planes[i]
                with BuildSketch(face_plane):
                    diff = self.parts[i]["ring"] - self.parts[i]["figure"]
                    add(diff)
                extrude(amount=EXTRUDE_AMOUNT, mode=Mode.ADD)
        print(f"Successfully extruded self.rings")
        self.rings = rings

    def _apply_sides(self):
        with BuildPart() as sides:
            for i in range(len(self.parts)):
                face_plane = self._face_planes[i]
                with BuildSketch(face_plane):
                    r = Rectangle(self.parts[i]["size"], self.parts[i]["size"], mode=Mode.PRIVATE)
                    add(r)
                extrude(
                    amount=EXTRUDE_AMOUNT, 
                    mode=Mode.ADD
                    )
                with BuildSketch(face_plane):
                    add(self.parts[i]["ring"])
                extrude(amount=EXTRUDE_AMOUNT, mode=Mode.SUBTRACT)
        print(f"Successfully extruded self.sides")
        self.sides = sides

    def _apply_fillets(self):
        with BuildPart() as fillets:
            for i in range(len(self.parts)):
                for edge in self.parts[i]["face"].edges():
                    edge_plane = Plane(origin=edge.position_at(0.0), z_dir=edge.tangent_at(0.0))
                    with BuildSketch(edge_plane):
                        Circle(radius=EXTRUDE_AMOUNT, mode=Mode.ADD)
                    sweep(
                        path=edge,
                        multisection=True, 
                        mode=Mode.ADD
                        )
        print(f"Successfully extruded self.fillets")
        self.fillets = fillets

    def _apply_corners(self):
        vertices = self.dice.vertices()
        corners = None
        for vertex in vertices:
            sphere = Sphere(radius=EXTRUDE_AMOUNT).locate(Location(vertex))
            corner = sphere - self.dice
            for solid in self.fillets.solids():
                corner -= solid
            if corners is None:
                corners = corner
            else:
                corners += corner
        self.corners = corners
        