import json

from build123d import export_step, export_gltf

from __init__ import script_dir
from render.model import Model
from render.design import Design

class Dice:

    config: dict | None = None
    model: Model | None = None
    render: Design | None = None

    def __init__(self, config_json: str):

        self.config_json = config_json
        self.init()

    def init(self):
        try:
            with open(self.config_json, 'r', encoding='utf-8') as file:
                self.config = json.load(file)
            textures = [
                self.config["dice"]["textures"].format(script_dir, figure)
                for figure in self.config["dice"]["colors"]
                ]
            self.model = Model(self.config, textures)
            self.render = Design(model=self.model)
        except FileNotFoundError:
            print(f"{self.config_json} not found!")
        except json.JSONDecodeError:
            print(f"Error in format JSON {self.config_json}")

    def save(self):
        render = self.render.assembling()       
        if "step" in self.model.output_formats:
            export_step(
                to_export=render, 
                file_path=self.model.output_file.format(script_dir, "step")
                )
        if "glb" in self.model.output_formats:
            export_gltf(
                to_export=render,
                file_path=self.model.output_file.format(script_dir, "glb"),
                binary=True
                )  
        print(f"Successfully export!") 


if __name__ == "__main__":
    config = f"{script_dir}/config/d12.chess-classic.json"
    config = f"{script_dir}/config/d6.chess-classic.white-black.json"
    config = f"{script_dir}/config/d6.chess-classic.black-white.json"
    config = f"{script_dir}/config/d12.chess-adds.white-black.json"
    config = f"{script_dir}/config/d12.chess-adds.black-white.json"
    Dice(config).save()
