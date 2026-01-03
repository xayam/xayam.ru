import re
import sys

import numpy as np
from Scripts import winsound

from png2gif import get_trajectory


def extract_coord(line, axis):
    """
    Извлекает числовое значение координаты по указанной оси (например, 'X', 'Y', 'Z')
    из строки G-кода. Возвращает float, или None, если ось не найдена.
    """
    match = re.search(rf'{axis}([-+]?\d*\.?\d+)', line, re.IGNORECASE)
    if match:
        return float(match.group(1))
    else:
        # Если координата не указана, можно вернуть None или оставить текущее значение.
        # Для целей оптимизации траектории лучше вернуть None и обработать отдельно.
        return None

def optimize_gcode(input_path, output_path, optimizer_func, speed):
    with open(input_path, 'r', encoding="UTF-8") as f:
        nc = f.read()
    match = re.search(rf'(.+)(\n;L0\n.+?S{speed}.+?\n)(M9.+)', nc,
                       flags=re.DOTALL | re.UNICODE | re.MULTILINE)
    preamble = match[1]
    body = match[2].split("\n")
    postamble = match[3]
    points = []
    for line in body:
        if 'G0' in line or 'G1' in line:
            # Извлекаем X, Y
            x = extract_coord(line, 'X')
            y = extract_coord(line, 'Y')
            points.append((x, y, line))
        # else:
        #     points.append((None, None, line))

    # Применяем оптимизатор к списку точек
    optimized_points = optimizer_func(points)

    # Сборка итогового файла
    with open(output_path, 'w', encoding="UTF-8") as f:
        f.write(preamble)
        f.write("\n")
        f.write(";L0\n")
        f.write(optimized_points)
        f.write("\n")
        f.write(postamble)

def optimize(points: list):
    width, height, trajectory = get_trajectory("input.png")
    result = ""
    for index in range(len(trajectory)):
        print(f"{index}/{len(trajectory)}")
        cluster = trajectory[index]
        y = 210.0 - cluster[0][0] / height * 210.0 + 50.1
        x = cluster[0][1] / width * 297.0 + 5.1
        y = round(y, 2)
        x = round(x, 2)
        ys_pred = y
        xs_pred = x
        result += f"G0X{x}Y{y}S1000.00F1000.00\n"
        for ys, xs in cluster:
            ys = 210.0 - ys / height * 210.0 + 50.1
            xs = xs / width * 297.0 + 5.1
            ys = round(ys, 2)
            xs = round(xs, 2)
            s = "G1"
            if xs != xs_pred:
                s += f"X{xs}"
                xs_pred = xs
            if ys != ys_pred:
                s += f"Y{ys}"
                ys_pred = ys
            if s == "G1":
                s = ""
            result += s + "\n"
    return result

if __name__ == "__main__":
    optimize_gcode(
        "01w.input.nc",
        "01w.output.nc",
        optimize,
        1000)
    winsound.Beep(1400, 1000)
