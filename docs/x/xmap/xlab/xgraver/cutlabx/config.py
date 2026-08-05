
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
