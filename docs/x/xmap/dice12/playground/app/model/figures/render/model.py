
class Model:

    n: int | None = None
    edge: float | None = None
    amount: float | None = None
    textures: list | None = None

    base_color: str | None = None
    main_color: str | None = None

    scale: list | None = None
    rotate: list | None = None

    def __init__(self, config: dict, textures: list):
        self.n = config["dice"]["count_faces"]
        self.edge = config["dice"]["edge_size"]
        self.amount = config["dice"]["extrude_amount"]
        self.textures = textures
        self.base_color = config["dice"]["base_color"]
        self.main_color = config["dice"]["main_color"]
        self.scale = config["dice"]["scale"]
        self.rotate = config["dice"]["rotate"]

        self.output_formats = config["export"]["output_formats"]
        self.output_file = config["export"]["output_file"]
        