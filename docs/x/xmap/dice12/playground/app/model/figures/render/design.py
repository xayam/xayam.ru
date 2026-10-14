import math

from build123d import \
    BuildPart, BuildSketch, Compound, Plane, \
    Axis, Mode, Sphere, Color, fillet, Solid, Shell, \
    scale, add, extrude, import_svg

from render.model import Model
from render.d6 import D6
from render.d12 import D12

class Design:

    m: Model | None = None

    corners: any = None
    fillets: any = None 
    sides: any = None 
    figures: list = []
    faces: list = []
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
        self.apply_fillets()

    def apply_figures(self):
        for i in range(len(self.form.base[0])):
            face = self.form.base[0][i] 
            svg_file = self.m.textures[i]
            with BuildPart() as figure: 
                print(f"--- Processing face {i} with SVG: {svg_file}")
                face_plane = Plane(face)
                self.faces.append(face) 
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
                        print(f"Raw SVG import result type: {type(raw_svg)}, content: -")
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
                    # Circle(0.99 * face_size / 2, mode=Mode.PRIVATE)
                    self.parts.append({
                        "figure": svg_compound, 
                        "size": face_size,
                        "face": face
                        })
                extrude(amount=-self.m.amount, mode=Mode.ADD) 
                print(f"Successfully extruded SVG on face {i}")
            self.figures.append(figure)
        print(f"Successfully extruded self.figures")

    def apply_fillets(self):
        i = 0
        for id in self.m.colors:
            self.form.base[1][i] = fillet(self.form.base[1][i].edges(), radius=self.m.radius)
            self.form.base[1][i].color = Color(self.m.colors[id][0])
            self.form.base[1][i].label=f"Faces, color '{self.m.colors[id][0]}'"
            i += 1

    def assembling(self) -> Compound:
        figures = []
        i = 0
        for id in self.m.colors:
            self.form.base[1][i] -= self.figures[i].part
            self.figures[i].part.color = Color(self.m.colors[id][1])
            self.figures[i].part.label = f"Figures, color '{self.m.colors[id][1]}'"
            figures.append(self.figures[i].part)
            figures.append(self.form.base[1][i])
            i += 1
        assembly = Compound(children=figures)
        return assembly
        