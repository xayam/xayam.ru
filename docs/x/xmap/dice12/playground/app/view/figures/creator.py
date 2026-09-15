
from build123d import Compound, Color

from d6 import D6
from d12 import D12


class Creator:

    form: any = None
    forms: dict = {6: D6, 12: D12}

    def __init__(self, config_dice: dict):

        self.config_dice = config_dice

        if self.config_dice["count_faces"] in self.forms:
            self.form = self.forms[self.config_dice["count_faces"]](self.config_dice)
        
    def coloring(self) -> Compound:

        base_color = self.config_dice["base_color"]
        main_color = self.config_dice["main_color"]

        self.form.base.color = Color(base_color)
        self.form.base.label = "Base, color #1"

        self.form.corners.color = Color(base_color)
        self.form.corners.label = "Corners, color #1"

        self.form.fillets.part.color = Color(base_color)
        self.form.fillets.part.label = "Fillets, color #1"

        self.form.sides.part.color = Color(base_color)
        self.form.sides.part.label = "Sides, color #1"

        self.form.figures.part.color = Color(main_color)
        self.form.figures.part.label = "Figures, color #1"

        model = Compound(children=[
            self.form.base, 
            self.form.corners,
            self.form.fillets.part, 
            self.form.sides.part,  
            self.form.figures.part
        ])

        return model

    def dice(self) -> Compound:

        return self.coloring()
