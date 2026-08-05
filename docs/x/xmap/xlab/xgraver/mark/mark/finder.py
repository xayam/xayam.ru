import sys
import cv2
import numpy as np
import math


def is_convex(pts):
    """Проверка на выпуклость (оставлена без изменений)"""
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

    score = (area * w_area) + (boundary_hits * w_boundary) - (internal_hits * w_internal)
    return score, area, boundary_hits, internal_hits


def generate_constrained_pentagon(cx, cy, R, deformations):
    """
    Генерирует 5 вершин с ЖЁСТКИМИ ограничениями:
    1. Вершина 0 строго сверху (угол -90°)
    2. Ребро 2-3 параллельно OX (углы 54° и 126°, k2==k3)
    3. Остальные вершины могут иметь независимые деформации (чуть-чуть неправильная форма)
    """
    # Углы в градусах (0 - вправо, 90 - вниз в системе координат изображения)
    angles_deg = [-90, -18, 54, 126, 198]
    # deformatios: [k0, k1, k2, k4] (k3 принудительно = k2)
    k0, k1, k2, k4 = deformations
    k3 = k2  # Гарантирует горизонтальность нижнего ребра

    ks = [k0, k1, k2, k3, k4]
    pts = []

    for deg, k in zip(angles_deg, ks):
        rad = math.radians(deg)
        r = R * k
        px = cx + r * math.cos(rad)
        py = cy + r * math.sin(rad)
        pts.append([int(px), int(py)])
    return pts


def get_smart_initial_params(mark, canny_img):
    """Находит центр и примерный радиус пустой области"""
    _, binary = cv2.threshold(canny_img, 127, 255, cv2.THRESH_BINARY)
    dist_map = cv2.distanceTransform(255 - binary, cv2.DIST_L2, 5)
    max_dist = np.max(dist_map)

    threshold_ratio = 0.6
    high_dist_mask = (dist_map >= max_dist * threshold_ratio).astype(np.uint8) * 255

    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
        high_dist_mask, connectivity=8, ltype=cv2.CV_32S
    )

    min_area = 500
    valid_clusters = []
    for i in range(1, num_labels):
        if stats[i, cv2.CC_STAT_AREA] >= min_area:
            valid_clusters.append((i, centroids[i]))

    if not valid_clusters:
        h, w = canny_img.shape
        return w // 2, h // 2, 40

    best_cluster = max(valid_clusters, key=lambda x: stats[x[0], cv2.CC_STAT_AREA])
    label_id = best_cluster[0]
    cx, cy = best_cluster[1]
    area = stats[label_id, cv2.CC_STAT_AREA]

    # Оцениваем радиус как радиус круга той же площади
    estimated_radius = math.sqrt(area / math.pi) * 0.85
    return int(cx), int(cy), int(estimated_radius)


def optimize_pentagon_constrained(canny_img, start_cx, start_cy, start_radius, iterations=150):
    canny_bin = (canny_img > 50).astype(np.uint8)

    w_boundary = 1000.0
    w_internal = 1.0
    w_area = 0.05

    current_cx, current_cy = start_cx, start_cy
    current_R = max(15, start_radius)
    # Деформации: [k_top, k_right_up, k_bot, k_left_up]
    # k_bot применяется к обеим нижним вершинам для горизонтального ребра
    current_k = [1.0, 1.0, 1.0, 1.0]

    print(f"{'Iter': <5} | {'CX': <6} | {'CY': <6} | {'R': <5} | {'k': <15} | {'Score': <10} ")
    print("-" * 65)

    for i in range(iterations):
        improved = False
        current_pts = generate_constrained_pentagon(current_cx, current_cy, current_R, current_k)
        current_score, _, _, _ = calculate_score(canny_bin, current_pts, w_area, w_boundary, w_internal)

        if i % 10 == 0:
            k_str = f"{current_k[0]:.2f},{current_k[1]:.2f},{current_k[2]:.2f},{current_k[3]:.2f}"
            print(
                f"{i: <5} | {current_cx: <6} | {current_cy: <6} | {current_R: <5} | {k_str: <15} | {current_score: <10.1f} ")

        # 1. Оптимизация центра (CX, CY)
        for dcx in range(-3, 4, 1):
            for dcy in range(-3, 4, 1):
                if dcx == 0 and dcy == 0: continue
                temp_pts = generate_constrained_pentagon(current_cx + dcx, current_cy + dcy, current_R, current_k)
                new_score, _, _, _ = calculate_score(canny_bin, temp_pts, w_area, w_boundary, w_internal)
                if new_score > current_score:
                    current_score = new_score
                    current_cx += dcx
                    current_cy += dcy
                    improved = True

        # 2. Оптимизация радиуса (R)
        for dR in [-3, -1, 1, 3]:
            new_R = current_R + dR
            if new_R < 15: continue
            temp_pts = generate_constrained_pentagon(current_cx, current_cy, new_R, current_k)
            new_score, _, _, _ = calculate_score(canny_bin, temp_pts, w_area, w_boundary, w_internal)
            if new_score > current_score:
                current_score = new_score
                current_R = new_R
                improved = True

        # 3. Оптимизация коэффициентов деформации (форма)
        for idx in range(4):  # 0,1,2,3 (3-й коэффициент управляет обеими нижними вершинами)
            best_k = current_k[idx]
            for dk in [-0.15, -0.05, 0.05, 0.15]:
                new_k_val = current_k[idx] + dk
                if new_k_val < 0.5: continue

                temp_k = current_k.copy()
                temp_k[idx] = new_k_val
                temp_pts = generate_constrained_pentagon(current_cx, current_cy, current_R, temp_k)
                new_score, _, _, _ = calculate_score(canny_bin, temp_pts, w_area, w_boundary, w_internal)

                if new_score > current_score:
                    current_score = new_score
                    current_k[idx] = new_k_val
                    improved = True

        if not improved:
            print(f"Сходимость достигнута на итерации {i}")
            break

    final_pts = generate_constrained_pentagon(current_cx, current_cy, current_R, current_k)
    final_score, f_area, f_bound, f_int = calculate_score(canny_bin, final_pts, w_area, w_boundary, w_internal)
    k_str = f"{current_k[0]:.2f},{current_k[1]:.2f},{current_k[2]:.2f},{current_k[3]:.2f}"
    print(
        f"{'Final': <5} | {current_cx: <6} | {current_cy: <6} | {current_R: <5} | {k_str: <15} | {final_score: <10.1f} ")

    return final_pts


def main(mark, image, canny_img):
    # 1. Инициализация параметров
    start_cx, start_cy, start_radius = get_smart_initial_params(mark, canny_img)

    # 2. Оптимизация с учётом ограничений
    final_pts = optimize_pentagon_constrained(canny_img, start_cx, start_cy, start_radius)

    # 3. Визуализация
    res_img = np.array(image.copy())
    pts = np.array(final_pts, np.int32).reshape((-1, 1, 2))
    cv2.polylines(res_img, [pts], True, (0, 255, 0), 3)
    return res_img