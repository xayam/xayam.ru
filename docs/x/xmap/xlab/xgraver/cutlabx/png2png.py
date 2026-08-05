import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread('input.png', cv2.IMREAD_GRAYSCALE)
_, binary_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY)
binary_image = 255 - binary_image
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
    binary_image, connectivity=8
)

object_ids = np.arange(1, num_labels)
centroids_objs = centroids[1:]

sort_idx = np.lexsort((centroids_objs[:, 0], centroids_objs[:, 1]))
sorted_old_labels = object_ids[sort_idx]

# Создаём новую карту меток, где первый по порядку объект = 1, второй = 2 и т.д.
new_labels = np.zeros_like(labels)

for new_id, old_label in enumerate(sorted_old_labels, start=1):
    mask = (labels == old_label)
    new_labels[mask] = new_id

original_pixels_restored = (new_labels > 0).astype(np.uint8) * 255
# Это бинарное изображение, идентичное исходному `binary` (если не было фильтрации)
assert np.array_equal(binary_image, original_pixels_restored), "Пиксели изменились!"

# Создаём RGB-изображение для цветного отображения
height, width = labels.shape
colored = np.zeros((height, width, 3), dtype=np.uint8)

# Генерируем уникальный цвет для каждой метки (кроме фона = 0)
for label in range(1, num_labels):
    # Угол в HSV: равномерно распределяем по кругу
    hue = int(255 * label / (num_labels - 1))  # 0–255 для OpenCV
    # Насыщенность и яркость — максимум
    colored[labels == label] = np.array([hue, 255, 255], dtype=np.uint8)

# Конвертируем из HSV в BGR (OpenCV работает в BGR!)
colored_bgr = cv2.cvtColor(colored, cv2.COLOR_HSV2BGR)

cv2.imwrite("output.png", colored_bgr)

# Визуализация
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.imshow(binary_image, cmap='gray')
plt.title('Исходное бинарное изображение')

plt.subplot(1, 2, 2)
plt.imshow(cv2.cvtColor(colored_bgr, cv2.COLOR_BGR2RGB))
plt.title(f'Кластеризация: {num_labels - 1} объектов')

plt.show()

print(f'Обнаружено объектов: {num_labels - 1}')  # минус фон (метка 0)
