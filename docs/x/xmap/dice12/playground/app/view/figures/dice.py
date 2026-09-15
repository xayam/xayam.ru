
from __init__ import script_dir

from creator import Creator
from export import Export

import json


class Dice:

    config: dict = None
    dice: Creator = None

    def __init__(self, config_json: str):
        self.config_json = config_json
        self.init()

    def init(self):
        try:
            with open(f"{script_dir}/{self.config_json}", 'r', encoding='utf-8') as file:
                self.config = json.load(file)
            self.dice = Creator(self.config["dice"]).dice()
        except FileNotFoundError:
            print(f"{self.config_json} not found!")
        except json.JSONDecodeError:
            print(f"Error in format JSON {self.config_json}")


if __name__ == "__main__":
    dice = Dice("d6.json")
    export = Export(config_export=dice.config["export"])
    export.execute(dice=dice.dice)
