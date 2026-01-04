import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.spatial.distance import cdist

np.random.seed(42)

def get_trajectory(filename='input.png'):
    image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    _, binary_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY)
    binary_image = 255 - binary_image
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
        binary_image, connectivity=8
    )

    # Пропускаем фон (метка 0)
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

    last_point = np.array([0, 0])  # начальная позиция (можно выбрать любую)

    for cluster in ordered_clusters:
        pixels = cluster['pixels']  # (N, 2) — [y, x]

        # Найти ближайшую точку к последней позиции — это старт кластера
        dists = cdist([last_point], pixels)[0]
        start_idx = np.argmin(dists)
        start_point = pixels[start_idx]

        # Удалим start_point из списка и начнём с него
        remaining = np.delete(pixels, start_idx, axis=0)

        # Простой способ обхода внутри: отсортировать по расстоянию от текущей точки (жадно)
        # (можно заменить на змейку, если кластер плотный)
        current = start_point
        cluster_path = [current]
        while len(remaining) > 0:
            dists = cdist([current], remaining)[0]
            next_idx = np.argmin(dists)
            current = remaining[next_idx]
            cluster_path.append(current)
            remaining = np.delete(remaining, next_idx, axis=0)

        # Добавляем путь по кластеру в общую траекторию
        trajectory.append(cluster_path)
        last_point = cluster_path[-1]  # обновляем последнюю позицию

    # trajectory = np.array(trajectory)
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
            trajectory[i] = np.array(trajectory[i])
            ys, xs = trajectory[i][:idx, 0], trajectory[i][:idx, 1]
            canvas[ys, xs] = 0
        im.set_array(canvas)
        return [im]

    ani = FuncAnimation(fig, animate, frames=len(frames), interval=25, blit=True, repeat=False)
    binary_image = 255 - binary_image
    assert canvas.any() == binary_image.any(), "Error! canvas != binary_image"
    ani.save("output.gif")

if __name__ == "__main__":
    main()
