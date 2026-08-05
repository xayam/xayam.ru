import cv2
import numpy as np
import os

def smooth_wood_preserve_edges(img,
                               d=11, sigma_color=50, sigma_space=50,
                               canny_low=30, canny_high=100,
                               dilate_k=3, soft_blend=False):
    # 1. Сглаживание с сохранением границ (аналог Surface Blur)
    # d: диаметр окрестности (должно быть нечётным)
    # sigmaColor: насколько сильно пиксели могут отличаться по цвету, чтобы сглаживаться
    # sigmaSpace: радиус пространственного влияния
    smoothed = cv2.bilateralFilter(img, d=d,
                                   sigmaColor=sigma_color,
                                   sigmaSpace=sigma_space)
    # 2. Детекция рёбер для создания защитной маски
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, canny_low, canny_high)
    # Утолщаем рёбра, чтобы эффект сглаживания не "залезал" на стыки
    if dilate_k > 1:
        kernel = np.ones((dilate_k, dilate_k), np.uint8)
        edges = cv2.dilate(edges, kernel, iterations=1)
    # 3. Нормализуем маску в [0.0, 1.0] и расширяем до 3 каналов
    mask = edges.astype(np.float32) / 255.0
    mask_3ch = cv2.merge([mask, mask, mask])
    # Опционально: мягкий переход вокруг рёбер (убирает "ступеньки")
    if soft_blend:
        mask_3ch = cv2.GaussianBlur(mask_3ch, (5, 5), 0)
    # 4. Линейная интерполяция: на рёбрах = оригинал, внутри = сглаженный
    result = (img.astype(np.float32) * mask_3ch +
              smoothed.astype(np.float32) * (1.0 - mask_3ch))
    result = np.clip(result, 0, 255).astype(np.uint8)
    return result

if __name__ == "__main__":
    pass
