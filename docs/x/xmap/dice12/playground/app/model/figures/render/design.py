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

    def apply_figures(self):
        all_faces = self.form.base[0].faces()  
        for i, (face, svg_file) in enumerate(
                                            zip(all_faces[:self.m.n], self.m.textures)
                                            ):
            if len(all_faces) < self.m.n:
                print(f"Warning: Not enough faces found ({len(all_faces)}) " + \
                      f"for {self.m.n} SVGs")
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

    def coloring(self) -> Compound:
        radius = self.m.amount / 3 * self.m.n / 6
        self.form.base[1] = fillet(self.form.base[1].edges(), radius=radius)
        self.form.base[1].color = Color(self.m.base_color)
        self.form.base[1].label=f"Faces, color '{self.m.base_color}'"
        if self.m.n != 6:
            self.form.base[2] = fillet(self.form.base[2].edges(), radius=radius)
            self.form.base[2].color = Color(self.m.main_color)
            self.form.base[2].label = f"Faces, color '{self.m.main_color}'"    
        figures = []
        for i in range(len(self.figures)):
            if i < 6:
                color = self.m.main_color
                self.form.base[1] -= self.figures[i].part
            else:
                color = self.m.base_color
                self.form.base[2] -= self.figures[i].part
            self.figures[i].part.color = Color(color)
            self.figures[i].part.label = f"Figures, color '{color}'"
            figures.append(self.figures[i].part)
        figures.append(self.form.base[1])
        if self.form.base[2] is not None:
            figures.append(self.form.base[2])
        assembly = Compound(children=[ 
            *figures
        ])
        return assembly
        