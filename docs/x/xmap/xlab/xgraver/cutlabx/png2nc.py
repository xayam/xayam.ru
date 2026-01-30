import numpy as np
import cv2
import winsound

from png2gif import get_trajectory

#    Шаблоны заданий работы гравера:
# 1) WOOD - установлен синий лазер;
# 2) PLASTIC/METAL - установлен красный лазер;
# 3) GRAVE - гравировка (один проход);
# 4) BURN - резка (несколько проходов по кластерам, обычно хватает 5 раз);
WOOD_GRAVE = "wood_grave"
WOOD_BURN = "wood_burn"
PLASTIC_GRAVE = "plastic_grave"
METAL_GRAVE = "metal_grave"
METAL_BURN = "metal_burn"

# ввод задания для гравера здесь
task = METAL_GRAVE

# калибровка по точке привязки
boundX = 5.1
boundY = 50.1

# приведение к формату А4
widthA4 = 297.0
heightA4 = 210.0

SPEED = "speed" # скорость передвижения лазера
POWER = "power" # мощность включения лазера в процентах
LOOP = "loop"   # количество проходов

# Все конфигурации заданий работы гравера
config = {
    WOOD_GRAVE: {
        SPEED: 4000,
        POWER: 95,
        LOOP: 1
    },
    WOOD_BURN: {
        SPEED: 400,
        POWER: 95,
        LOOP: 5
    },
    PLASTIC_GRAVE: {
        SPEED: 1000,
        POWER: 95,
        LOOP: 1
    },
    METAL_GRAVE: {
        SPEED: 1000,
        POWER: 95,
        LOOP: 1
    },
    METAL_BURN: {
        SPEED: 400,
        POWER: 95,
        LOOP: 5
    }
}

# не менять
task = config[task]


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

def optimize(filename: str, speed: str, loop: int = 1) -> str:
    width, height, binary_image, trajectory = \
        get_trajectory(filename=filename, animate=False)
    image = np.ones_like(binary_image) * 255
    # image3 = np.ones_like(binary_image) * 255
    # cv2.imwrite("temp.png", image)
    # image = cv2.imread("temp.png", cv2.IMREAD_GRAYSCALE)
    # binary_image = 255 - binary_image
    result = ""
    for i in range(len(trajectory)):
        for l in range(loop):
            print(f"{i + 1}/{len(trajectory)} : {l + 1}/{loop}")
            cluster = trajectory[i]
            y = round(heightA4 - cluster[0][0] / height * heightA4 + boundY, 2)
            x = round(cluster[0][1] / width * widthA4 + boundX, 2)
            ys_pred1, xs_pred1 = y, x
            ys_pred2, xs_pred2 = cluster[0][0], cluster[0][1]
            result += f"G0X{x}Y{y}{speed}\n"
            index = -1
            for ys, xs in cluster:
                index += 1
                flag = False
                y = round(heightA4 - ys / height * heightA4 + boundY, 2)
                x = round(xs / width * widthA4 + boundX, 2)
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
    cv2.imwrite("output.nc.png", image)
    return result


def get_gcode(speed: int = 4000, power: int = 95, loop: int = 1):
    with open(f"begin.nc", 'r', encoding="UTF-8") as f:
        preamble = f.read()
    with open(f"end.nc", 'r', encoding="UTF-8") as f:
        postamble = f.read()
    speed = f"S{power * 10}.00F{speed}.00"
    optimized_points = optimize(filename="input.png", speed=speed, loop=loop)

    with open("output.nc", 'w', encoding="UTF-8") as f:
        f.write(preamble)
        f.write("\n\n")
        f.write(";L0\n")
        f.write(optimized_points)
        f.write("\n\n")
        f.write(postamble)


if __name__ == "__main__":
    get_gcode(**task)
    winsound.Beep(1000, 1500)
