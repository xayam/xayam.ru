import re
import sys
import numpy as np

from Scripts import winsound
from png2gif import get_trajectory


def optimize(filename, speed=1000):
    width, height, binary_image, trajectory = get_trajectory(filename)
    result = ""
    # directions = [
    #     [1, 1], [0, 1], [-1, 1], [-1, 0],
    #     [-1, -1], [0, -1], [1, -1], [1, 0]
    # ]
    binary_image = 255 - binary_image
    for index in range(len(trajectory)):
        print(f"{index + 1}/{len(trajectory)}")
        cluster = trajectory[index]
        y = round(210.0 - cluster[0][0] / height * 210.0 + 50.1, 2)
        x = round(cluster[0][1] / width * 297.0 + 5.1, 2)
        ys_pred1, xs_pred1 = y, x
        result += f"G0X{x}Y{y}S{speed}.00F1000.00\n"
        for ys, xs in cluster:
            y = round(210.0 - ys / height * 210.0 + 50.1, 2)
            x = round(xs / width * 297.0 + 5.1, 2)
            s = "G1"
            if x != xs_pred1:
                s += f"X{x}"
                xs_pred1 = x
            if y != ys_pred1:
                s += f"Y{y}"
                ys_pred1 = y
            if s == "G1":
                s = ""
            s += "\n" + s.replace("G1", "G0") + "\n"
            result += s
    return result


def get_gcode(filename: str, preamble: str, postamble: str, speed: int):
    with open(preamble, 'r', encoding="UTF-8") as f:
        preamble = f.read()
    with open(postamble, 'r', encoding="UTF-8") as f:
        postamble = f.read()

    optimized_points = optimize(filename=filename, speed=speed)

    with open(filename[:-3] + "nc", 'w', encoding="UTF-8") as f:
        f.write(preamble)
        f.write("\n\n")
        f.write(";L0\n")
        f.write(optimized_points)
        f.write("\n\n")
        f.write(postamble)


if __name__ == "__main__":
    get_gcode("input.png","begin.nc","end.nc",1000)
