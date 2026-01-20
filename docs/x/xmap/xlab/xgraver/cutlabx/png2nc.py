import re
import sys
import numpy as np
import cv2
from Scripts import winsound
from png2gif import get_trajectory


def line_pixels(x0, y0, x1, y1):
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    while True:
        points.append((y0, x0))
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy
    return points

def optimize(filename, speed=""):
    width, height, binary_image, trajectory = \
        get_trajectory(filename=filename, animate=False)
    image = np.ones_like(binary_image) * 255
    # image3 = np.ones_like(binary_image) * 255
    # cv2.imwrite("temp.png", image)
    # image = cv2.imread("temp.png", cv2.IMREAD_GRAYSCALE)
    # binary_image = 255 - binary_image
    result = ""
    for index in range(len(trajectory)):
        print(f"{index + 1}/{len(trajectory)}")
        cluster = trajectory[index]
        y = round(210.0 - cluster[0][0] / height * 210.0 + 50.1, 2)
        x = round(cluster[0][1] / width * 297.0 + 5.1, 2)
        ys_pred1, xs_pred1 = y, x
        ys_pred2, xs_pred2 = cluster[0][0], cluster[0][1]
        result += f"G0X{x}Y{y}{speed}\n"
        index = -1
        for ys, xs in cluster:
            index += 1
            flag = False
            y = round(210.0 - ys / height * 210.0 + 50.1, 2)
            x = round(xs / width * 297.0 + 5.1, 2)
            line_pts = line_pixels(xs, ys, xs_pred2, ys_pred2)
            for yy, xx in line_pts:
                if binary_image[yy, xx] == 0:
                    flag = True
                    break
            if flag:
                s = "G0"
            else:
                s = "G1"
            if x != xs_pred1:
                s += f"X{x}"
                xs_pred1 = x
            if y != ys_pred1:
                s += f"Y{y}"
                ys_pred1 = y
            if s in ["G0", "G1"]:
                s = ""
            if not flag:
                image = cv2.line(image,
                                 (xs, ys), (xs_pred2, ys_pred2),
                                 (0, 0, 0), thickness=1)
            ys_pred2, xs_pred2 = ys, xs
            s += "\n" + s.replace("G1", "G0") + "\n"
            result += s
    cv2.imwrite("temp.png", image)
    return result


def get_gcode(tip="plastic"):
    # Plastic = S1000.00F1000.00
    # Wood = = S950.00F4000.00
    with open(f"begin_{tip}.nc", 'r', encoding="UTF-8") as f:
        preamble = f.read()
    with open(f"end_{tip}.nc", 'r', encoding="UTF-8") as f:
        postamble = f.read()

    if tip == "wood":
        speed = "S950.00F4000.00"
    elif tip == "plastic":
        speed = "S1000.00F1000.00"
    else:
        raise "Error! material!"

    optimized_points = optimize(filename="input.png", speed=speed)

    with open("output.nc", 'w', encoding="UTF-8") as f:
        f.write(preamble)
        f.write("\n\n")
        f.write(";L0\n")
        f.write(optimized_points)
        f.write("\n\n")
        f.write(postamble)


if __name__ == "__main__":
    # get_gcode()
    get_gcode("wood")
