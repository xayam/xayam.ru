import re
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
        else:
            points.append((None, None, line))

    # Применяем оптимизатор к списку точек
    optimized_points = optimizer_func(points)

    # Перестраиваем body: сопоставляем оптимизированный порядок с исходными строками
    # (здесь возможны упрощения: например, перегенерация строк по новым координатам)
    new_body = []
    for pt in optimized_points:
        # Генерация строки G1 X... Y... Z... (сохраняя исходный стиль)
        new_line = ""
        if pt[0] is not None:
            new_line += f"G1X{pt[0]:.3f}"
        if pt[1] is not None:
            new_line += f"Y{pt[1]:.3f}"
        new_line += "\n"
        # print(pt)
        new_line = pt[2]
        new_body.append(new_line)

    # Сборка итогового файла
    with open(output_path, 'w') as f:
        f.write(preamble)
        f.write("\n")
        f.write("\n".join(new_body).replace("\n\n", "\n").strip())
        f.write("\n")
        f.write(postamble)

def optimize(points: list):
    width, height, trajectory = get_trajectory("input.png")
    result = []
    print(width, height)
    print(trajectory[0][0])
    for idx in range(width * height):
        ys, xs = trajectory[:idx + 1, 0], trajectory[:idx + 1, 1]
        print(ys, xs)
    return points

if __name__ == "__main__":
    optimize_gcode(
        "01w.input.nc",
        "01w.output.nc",
        optimize,
        1000)
