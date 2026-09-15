
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
        self.n = self.config["count_faces"]
        self.edge = self.config["edge_size"]
        self.amount = self.config["extrude_amount"]
        self.textures = textures
        self.base_color = self.config["base_color"]
        self.main_color = self.config["main_color"]
        self.scale = self.config["scale"]
        self.rotate = self.config["rotate"]
        