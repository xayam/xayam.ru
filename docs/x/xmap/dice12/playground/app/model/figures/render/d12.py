
from build123d import Vertex, Edge, Face, Wire, Shell, Solid

from render.model import Model


class D12:

    def __init__(self, model: Model):

        self.m = model
        self.base = self.dode()

    def dode(self) -> Solid:
        
        return Solid()
