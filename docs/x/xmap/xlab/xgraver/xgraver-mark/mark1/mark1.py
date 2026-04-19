import cv2
import numpy as np
from transformers import pipeline
from PIL import Image
import sys
import os

INPUT_FILE = "input.jpg"  # Ваше изображение
OUTPUT_FILE = "output.jpg"  # Результат с точками

if not os.path.exists(INPUT_FILE):
    sys.exit("❌ Файл не найден. Положите картинку рядом со скриптом.")

print("⏳ Загрузка AI-модели (первый запуск скачает ~350 МБ)...")
# OWLv2: современная zero-shot модель для детекции по текстовому запросу
detector = pipeline("zero-shot-object-detection", model="google/owlv2-base-patch16-ensemble")

image = Image.open(INPUT_FILE)
print("🔍 Поиск верхней грани кубиков D12 додекаэдра")
# Ищем по синонимам, порог уверенности 0.15 отбрасывает мусор
results = detector(image,
                   candidate_labels=["dice",
                                     ""],
                   threshold=0.15
                   )

img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
count = 0

for res in results:
    box = res["box"]
    # Центр ограничивающей рамки
    cx = int((box["xmin"] + box["xmax"]) / 2)
    cy = int((box["ymin"] + box["ymax"]) / 2)

    cv2.circle(img_cv, (cx, cy), 10, (0, 255, 0), -1)  # 🟢 Центр
    cv2.circle(img_cv, (cx, cy), 18, (0, 0, 255), 2)  # 🔴 Обводка
    count += 1

cv2.imwrite(OUTPUT_FILE, img_cv)
print(f"✅ Готово. Найдено кубиков: {count}. Сохранено в {OUTPUT_FILE}")