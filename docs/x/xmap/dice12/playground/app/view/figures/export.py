
from __init__ import script_dir

from build123d import export_step, export_gltf

class Export:
    def __init__(self, config_export):
          
          self.config_export = config_export
     
    def execute(self, dice):
        if "step" in self.config_export["output_formats"]:
            export_step(
                to_export=dice, 
                file_path=self.config_export["output_file"].format(script_dir, "step")
                )
        if "glb" in self.config_export["output_formats"]:
            export_gltf(
                to_export=dice,
                file_path=self.config_export["output_file"].format(script_dir, "glb"),
                binary=True
                )  
        print(f"Successfully export!") 
