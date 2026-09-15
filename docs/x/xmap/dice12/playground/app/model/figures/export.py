
from __init__ import script_dir

from build123d import export_step, export_gltf

from render.model import Model
from render.design import Design


class Export:

    render: Design | None = None

    def __init__(self, config: dict, model: Model):
          
        self.config_dice = config["dice"]
        self.config_export = config["export"]
        self.render = Design(model=model)
     
    def execute(self):

        render = self.render.coloring()
        
        if "step" in self.config_export["output_formats"]:
            export_step(
                to_export=render, 
                file_path=self.config_export["output_file"].format(script_dir, "step")
                )
        if "glb" in self.config_export["output_formats"]:
            export_gltf(
                to_export=render,
                file_path=self.config_export["output_file"].format(script_dir, "glb"),
                binary=True
                )  
        print(f"Successfully export!") 
