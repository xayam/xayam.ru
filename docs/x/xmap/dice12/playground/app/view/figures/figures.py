from build123d import *
import trimesh
import numpy as np
from pathlib import Path
from typing import List, Tuple
from scipy.spatial import ConvexHull

script_dir = str(Path(__file__).resolve().parent)

class DiceBase(BasePartObject):
    """Базовый класс для создания платоновых тел"""
    
    def __init__(self, count_faces: int, sizes: float = 20.0, mode: Mode = Mode.ADD):
        supported = {6, 12, 20}
        if count_faces not in supported:
            raise ValueError(f"Поддерживаются только {supported} граней, получено {count_faces}")
        
        self.count_faces = count_faces
        self.sizes = sizes
        self.tm_mesh = None 
        
        with BuildPart() as part:
            if count_faces == 6:
                self.tm_mesh = trimesh.creation.box(extents=[sizes, sizes, sizes])
                Box(sizes, sizes, sizes)
                self.svg_rotating = (-90.0, -90.0, -90.0, -90.0, 0.0, 0.0)
            elif count_faces == 12:
                self.tm_mesh = self._build_dodecahedron(sizes)
            elif count_faces == 20:
                self.tm_mesh = self._build_icosahedron(sizes)
        
        super().__init__(part=part.part, mode=mode)
        self.part = part.part 
    
    def _build_dodecahedron(self, size: float) -> trimesh.Trimesh:
        phi = (1 + np.sqrt(5)) / 2
        scale = size / (2 * phi)
        vertices = []
        for s1 in [-1, 1]:
            for s2 in [-1, 1]:
                for s3 in [-1, 1]:
                    vertices.append([s1*scale, s2*scale, s3*scale])
        for s1 in [-1, 1]:
            for s2 in [-1, 1]:
                vertices.append([0, s1*scale/phi, s2*scale*phi])
                vertices.append([s1*scale/phi, s2*scale*phi, 0])
                vertices.append([s2*scale*phi, 0, s1*scale/phi])
        
        vertices = np.array(vertices)
        hull = ConvexHull(vertices)
        tm_mesh = trimesh.Trimesh(vertices=vertices, faces=hull.simplices)
        self._import_from_trimesh(tm_mesh)
        return tm_mesh
    
    def _build_icosahedron(self, size: float) -> trimesh.Trimesh:
        tm_icos = trimesh.creation.icosahedron()
        scale_factor = size / (2 * tm_icos.bounding_box.extents.max())
        tm_icos.apply_scale(scale_factor)
        self._import_from_trimesh(tm_icos)
        return tm_icos
    
    def _import_from_trimesh(self, tm_mesh: trimesh.Trimesh):
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.stl', delete=False) as tmp:
            tm_mesh.export(tmp.name)
            tmp_path = tmp.name
        try:
            imported = import_stl(tmp_path)
            add(imported)
        finally:
            Path(tmp_path).unlink()

class Dice(DiceBase):
    """Класс для создания игральных костей с SVG и цветами"""
    
    def __init__(self, count_faces: int, svg_files: List[str], sizes: float = 20.0, mode: Mode = Mode.ADD):
        self.svg_files = svg_files
        self._face_planes = []
        super().__init__(count_faces=count_faces, sizes=sizes, mode=mode)
        self._apply_svgs()
    
    def _apply_svgs(self):
        """Применяет SVG-изображения на грани как плоский рисунок"""
        with BuildPart() as dice:
            add(self.part)   
            all_faces = dice.faces()
            
            # Убедимся, что количество граней совпадает с количеством SVG
            if len(all_faces) < self.count_faces:
                print(f"Warning: Not enough faces found ({len(all_faces)}) for {self.count_faces} SVGs")
                
            for i, (face, svg_file) in enumerate(zip(all_faces[:self.count_faces], self.svg_files)):
                print(f"--- Processing face {i} with SVG: {svg_file}")
                
                if not Path(svg_file).exists():
                    print(f"Warning: SVG file {svg_file} not found, skipping")
                    continue
                
                face_plane = Plane(face)
                self._face_planes.append(face_plane)
                
                try:
                    # Импорт SVG
                    raw_svg = import_svg(svg_file)
                    
                    print(f"Raw SVG import result type: {type(raw_svg)}, content: {raw_svg}")
                    
                    if not raw_svg:
                        print(f"Warning: SVG {svg_file} is empty or invalid.")
                        continue
                    
                    # Создаем Compound из списка объектов, если нужно
                    if isinstance(raw_svg, list):
                        if not raw_svg:
                            continue
                        svg_compound = Compound(raw_svg)
                    else:
                        svg_compound = raw_svg

                    bbox = svg_compound.bounding_box()
                    print(f"SVG Bounding Box: {bbox}")
                    bbox_center = bbox.center()

                    face_bounds = face.bounding_box()

                    svg_compound = svg_compound.translate(
                        vector=-bbox_center, 
                        transform=True
                        )

                    face_size = max(face_bounds.size.X, face_bounds.size.Y, face_bounds.size.Z)
                    svg_size = max(bbox.size.X, bbox.size.Y, bbox.size.Z)
                    print(f"Face size: {face_size}, SVG size: {svg_size}")
                    
                    if svg_size > 0 and face_size > 0:
                        scale_factor = (face_size * 0.7) / svg_size
                        print(f"Scaling SVG by factor: {scale_factor}")
                        svg_compound = scale(svg_compound, scale_factor)
                    svg_compound = svg_compound.rotate(Axis.Z, self.svg_rotating[i], True)
                    svg_compound.color = Color("Black")
                    with BuildSketch(face_plane):
                        add(svg_compound)
                    extrude(amount=5.0, mode=Mode.ADD) 
                    print(f"Successfully extruded SVG on face {i}")
                    
                except Exception as e:
                    print(f"Error processing SVG {svg_file}: {e}")
                    import traceback
                    traceback.print_exc()
        dice_part = dice.part
        dice_part.color = Color("Yellow")
        assembly = Compound(children=[dice_part])
        export_step(assembly, f"{script_dir}/3d/d6.step")
        export_gltf(
            to_export=assembly,
            file_path=f"{script_dir}/3d/d6.glb",
            binary=True
            )       
        self.part = dice.part
    

# Пример использования
if __name__ == "__main__":
    svg_files_d6 = [f"{script_dir}/3d/d6/{i}.svg" for i in range(6)]
    d6 = Dice(count_faces=6, svg_files=svg_files_d6, sizes=90.0)
