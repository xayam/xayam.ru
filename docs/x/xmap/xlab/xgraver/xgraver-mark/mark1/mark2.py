import cv2
import numpy as np
import torch
import os, sys
from ultralytics import YOLO
from mobile_sam import sam_model_registry, SamPredictor

# === НАСТРОЙКИ ===
INPUT_FILE = "input.jpg"
OUTPUT_FILE = "output_subpixel.jpg"
SAM_WEIGHTS = "mobile_sam.pt"  # ← Ваш локальный файл
CLASSES = ["dice", "die", "D6", "D12", "cube", "game piece"]
CONF_THRESHOLD = 0.25
# =================

if not os.path.exists(INPUT_FILE):
    sys.exit(f"❌ {INPUT_FILE} не найден")
if not os.path.exists(SAM_WEIGHTS):
    sys.exit(f"❌ {SAM_WEIGHTS} не найден. Скачайте его вручную и положите рядом со скриптом.")

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"🖥️ Устройство: {device.upper()}")

# 1. Zero-shot детекция (YOLO-World)
print("🔍 Поиск кубиков...")
model = YOLO("yolov8s-worldv2.pt")  # Первое подключение скачает ~15 МБ
model.set_classes(CLASSES)
results = model.predict(INPUT_FILE, conf=CONF_THRESHOLD, verbose=False)
boxes = results[0].boxes.xyxy.cpu().numpy()

if len(boxes) == 0:
    sys.exit("🤷 Не найдено объектов. Уменьшите CONF_THRESHOLD или измените CLASSES")

# 2. Загрузка MobileSAM из локального файла
print("🎯 Загрузка MobileSAM...")
sam = sam_model_registry["vit_t"](checkpoint=SAM_WEIGHTS).to(device).eval()
predictor = SamPredictor(sam)
image_cv = cv2.imread(INPUT_FILE)
predictor.set_image(image_cv)

# 3. Обработка: маска → субпиксельный центр
out_img = image_cv.copy()
with torch.no_grad():
    for i, box in enumerate(boxes):
        masks, _, _ = predictor.predict(box=box[None, :], multimask_output=False)
        mask = (masks[0][0] > 0.5).astype(np.uint8) * 255
        M = cv2.moments(mask)
        if M["m00"] > 0:
            cx, cy = M["m10"]/M["m00"], M["m01"]/M["m00"]  # 📐 субпиксельные координаты
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(out_img, contours, -1, (0, 255, 0), 2)
            cv2.circle(out_img, (int(round(cx)), int(round(cy))), 6, (0, 0, 255), -1)
            cv2.circle(out_img, (int(round(cx)), int(round(cy))), 12, (255, 255, 0), 2)
            print(f"🎲 #{i+1}: X={cx:.3f}, Y={cy:.3f} px")

cv2.imwrite(OUTPUT_FILE, out_img)
print(f"✅ Готово. Найдено: {len(boxes)}. Сохранено в {OUTPUT_FILE}")