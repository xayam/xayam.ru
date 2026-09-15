
from __init__ import script_dir

from build123d import \
    BuildPart, BuildSketch, Compound, Plane, Location, \
    Axis, Mode, Sphere, Circle, Rectangle, \
    scale, add, extrude, import_svg, sweep


class Design:

    base: any = None 
    corners: any = None
    fillets: any = None 
    sides: any = None 
    figures: any = None

    svg_files = None
    svg_scaling = None
    svg_rotating = None
    face_planes = []
    parts = []

    def __init__(self):
        self.init()

    def init(self):

        self.apply_figures()
        self.apply_sides()
        self.apply_fillets()
        self.apply_corners()

    def apply_figures(self):
        all_faces = self.base.faces()
        self.svg_files = [
            self.config_dice["svg_figures"].format(script_dir, figure)
            for figure in self.config_dice["id_figures"]
            ]   
        with BuildPart() as figures:
            if len(all_faces) < self.config_dice["count_faces"]:
                print(f"Warning: Not enough faces found ({len(all_faces)}) " + \
                      f"for {self.config_dice["count_faces"]} SVGs")
            for i, (face, svg_file) in enumerate(
                zip(all_faces[:self.config_dice["count_faces"]], self.svg_files)
                ):
                print(f"--- Processing face {i} with SVG: {svg_file}")
                face_plane = Plane(face)
                self.face_planes.append(face_plane) 
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
                        scale_factor = (face_size * self.config_dice["svg_scaling"][i]) / svg_size
                        print(f"Scaling SVG by factor: {scale_factor}")
                        svg_compound = scale(
                            objects=svg_compound, 
                            by=scale_factor, 
                            mode=Mode.PRIVATE
                            )
                    svg_compound = svg_compound.rotate(
                        axis=Axis.Z, 
                        angle=self.config_dice["svg_rotating"][i],
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
                extrude(amount=self.config_dice["extrude_amount"], mode=Mode.ADD) 
                print(f"Successfully extruded SVG on face {i}")
        print(f"Successfully extruded self.figures")
        self.figures = figures

    def apply_sides(self):
        with BuildPart() as sides:
            for i in range(len(self.parts)):
                face_plane = self.face_planes[i]
                with BuildSketch(face_plane):
                    r = Rectangle(self.parts[i]["size"], self.parts[i]["size"], mode=Mode.PRIVATE)
                    add(r)
                extrude(
                    amount=self.config_dice["extrude_amount"], 
                    mode=Mode.ADD
                    )
                with BuildSketch(face_plane):
                    add(self.parts[i]["figure"])
                extrude(amount=self.config_dice["extrude_amount"], mode=Mode.SUBTRACT)
        print(f"Successfully extruded self.sides")
        self.sides = sides

    def apply_fillets(self):
        with BuildPart() as fillets:
            for i in range(len(self.parts)):
                for edge in self.parts[i]["face"].edges():
                    edge_plane = Plane(origin=edge.position_at(0.0), z_dir=edge.tangent_at(0.0))
                    with BuildSketch(edge_plane):
                        Circle(radius=self.config_dice["extrude_amount"], mode=Mode.ADD)
                    sweep(
                        path=edge,
                        multisection=True, 
                        mode=Mode.ADD
                        )
        print(f"Successfully extruded self.fillets")
        self.fillets = fillets

    def apply_corners(self):
        vertices = self.base.vertices()
        corners = None
        for vertex in vertices:
            sphere = Sphere(radius=self.config_dice["extrude_amount"]).locate(Location(vertex))
            corner = sphere - self.base
            for solid in self.fillets.solids():
                corner -= solid
            if corners is None:
                corners = corner
            else:
                corners += corner
        self.corners = corners
        