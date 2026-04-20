import sys

import cv2
import numpy as np
import matplotlib.pyplot as plt


def is_convex(pts):
    """Проверка на выпуклость (остается без изменений)"""
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


def calculate_score(canny_mask, poly_pts, w_area, w_boundary, w_internal):
    mask = np.zeros_like(canny_mask, dtype=np.uint8)
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

    # Формула:
    # Мы делаем упор на BOUNDARY (прилипание к краям).
    # AREA делаем очень маленьким, чтобы он просто не давал пятиугольнику сжаться в точку,
    # но не позволял ему расти бесконечно.
    score = (area * w_area) + (boundary_hits * w_boundary) - (internal_hits * w_internal)
    return score, area, boundary_hits, internal_hits


def get_smart_initial_pentagon(mark, canny_img):
    _, binary = cv2.threshold(canny_img, 127, 255, cv2.THRESH_BINARY)
    dist_map = cv2.distanceTransform(255 - binary, cv2.DIST_L2, 5)
    max_dist = np.max(dist_map)
    threshold_ratio = 0.5  # берём 90% от максимума (настраивается)
    high_dist_mask = (dist_map >= max_dist * threshold_ratio).astype(np.uint8) * 255
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
        high_dist_mask, connectivity=8, ltype=cv2.CV_32S
    )
    min_area = 1000  # минимальное количество пикселей в кластере
    valid_clusters = []
    for i in range(1, num_labels):  # пропускаем фон (label 0)
        if stats[i, cv2.CC_STAT_AREA] >= min_area:
            valid_clusters.append((i, centroids[i]))
    print(f"Найдено {len(valid_clusters)} стабильный(х) кластер(а):")
    cx_maximum = 0
    cy_maximum = 0
    area_maximum = 0
    for idx, (label_id, (cx, cy)) in enumerate(valid_clusters, 1):
        area = stats[label_id, cv2.CC_STAT_AREA]
        if area > area_maximum:
            area_maximum = area
            cx_maximum = int(cx)
            cy_maximum = int(cy)
        # print(f"  Кластер {idx}: центр ({cx:.1f}, {cy:.1f}), площадь {area} пикс.")
    x_center = cx_maximum
    y_center = cy_maximum
    print(x_center, y_center)
    initial_pts = [[x_center, y_center - 1],
                   [x_center - 1, y_center],
                   [x_center - 1, y_center + 1],
                   [x_center + 1, y_center + 1],
                   [x_center + 1, y_center]]
    return initial_pts
    # width = mark["width"]
    # height = mark["height"]
    # sizes = mark["input_box"]
    # x_delta = (sizes[0] + (sizes[2] - sizes[0]) / 2) / (width - 0)
    # y_delta = (sizes[1] + (sizes[3] - sizes[1]) / 2) / (height - 0)
    # x_center = int(canny_img.shape[0] * x_delta)
    # y_center = int(canny_img.shape[1] * y_delta)
    # initial_pts = [[x_center    , y_center - 1],
    #                [x_center - 1, y_center],
    #                [x_center - 1, y_center + 1],
    #                [x_center + 1, y_center + 1],
    #                [x_center + 1, y_center]]
    # return initial_pts


def optimize_pentagon_fixed(canny_img, initial_pts, iterations=300):
    canny_bin = (canny_img > 50).astype(np.uint8)
    current_pts = initial_pts.copy()

    # --- НАСТРОЙКА ВЕСОВ (ИСПРАВЛЕННАЯ) ---

    # 1. w_boundary (Награда за границу): Главный двигатель.
    #    Заставляет стороны пятиугольника лечь ровно на белые линии Canny.
    #    Чем больше это число, тем точнее форма.
    w_boundary = 10.0

    # 2. w_internal (Штраф за внутренность):
    #    Заставляет избегать логотипа (пчелы).
    #    Должно быть меньше, чем выгода от прилипания к внешнему краю.
    w_internal = 90.0

    # 3. w_area (Вес площади):
    #    ОЧЕНЬ МАЛЕНЬКИЙ.
    #    Он нужен только как "поверхностное натяжение", чтобы пятиугольник не сжался в точку,
    #    если линий внутри мало. Но он не должен быть достаточно большим, чтобы вызвать взрыв.
    w_area = 0.05

    print(f"{'Iter':<5} | {'Area':<8} | {'Bound':<8} | {'Internal':<8} | {'Score':<10}")
    print("-" * 50)

    for i in range(iterations):
        improved = False

        current_score, cur_area, cur_bound, cur_int = calculate_score(
            canny_bin, current_pts, w_area, w_boundary, w_internal)

        if i % 5 == 0:
            print(f"{i:<5} | {cur_area:<8.0f} | {cur_bound:<8.0f} | {cur_int:<8.0f} | {current_score:<10.1f}")

        for idx in range(5):
            best_score = calculate_score(canny_bin, current_pts, w_area, w_boundary, w_internal)[0]
            best_pt = current_pts[idx]

            search_radius = 10
            cx, cy = current_pts[idx]

            local_best_score = best_score
            local_best_pt = best_pt

            # Поиск в окрестности
            for dx in range(-search_radius, search_radius + 1, 2):
                for dy in range(-search_radius, search_radius + 1, 2):
                    new_pt = (int(cx + dx), int(cy + dy))

                    h, w = canny_bin.shape
                    if not (0 <= new_pt[0] < w and 0 <= new_pt[1] < h):
                        continue

                    temp_pts = current_pts.copy()
                    temp_pts[idx] = new_pt

                    # Проверка выпуклости
                    if not is_convex(temp_pts):
                        continue

                    new_score, _, _, _ = calculate_score(canny_bin, temp_pts, w_area, w_boundary, w_internal)

                    if new_score > local_best_score:
                        local_best_score = new_score
                        local_best_pt = new_pt
                        improved = True

            if local_best_score > best_score:
                current_pts[idx] = local_best_pt

        if not improved:
            print(f"Сходимость достигнута на итерации {i}")
            break

    final_score, f_area, f_bound, f_int = calculate_score(canny_bin, current_pts, w_area, w_boundary, w_internal)
    print(f"{'Final':<5} | {f_area:<8.0f} | {f_bound:<8.0f} | {f_int:<8.0f} | {final_score:<10.1f}")

    return current_pts

def main(mark, image, canny_img):
    # Получаем начальные точки
    initial_pts = get_smart_initial_pentagon(mark, canny_img)
    # Оптимизируем
    final_pts = optimize_pentagon_fixed(canny_img, initial_pts)
    # Визуализация
    res_img = np.array(image.copy())
    pts = np.array(final_pts, np.int32).reshape((-1, 1, 2))
    cv2.polylines(res_img, [pts], True, (0, 255, 0), 3)
    return res_img
