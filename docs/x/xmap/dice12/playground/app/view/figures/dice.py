# from scipy.spatial import ConvexHull

from base import *


class Dice(DiceBase):
    def __init__(self, count_faces: int, svg_files: List[str], edge: float):
        self.svg_files = svg_files
        self._face_planes = []
        super().__init__(count_faces=count_faces, edge=edge)
        self._apply_svgs()
    
    def _apply_svgs(self):
         
        all_faces = self.base_dice.faces()
        with BuildPart() as dice:
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
                        scale_factor = (face_size * 0.7) / svg_size
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
                extrude(amount=5.0, mode=Mode.ADD) 
                print(f"Successfully extruded SVG on face {i}")
        self.dice = dice

    def coloring(self, base_color, main_color):
        self.base_dice.color = Color(base_color)
        self.dice.part.color = Color(main_color)
        return [self.base_dice, self.dice.part]
    
    def export(self, base_color, main_color, filename, formats=["step", "glb"]):
        assembly = Compound(children=self.coloring(base_color, main_color))
        if "step" in formats:
            export_step(
                to_export=assembly, 
                file_path=f"{script_dir}/3d/{filename}.step"
                )
        if "glb" in formats:
            export_gltf(
                to_export=assembly,
                file_path=f"{script_dir}/3d/{filename}.glb",
                binary=True
                )       

if __name__ == "__main__":
    svg_files_d6 = [
        f"{script_dir}/3d/d6/{figure}.svg" 
        for figure in d6_figures
        ]
    d6 = Dice(
        count_faces=6, 
        svg_files=svg_files_d6, 
        edge=90.0
        )
    d6.export(
        base_color="white",
        main_color="gray",
        filename="d6", 
        formats=["glb"]
        )
