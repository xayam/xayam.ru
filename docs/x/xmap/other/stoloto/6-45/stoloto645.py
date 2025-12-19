import pprint

width = 45
sizes = set()
markers = []
result = [0] * width

for w in range(1, width + 1):
    h = width // w
    if width % w > 0:
        h += 1
    sizes.add((w, h))
for w, h in sizes:
    numbers = []
    point = {"t": 0, "n": 0, "v": 0, "x": 0, "y": 0, "w": w, "h": h}
    board = [[point for j in range(width)] for i in range(width)]
    num = 0
    vertical = [0] * h
    horizontal = [0] * w
    diagonal_up = [0] * (2 * width - 1)
    diagonal_down = [0] * (2 * width - 1)
    for i in range(w):
        for j in range(h):
            if num >= width:
                break
            point = {"t": 1, "n": num, "v": 0, "x": i, "y": j, "w": w, "h": h}
            vertical[j] += 1
            horizontal[i] += 1
            if (w - i) ** 2 + j ** 2 <= w ** 2 + h ** 2:
                diagonal_down[j] += 1
            else:
                diagonal_down[width + j - 1] += 1
            if i ** 2 + j ** 2 <= w ** 2 + h ** 2:
                diagonal_up[i] += 1
            else:
                diagonal_up[width + i - 1] += 1
            board[i][j] = point
            numbers.append(point)
            num += 1

    for number in numbers:
        if number["t"] == 1:
            result[number["n"]] += vertical[number["y"]]
            result[number["n"]] += horizontal[number["x"]]
            if (w - number["x"]) ** 2 + number["y"] ** 2 <= w ** 2 + h ** 2:
                result[number["n"]] += diagonal_down[number["x"]]
            else:
                result[number["n"]] += diagonal_down[number["w"] + number["x"]]
            if number["x"] ** 2 + number["y"] ** 2 <= w ** 2 + h ** 2:
                result[number["n"]] += diagonal_down[number["x"]]
            else:
                result[number["n"]] += diagonal_down[number["h"] + number["y"]]
        # print(number["w"], number["h"])
    # print(result)
middle = int(sum(result) / len(result))
print(middle)
r2 = sorted(list(set(result)), reverse=True)
print(r2)
view = [[0] * 9] * 5
index = 0
s = ""
for j in range(len(view)):
    fborder = False
    for i in range(len(view[j])):
        if not fborder:
            view[j][i] = abs(result[index] - middle)
            index += 1
        if index >= width:
            fborder = True
            break
    s += " ".join(map(lambda v: str(v).rjust(4, " "), view[j])) + "\n"
print(s)
