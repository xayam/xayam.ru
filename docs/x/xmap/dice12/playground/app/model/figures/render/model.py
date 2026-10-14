
class Model:

    n: int | None = None
    edge: float | None = None
    amount: float | None = None
    textures: list | None = None
    colors: dict | None = None
    scale: list | None = None
    rotate: list | None = None
    radius: float | None = None

    def __init__(self, config: dict, textures: list):
        self.n = config["dice"]["count_faces"]
        self.edge = config["dice"]["edge_size"]
        self.amount = config["dice"]["extrude_amount"]
        self.textures = textures
        self.colors = config["dice"]["colors"]
        self.scale = config["dice"]["scale"]
        self.rotate = config["dice"]["rotate"]

        self.radius = self.amount / 3 * self.n / 6

        self.output_formats = config["export"]["output_formats"]
        self.output_file = config["export"]["output_file"]
        