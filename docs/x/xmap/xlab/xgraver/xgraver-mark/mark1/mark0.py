import cv2

# 1. Захват одного кадра
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cap.release()
if not ret:
    raise SystemExit("❌ Камера не отвечает")

# 2. Базовая обработка
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (9, 9), 0)
thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                               cv2.THRESH_BINARY_INV, 11, 5)

# 3. Поиск центров
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
count = 0
for cnt in contours:
    area = cv2.contourArea(cnt)
    # 👇 Подстройте этот диапазон под ваше расстояние камеры
    if 4000 < area < 200000:  
        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cx, cy = int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"])
            cv2.circle(frame, (cx, cy), 8, (0, 0, 255), -1)   # точка
            cv2.circle(frame, (cx, cy), 14, (0, 255, 0), 2)   # обводка
            count += 1

# 4. Вывод
cv2.imwrite("output.jpg", frame)
print(f"✅ Готово. Найдено центров: {count}")
print("🖼️ Откройте output.jpg или нажмите любую клавишу для просмотра")
cv2.imshow("Result", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()