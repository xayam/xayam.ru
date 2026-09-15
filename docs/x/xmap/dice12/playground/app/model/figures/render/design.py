
from build123d import \
    BuildPart, BuildSketch, Compound, Plane, Location, \
    Axis, Mode, Sphere, Circle, Rectangle, Color, Cylinder, Pos, \
    scale, add, extrude, import_svg, sweep

from render.model import Model
from render.d6 import D6
from render.d12 import D12

class Design:

    m: Model | None = None

    corners: any= None
    fillets: any = None 
    sides: any = None 
    figures: any = None
    face_planes: list = []
    parts: list = []

    form: D6 | D12 | None = None
    forms: dict = {6: D6, 12: D12}

    def __init__(self, model: Model):
        self.m = model
        self.init()

    def init(self):

        if self.m.n in self.forms:
            self.form = self.forms[self.m.n](self.m)

        self.apply_figures()
        self.apply_sides()
        self.apply_fillets()
        self.apply_corners()

    def apply_figures(self):
        all_faces = self.form.base.faces()   
        with BuildPart() as figures:
            if len(all_faces) < self.m.n:
                print(f"Warning: Not enough faces found ({len(all_faces)}) " + \
                      f"for {self.m.n} SVGs")
            for i, (face, svg_file) in enumerate(
                zip(all_faces[:self.m.n], self.m.textures)
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
                        scale_factor = (face_size * self.m.scale[i]) / svg_size
                        print(f"Scaling SVG by factor: {scale_factor}")
                        svg_compound = scale(
                            objects=svg_compound, 
                            by=scale_factor, 
                            mode=Mode.PRIVATE
                            )
                    svg_compound = svg_compound.rotate(
                        axis=Axis.Z, 
                        angle=self.m.rotate[i],
                        transform=True
                        )
                    add(svg_compound)
                    Circle(0.99 * face_size / 2, mode=Mode.PRIVATE)
                    self.parts.append({
                        "figure": svg_compound, 
                        "size": face_size,
                        "face": face
                        })
                extrude(amount=self.m.amount, mode=Mode.ADD) 
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
                    amount=self.m.amount, 
                    mode=Mode.ADD
                    )
                with BuildSketch(face_plane):
                    add(self.parts[i]["figure"])
                extrude(amount=self.m.amount, mode=Mode.SUBTRACT)
        print(f"Successfully extruded self.sides")
        self.sides = sides

    def apply_fillets(self):
        fillets = None
        for i in range(len(self.parts)):
            for edge in self.parts[i]["face"].edges():
                cylinder = edge.location_at(0.5) * Cylinder(radius=self.m.amount, height=edge.length)
                fillet = cylinder - self.form.base
                for solid in self.sides.part.solids():
                    fillet -= solid
                if fillets is None:
                    fillets = fillet
                else:
                    fillets += fillet
        self.fillets = fillets
        print(f"Successfully extruded self.fillets")

    def apply_corners(self):
        vertices = self.form.base.vertices()
        corners = None
        for vertex in vertices:
            
            sphere = Sphere(radius=self.m.amount).locate(Location(vertex))
            corner = sphere - self.form.base
            for solid in self.fillets.solids():
                corner -= solid
            if corners is None:
                corners = corner
            else:
                corners += corner
        self.corners = corners

    def coloring(self) -> Compound:

        self.form.base.color = Color(self.m.base_color)
        self.form.base.label = "Base, color #1"

        self.corners.color = Color(self.m.base_color)
        self.corners.label = "Corners, color #1"

        self.fillets.color = Color(self.m.base_color)
        self.fillets.label = "Fillets, color #1"

        self.sides.part.color = Color(self.m.base_color)
        self.sides.part.label = "Sides, color #1"

        self.figures.part.color = Color(self.m.main_color)
        self.figures.part.label = "Figures, color #2"

        assembly = Compound(children=[
            self.form.base, 
            self.corners,
            self.fillets, 
            self.sides.part,  
            self.figures.part
        ])

        return assembly
        