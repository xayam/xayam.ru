import os
import numpy as np
import cv2
import winsound

from png2gif import greedy_path, matrix_path, contour_path, get_trajectory

# алгоритм траекторий
# greedy_path медленно, плохое качество
# matrix_path быстро, хорошее качество
# contour_path - быстро, только контур, есть недостатки - лишние линии
algorithms = {
    "matrix": matrix_path, # для гравировки
    "contour": contour_path,
    "greedy": greedy_path # TODO плохой недоделанный алгоритм, работает для резки по линиям
}
materials = {
    "burn": "burn",
    "osina": "wood_light",
    "fanera": "wood_light",
    "buk": "wood_hard",
    "dub": "wood_hard",
    "bereza": "wood_hard",
    "acril": "acril",
    "plastic": "plastic",
    "metal": "metal"
}

# калибровка по точке привязки
boundX = 5.1
boundY = 50.1

# приведение к формату А4
widthA4 = 297.0
heightA4 = 210.0

# TODO удалить это
config1 = {
    "PLASTIC_GRAVE": {
        "ALGORITHM": "algorithm",
        "SPEED": 1000,
        "POWER": 95,
        "LOOP": 1
    },
    "METAL_GRAVE": {
        "ALGORITHM": "algorithm",
        "SPEED": 1000,
        "POWER": 100,
        "LOOP": 1
    },
}


def line_pixels(y0, x0, y1, x1):
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

def optimize(filename: str, algorithm, speed: str, loop: int = 1) -> str:
    width, height, binary_image, trajectory = \
        get_trajectory(filename=filename, algorithm=algorithm, animate=False)
    image = np.ones_like(binary_image) * 255
    result = ""
    for l in range(loop):
        for i in range(len(trajectory)):
            print(f"{i + 1}/{len(trajectory)} : {l + 1}/{loop}")
            cluster = trajectory[i]
            y_pred = None
            for j in range(1, len(cluster)):
                flag = False
                ys1, xs1 = cluster[j - 1]
                ys2, xs2 = cluster[j]
                y1 = round(heightA4 - ys1 / height * heightA4 + boundY, 2)
                x1 = round(xs1 / width * widthA4 + boundX, 2)
                if j == 1:
                    result += f"G0X{x1}Y{y1}{speed}\n"
                    y_pred = y1
                y2 = round(heightA4 - ys2 / height * heightA4 + boundY, 2)
                x2 = round(xs2 / width * widthA4 + boundX, 2)
                points = line_pixels(ys1, xs1, ys2, xs2)
                for yy, xx in points:
                    if binary_image[yy, xx] == 0:
                        flag = True
                        break
                if flag:
                    result += f"G0X{x2}Y{y2}\n"
                    y_pred = y2
                else:
                    s1 = f"G0X{x1}"
                    if y1 != y_pred:
                        s1 += f"Y{y1}"
                        y_pred = y1
                    s1 += "\n"
                    if x1 != x2:
                        result += s1
                    result += f"G1X{x2}"
                    result += "\n"
                    image = cv2.line(image, (xs1, ys1), (xs2, ys2),
                                         color=(0, 0, 0), thickness=1)
    cv2.imwrite(filename[:-3] + "nc.png", image)
    return result


def get_gcode():
    with open(f"begin.nc", 'r', encoding="UTF-8") as f:
        preamble = f.read()
    with open(f"end.nc", 'r', encoding="UTF-8") as f:
        postamble = f.read()
    inputs = [
        f for f in os.listdir('./')
        if f.endswith('all.png') and f.startswith('matrix.')
    ]
    for filename in inputs:
        print(filename)
        s = filename.split("--")[1]
        s2 = s.split("-")
        algorithm = algorithms[s2[0]]
        # material = materials[s2[1]]
        speed = int(s2[2]) # скорость передвижения лазера
        power = int(s2[3]) # мощность включения лазера в процентах
        loop = int(s2[4]) # количество проходов
        conf = f"S{power * 10}.00F{speed}.00"
        print(conf)
        optimized_points = optimize(filename=filename, algorithm=algorithm,
                                    speed=conf, loop=loop)

        with open(f"{filename[:-3]}nc", 'w', encoding="UTF-8") as f:
            f.write(preamble)
            f.write("\n\n")
            f.write(";L0\n")
            f.write(optimized_points)
            f.write("\n\n")
            f.write(postamble)


if __name__ == "__main__":
    get_gcode()
    winsound.Beep(1000, 1500)
