import json

from __init__ import script_dir

from render.model import Model
from export import Export

class Dice:

    config: dict | None = None
    model: Model | None = None
    export: Export | None = None

    def __init__(self, config_json: str):

        self.config_json = config_json
        self.init()

    def init(self):

        try:
            with open(self.config_json, 'r', encoding='utf-8') as file:
                self.config = json.load(file)
            textures = [
                self.config["dice"]["textures"].format(script_dir, figure)
                for figure in self.config["dice"]["id_figures"]
                ]
            self.model = Model(self.config["dice"], textures)
            self.export = Export(self.config, model=self.model)
        except FileNotFoundError:
            print(f"{self.config_json} not found!")
        except json.JSONDecodeError:
            print(f"Error in format JSON {self.config_json}")

    def save(self):

        self.export.execute()


if __name__ == "__main__":
    jobs = [
        f"{script_dir}/config/d6.white-black.json", 
        f"{script_dir}/config/d6.black-white.json"
        ]
    for config in jobs:
        dice = Dice(config)
        dice.save()
