import math

from build123d import \
    BuildPart, BuildSketch, Compound, Plane, \
    Axis, Mode, Color, \
    scale, add, extrude, import_svg, Part

from render.model import Model
from render.d6 import D6
from render.d12 import D12

class Design:

    m: Model | None = None

    fillets: list = []
    corners: list = []
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
                extrude(amount=-self.m.amount, mode=Mode.ADD) 
                print(f"Successfully extruded SVG on face {i}")
            self.figures.append(figure.part)
        print(f"Successfully extruded self.figures")

    def apply_fillets(self):
        for i in range(len(self.form.base[2])):
            with BuildPart() as fillet:  
                add(self.form.base[2][i])
                extrude(
                    dir=self.form.base[2][i].normal_at(), 
                    amount=-self.m.amount)
            self.fillets.append(fillet.part)
        for i in range(len(self.form.base[3])):
            with BuildPart() as corner:  
                add(self.form.base[3][i])
                extrude(
                    dir=self.form.base[3][i].normal_at(), 
                    amount=-2.0 * self.m.amount)
            self.corners.append(corner.part)
        fillets = Compound(children=self.fillets)
        corners = Compound(children=self.corners)
        for i in range(len(self.form.base[1])):
            self.form.base[1][i] = \
                self.form.base[1][i] - fillets - corners - self.figures[i]
        print(f"Successfully apply_fillets")

    def fuse_shapes(self, shapes):
        if not shapes:
            return None
        result = shapes[0]
        for shape in shapes[1:]:
            result = result + shape
        return result

    def assembling(self): 
        colored = {} 
        for i, id in enumerate(self.m.colors):
              colored[self.m.colors[id][0]] = None
              colored[self.m.colors[id][1]] = None 
        for i, id in enumerate(self.m.colors):
            if colored[self.m.colors[id][0]] is None:
                colored[self.m.colors[id][0]] = self.form.base[1][i]
            else:
                colored[self.m.colors[id][0]] += self.form.base[1][i]
            if colored[self.m.colors[id][1]] is None:
                colored[self.m.colors[id][1]] = self.figures[i]
            else:
                colored[self.m.colors[id][1]] += self.figures[i]
        result = []
        for color, fused in colored.items():
            if fused is not None:
                fused.color = Color(color)
                fused.label = f"Part, color '{color}'"
                result.append(fused)
        assembly = Compound(children=result)
        print(f"Successfully assembling")
        # assembly = assembly.rotate(
        #     axis=self.form.rotate_axis, 
        #     angle=self.form.rotate_angle, 
        #     transform=True
        #     ) 
        return assembly    
        