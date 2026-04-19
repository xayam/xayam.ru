import cv2
import numpy as np
import os, sys
from ultralytics import YOLO

# === НАСТРОЙКИ ===
INPUT_FILE = "input.jpg"  # Ваше изображение
OUTPUT_FILE = "output.jpg"  # Результат с точками
MODEL_PATH = "yolov8s-worldv2.pt"  # Модель (скачается автоматически)
CLASSES = ["dice", "die", "D6", "D12", "cube", "game piece"]
CONF_THRESHOLD = 0.005  # Порог уверенности (0.0–1.0)
# =================

if not os.path.exists(INPUT_FILE):
    sys.exit(f"❌ Файл {INPUT_FILE} не найден")

print("🔍 Загрузка модели и поиск кубиков...")
model = YOLO(MODEL_PATH)
model.set_classes(CLASSES)
results = model.predict(INPUT_FILE, conf=CONF_THRESHOLD, verbose=False, device="cpu")

img = cv2.imread(INPUT_FILE)
if img is None:
    sys.exit("❌ Не удалось прочитать изображение")

count = 0
for box in results[0].boxes.xyxy.cpu().numpy():
    x1, y1, x2, y2 = map(int, box)

    # 🎯 Уточнение центра через контур внутри бокса (работает на сложном фоне)
    roi = img[y1:y2, x1:x2]
    if roi.size == 0: continue

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    th = cv2.morphologyEx(th, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))

    cnts, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if cnts:
        cnt = max(cnts, key=cv2.contourArea)
        area = cv2.contourArea(cnt)
        if area > 100:  # Фильтр шума
            M = cv2.moments(cnt)
            if M["m00"] > 0:
                # 📐 Субпиксельный центр относительно всего изображения
                cx = x1 + M["m10"] / M["m00"]
                cy = y1 + M["m01"] / M["m00"]

                # Отрисовка
                cv2.circle(img, (int(round(cx)), int(round(cy))), 7, (0, 0, 255), -1)
                cv2.circle(img, (int(round(cx)), int(round(cy))), 14, (255, 255, 0), 2)
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 1)
                print(f"🎲 #{count + 1}: X={cx:.3f}, Y={cy:.3f} px")
                count += 1
    else:
        # Fallback: центр бокса, если контур не найден
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        cv2.circle(img, (cx, cy), 7, (0, 0, 255), -1)
        cv2.circle(img, (cx, cy), 14, (255, 255, 0), 2)
        print(f"🎲 #{count + 1}: X={cx:.1f}, Y={cy:.1f} px (bbox-center)")
        count += 1

cv2.imwrite(OUTPUT_FILE, img)
print(f"\n✅ Готово. Найдено центров: {count}. Сохранено в {OUTPUT_FILE}")