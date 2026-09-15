from build123d import *
from pathlib import Path

EXTRUDE_AMOUNT = 2
EDGE = 11

script_dir = str(Path(__file__).resolve().parent)

d6_figures = ["bn", "bq", "bk", "bb", "bp", "br"]
d6_svg_files = [
    f"{script_dir}/3d/d6/{figure}.svg" 
    for figure in d6_figures
    ]    
d6_svg_scaling = (0.65, 0.77, 0.77, 0.68, 0.73, 0.68)
d6_svg_rotating = (0.0, 0.0, -90.0, 0.0, 90.0, 180.0)
