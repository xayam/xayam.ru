
from build123d import Vertex, Edge, Face, Wire, Shell, Solid

from design import Design


class D12(Design):

    def __init__(self, config_dice):

        self.config_dice = config_dice
        self.base = self.dode()

        super().__init__(self)

    def dode(self) -> Solid:
        
        return Solid()
