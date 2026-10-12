
class Model:

    n: int | None = None
    edge: float | None = None
    amount: float | None = None
    textures: list = []

    base_color: str | None = None
    main_color: str | None = None

    scale: list | None = None
    rotate: list | None = None

    def __init__(self, config: dict, textures: list):

        self.config = config
        self.n = self.config["dice"]["count_faces"]
        self.edge = self.config["dice"]["edge_size"]
        self.amount = self.config["dice"]["extrude_amount"]
        self.textures = textures
        self.base_color = self.config["dice"]["base_color"]
        self.main_color = self.config["dice"]["main_color"]
        self.scale = self.config["dice"]["scale"]
        self.rotate = self.config["dice"]["rotate"]
        