import cv2
import numpy as np
import matplotlib.pyplot as plt


def get_geometry_metrics(pts):
    """
    Вычисляет длины сторон и внутренние углы пятиугольника.
    """
    n = len(pts)
    sides = []
    angles = []
    for i in range(n):
        p1 = np.array(pts[i], dtype=float)
        p2 = np.array(pts[(i + 1) % n], dtype=float)
        p3 = np.array(pts[(i + 2) % n], dtype=float)

        side_len = np.linalg.norm(p2 - p1)
        sides.append(side_len)

        v1 = p1 - p2
        v2 = p3 - p2

        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)

        if norm_v1 > 0 and norm_v2 > 0:
            cos_angle = np.dot(v1, v2) / (norm_v1 * norm_v2)
            cos_angle = np.clip(cos_angle, -1.0, 1.0)
            angle_rad = np.arccos(cos_angle)
            angles.append(np.degrees(angle_rad))
        else:
            angles.append(0.0)

    return sides, angles


def calculate_score(canny_mask, poly_pts, w_area, w_boundary, w_internal, w_regular):
    mask = np.zeros_like(canny_mask, dtype=np.uint8)
    # Важно: pts должны быть в формате [x, y] для OpenCV
    pts = np.array(poly_pts, dtype=np.int32).reshape((-1, 1, 2))
    cv2.fillPoly(mask, [pts], 1)
    area = cv2.contourArea(pts)

    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(mask, kernel, iterations=1)
    eroded = cv2.erode(mask, kernel, iterations=1)
    poly_boundary = dilated - eroded

    boundary_hits = np.sum((poly_boundary > 0) & (canny_mask > 0))

    interior = mask - poly_boundary
    interior = (interior > 0).astype(np.uint8)
    internal_hits = np.sum((interior > 0) & (canny_mask > 0))

    # --- БАЗОВАЯ ОЦЕНКА ---
    # Увеличил вес площади, чтобы стимулировать рост
    base_score = (area * w_area) + (boundary_hits * w_boundary) - (internal_hits * w_internal)

    # --- ШТРАФ ЗА НЕПРАВИЛЬНОСТЬ ---
    sides, angles = get_geometry_metrics(poly_pts)

    mean_side = np.mean(sides)
    # Нормализуем дисперсию сторон относительно среднего, чтобы не зависеть от масштаба
    side_variance = sum((s - mean_side) ** 2 for s in sides) / (mean_side ** 2 + 1e-5)

    mean_angle = np.mean(angles)
    angle_variance = sum((a - mean_angle) ** 2 for a in angles)

    # Общий штраф
    regularity_penalty = (side_variance * 1000 + angle_variance * 10.0)

    final_score = base_score - (regularity_penalty * w_regular)

    return final_score, area, boundary_hits, internal_hits, regularity_penalty


def is_convex(pts):
    n = len(pts)
    sign = None
    for i in range(n):
        p1 = np.array(pts[i])
        p2 = np.array(pts[(i + 1) % n])
        p3 = np.array(pts[(i + 2) % n])
        v1 = p2 - p1
        v2 = p3 - p2
        cross = v1[0] * v2[1] - v1[1] * v2[0]
        if cross != 0:
            if sign is None:
                sign = cross > 0
            else:
                if (cross > 0) != sign:
                    return False
    return True


def get_smart_initial_pentagon(canny_img):
    # Исправлено: shape[0] - высота (Y), shape[1] - ширина (X)
    h, w = canny_img.shape
    x_center = w // 2
    y_center = h // 2

    # Создаем начальный пятиугольник побольше (радиус 50 пикселей), чтобы сразу захватить часть грани
    radius = 5
    initial_pts = []
    # Углы для правильного пятиугольника, начинаем сверху (-90 градусов)
    for i in range(5):
        angle = np.deg2rad(-90 + i * 72)
        px = int(x_center + radius * np.cos(angle))
        py = int(y_center + radius * np.sin(angle))
        initial_pts.append([px, py])

    return initial_pts


def optimize_pentagon_regular(canny_img, initial_pts, iterations=50):
    canny_bin = (canny_img > 50).astype(np.uint8)
    current_pts = initial_pts.copy()

    # --- НАСТРОЙКА ВЕСОВ ---
    # 1. w_boundary: Прилипание к контуру
    w_boundary = 5.0

    # 2. w_area: Стимул к большой площади (немного увеличил)
    w_area = 0.5

    # 3. w_internal: Штраф за внутренности (ЛОГОТИП).
    #    Сильно уменьшил, чтобы алгоритм игнорировал корону внутри
    w_internal = 0.05

    # 4. w_regular: Стремление к правильной форме.
    #    Уменьшил, так как перспектива искажает форму.
    w_regular = 0.1

    print(f"{'Iter': <5} | {'Area': <8} | {'Bound': <8} | {'Int': <6} | {'RegPen': <10} | {'Score': <10} ")
    print("-" * 65)

    for i in range(iterations):
        improved = False

        current_score, cur_area, cur_bound, cur_int, cur_reg = calculate_score(
            canny_bin, current_pts, w_area, w_boundary, w_internal, w_regular)

        if i % 5 == 0:
            print(
                f"{i: <5} | {cur_area: <8.0f} | {cur_bound: <8.0f} | {cur_int: <6.0f} | {cur_reg: <10.1f} | {current_score: <10.1f} ")

        # Увеличил радиус поиска, чтобы пятиугольник мог быстрее вырасти
        search_radius = 30

        for idx in range(5):
            best_score = calculate_score(canny_bin, current_pts, w_area, w_boundary, w_internal, w_regular)[0]
            best_pt = current_pts[idx]

            cx, cy = current_pts[idx]
            local_best_score = best_score
            local_best_pt = best_pt

            # Поиск в окрестности
            for dx in range(-search_radius, search_radius + 1, 3):  # Шаг 3 для скорости
                for dy in range(-search_radius, search_radius + 1, 3):
                    new_pt = (int(cx + dx), int(cy + dy))

                    h, w = canny_bin.shape
                    if not (0 <= new_pt[0] < w and 0 <= new_pt[1] < h):
                        continue

                    temp_pts = current_pts.copy()
                    temp_pts[idx] = new_pt

                    if not is_convex(temp_pts):
                        continue

                    new_score, _, _, _, _ = calculate_score(canny_bin, temp_pts, w_area, w_boundary, w_internal,
                                                            w_regular)

                    if new_score > local_best_score:
                        local_best_score = new_score
                        local_best_pt = new_pt
                        improved = True

            if local_best_score > best_score:
                current_pts[idx] = local_best_pt

        if not improved:
            print(f"Сходимость достигнута на итерации {i} ")
            break

    final_score, f_area, f_bound, f_int, f_reg = calculate_score(canny_bin, current_pts, w_area, w_boundary, w_internal,
                                                                 w_regular)
    print(
        f"{'Final': <5} | {f_area: <8.0f} | {f_bound: <8.0f} | {f_int: <6.0f} | {f_reg: <10.1f} | {final_score: <10.1f} ")

    return current_pts


def main(image, canny_img):
    initial_pts = get_smart_initial_pentagon(canny_img)
    final_pts = optimize_pentagon_regular(canny_img, initial_pts)

    res_img = np.array(image.copy())
    pts = np.array(final_pts, np.int32).reshape((-1, 1, 2))
    cv2.polylines(res_img, [pts], True, (0, 255, 0), 3)

    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    axes[0].imshow(canny_img, cmap='gray')
    axes[0].set_title("Canny Edges")
    axes[0].axis('off')
    axes[1].imshow(res_img)
    axes[1].set_title("Optimized Pentagon")
    axes[1].axis('off')
    plt.tight_layout()
    plt.savefig("comparison.jpg", dpi=150)
    plt.show()