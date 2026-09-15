
from dice import *


class ExportDice(Dice):
    def __init__(self, count_faces: int, svg_files: List[str], edge: float):
        super().__init__(count_faces=count_faces, svg_files=svg_files, edge=edge)

    def coloring(self, base_color, main_color):
        self.dice.color = Color(base_color)
        self.dice.label = "Inner dice, color #1"
        self.corners.color = Color(base_color)
        self.corners.label = "Corners, color #1"
        self.fillets.part.color = Color(base_color)
        self.fillets.part.label = "Fillets, color #1"
        self.sides.part.color = Color(base_color)
        self.sides.part.label = "Sides, color #1"
        self.rings.part.color = Color(main_color)
        self.rings.part.label = "Rings, color #2"
        self.figures.part.color = Color(base_color)
        self.figures.part.label = "Figures, color #1"
        return [
            self.dice, 
            self.corners,
            self.fillets.part, 
            self.sides.part, 
            self.rings.part, 
            self.figures.part
            ]
    
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
        print(f"Successfully export!")     


if __name__ == "__main__":
    d6 = ExportDice(
        count_faces=6, 
        svg_files=d6_svg_files, 
        edge=EDGE
        )
    d6.export(
        base_color="white",
        main_color="black",
        filename="d6-white-black", 
        formats=["glb", "step"]
        )
