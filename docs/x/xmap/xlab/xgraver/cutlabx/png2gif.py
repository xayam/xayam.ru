import sys

import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.spatial.distance import cdist
from telebot.service_utils import chunks

np.random.seed(42)

def contour_path(pixels, last_point):
    # 1. Создаём бинарную маску из пикселей кластера
    h, w = np.max(pixels, axis=0) + 10
    mask = np.zeros((h, w), dtype=np.uint8)
    for y, x in pixels:
        mask[y, x] = 255
    # 2. Находим все контуры (внешние + внутренние)
    contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    # 3. Преобразуем контуры в цепочки точек [ [y0,x0], [y1,x1], ... ]
    chains = []
    for cnt in contours:
        chain = [np.array([point[0][1], point[0][0]]) for point in cnt]  # [y, x]
        if len(chain) > 1:
            chains.append(chain)
    # 4. Сортируем цепочки по ближайшему расстоянию от last_point
    trajectory = []
    current = last_point
    while chains:
        # Находим ближайший конец любой цепочки
        best_idx, best_end, best_dist = None, None, float('inf')
        for i, chain in enumerate(chains):
            for end_idx in (0, -1):
                d = np.linalg.norm(current - chain[end_idx])
                if d < best_dist:
                    best_dist, best_idx, best_end = d, i, end_idx
        # Берём цепочку, возможно разворачиваем
        chain = chains.pop(best_idx)
        if best_end == -1:
            chain = chain[::-1]
        trajectory.extend(chain)
        current = chain[-1]
    return trajectory, current

def greedy_path(pixels, last_point):
    trajectory = []
    dists = cdist([last_point], pixels)[0]
    start_idx = np.argmin(dists)
    start_point = pixels[start_idx]
    remaining = np.delete(pixels, start_idx, axis=0)
    current = start_point
    cluster_path = [current]
    while len(remaining) > 0:
        dists = cdist([current], remaining)[0]
        next_idx = np.argmin(dists)
        current = remaining[next_idx]
        cluster_path.append(current)
        remaining = np.delete(remaining, next_idx, axis=0)
    trajectory.extend(cluster_path)
    last_point = cluster_path[-1]
    return trajectory, last_point

def matrix_path(pixels, last_point):
    rows = {}
    trajectory = []
    for y, x in pixels:
        rows.setdefault(y, []).append(x)
    sorted_ys = sorted(rows.keys())
    cluster_path = []
    for i, y in enumerate(sorted_ys):
        xs = sorted(rows[y])
        if i % 2 == 1:  # нечётная строка — меняем направление
            xs = xs[::-1]
        for x in xs:
            cluster_path.append(np.array([y, x]))
    if len(cluster_path) > 1:
        start_candidates = [cluster_path[0], cluster_path[-1]]
        dists_to_start = cdist([last_point], start_candidates)[0]
        if dists_to_start[1] < dists_to_start[0]:  # ближе конец змейки
            cluster_path = cluster_path[::-1]  # разворачиваем весь путь
    trajectory.extend(cluster_path)
    last_point = cluster_path[-1]
    return trajectory, last_point

def get_trajectory(filename='input.png',
                   algorithm=greedy_path, animate=True,
                   max_cluster_size=2000):
    image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    _, binary_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY)
    binary_image = 255 - binary_image
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
        binary_image, connectivity=4
    )
    cluster_data = []
    for label in range(1, num_labels):
        mask = (labels == label)
        ys, xs = np.where(mask)
        pixels = np.column_stack([ys, xs])  # (N, 2), [row, col] = [y, x]

        centroid = centroids[label]  # (x, y)
        cluster_data.append({
            'label': label,
            'pixels': pixels,  # все пиксели кластера
            'centroid': np.array([centroid[1], centroid[0]])  # [y, x] для согласования
        })

    def solve_tsp_greedy(centroids):
        n = len(centroids)
        visited = [False] * n
        order = []
        current = 0  # начинаем с первого
        visited[current] = True
        order.append(current)
        for _ in range(n - 1):
            last = centroids[current]
            distances = cdist([last], centroids)[0]
            distances[visited] = np.inf  # игнорируем посещённые
            next_idx = np.argmin(distances)
            visited[next_idx] = True
            order.append(next_idx)
            current = next_idx
        return order

    centroids_list = np.array([c['centroid'] for c in cluster_data])  # (K, 2)
    tsp_order = solve_tsp_greedy(centroids_list)
    ordered_clusters = [cluster_data[i] for i in tsp_order]

    trajectory = []
    last_point = np.array([0, 0])
    for cluster in ordered_clusters:
        pixels = cluster['pixels']  # (N, 2) — [y, x]
        chunks =  [
            pixels[i:i + max_cluster_size]
            for i in range(0, len(pixels), max_cluster_size)]
        for chunk in chunks:
            result, last_point = algorithm(chunk, last_point)
            trajectory.append(result)
            if animate:
                trajectory.extend(result)
            else:
                trajectory.append(result)
    if animate:
        trajectory = np.array(trajectory)
    return image.shape[1], image.shape[0], binary_image, trajectory

def main(filename="input.png"):
    _, _, binary_image, trajectory = get_trajectory(filename=filename)

    fig, ax = plt.subplots(figsize=(10, 7))
    ax.axis('off')
    canvas = np.ones_like(binary_image) * 255
    im = ax.imshow(canvas, cmap='gray', vmin=0, vmax=255)

    total = len(trajectory)
    step = max(1, total // 400)
    frames = list(range(0, total, step)) + [total]

    def animate(i):
        idx = frames[i]
        if idx > 0:
            ys, xs = trajectory[:idx, 0], trajectory[:idx, 1]
            canvas[ys, xs] = 0
        im.set_array(canvas)
        return [im]

    ani = FuncAnimation(fig, animate, frames=len(frames), interval=25, blit=True, repeat=False)
    binary_image = 255 - binary_image
    assert canvas.any() == binary_image.any(), "Error! canvas != binary_image"
    # ani.save("output.matrix.gif")
    ani.save("output.greedy.gif")

if __name__ == "__main__":
    main()
