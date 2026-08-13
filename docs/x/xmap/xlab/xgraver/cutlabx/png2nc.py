import os
import numpy as np
import cv2
import winsound

from config import *
from png2gif import greedy_path, matrix_path, liner_path, get_trajectory, get_liner_trajectory
from gray import get_gray_trajectory

current_dir = os.path.dirname(os.path.abspath(__file__))

# алгоритм траекторий
# greedy_path для сложных картинок
# matrix_path быстро, для текста и мелких кластеров
# contour_path - быстро, только контур, есть недостатки - лишние линии
methods = {
    "liner": {"trajectory": get_liner_trajectory, "algorithm": liner_path},
    "matrix": {"trajectory": get_trajectory, "algorithm": matrix_path},
    "greedy": {"trajectory": get_trajectory, "algorithm": greedy_path},
}

def optimize(filename: str, algorithm, speed: str, loop: int = 1) -> str:
    width, height, binary_image, trajectory = \
        methods[algorithm]["trajectory"](filename=filename, algorithm=methods[algorithm]["algorithm"])
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
    with open(f"{current_dir}/begin.nc", 'r', encoding="UTF-8") as f:
        preamble = f.read()
    with open(f"{current_dir}/end.nc", 'r', encoding="UTF-8") as f:
        postamble = f.read()
    inputs = [
        f for f in os.listdir(current_dir)
        if f.endswith('all.png') and f.startswith('matrix.')
    ]
    for filename in inputs:
        print(filename)
        s = filename.split("--")[1]
        s2 = s.split("-")
        algorithm = s2[0]
        # material = materials[s2[1]]
        speed = int(s2[2]) # скорость передвижения лазера
        power = int(s2[3]) # мощность включения лазера в процентах
        loop = int(s2[4]) # количество проходов
        conf = f"S{power * 10}.00F{speed}.00"
        print(conf)
        if s2[0] == "gray":
            optimized_points = algorithm.__call__(filename=f"{current_dir}/{filename}", speed=speed, power=power)
        else:
            optimized_points = optimize(filename=f"{current_dir}/{filename}", algorithm=algorithm,
                                        speed=conf, loop=loop)

        with open(f"{current_dir}/{filename[:-3]}nc", 'w', encoding="UTF-8") as f:
            f.write(preamble)
            f.write("\n\n")
            f.write(";L0\n")
            f.write(optimized_points)
            f.write("\n\n")
            f.write(postamble)


if __name__ == "__main__":
    get_gcode()
    winsound.Beep(1000, 1500)
