from pathlib import Path
from build123d import *

class Punch(BaseSketchObject):
    def __init__(
        self,
        radius: float,
        size: float,
        blobs: float,
        mode: Mode = Mode.ADD,
    ):
        with BuildSketch() as punch:
            if blobs == 1:
                Circle(size)
            else:
                with PolarLocations(radius, blobs):
                    Circle(size)

            if len(faces()) > 1:
                raise RuntimeError("radius is too large for number and size of blobs")

            insert(Face(faces()[0].outer_wire()), mode=Mode.REPLACE)

        super().__init__(obj=punch.sketch, mode=mode)

tape = Rectangle(20, 5)
for i, location in enumerate(GridLocations(5, 0, 4, 1)):
    tape -= location * Punch(.8, 1, i + 1)
# extrude(tape, amount=5)

script_dir = str(Path(__file__).resolve().parent)

export_stl(tape, script_dir + "/tape.stl")

export_gltf(
    tape, script_dir + "/tape.glb", binary=True, 
    linear_deflection=0.1, 
    angular_deflection=0.5
)

# export = Mesher()
# export.add_shape(tape)
# export.write(script_dir + "/tape.3mf")
