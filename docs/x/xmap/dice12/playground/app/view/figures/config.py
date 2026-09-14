from build123d import *
from pathlib import Path
from typing import List, Iterable

script_dir = str(Path(__file__).resolve().parent)

d6_figures = ["bk", "bq", "br", "bb", "bn", "bp"]
d6_svg_rotating = (180.0, -90.0, -90.0, 90.0, -90.0, 180.0)
