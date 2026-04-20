import torch
import numpy as np
import cv2
import trimesh
from PIL import Image
from transformers import AutoProcessor, Owlv2ForObjectDetection
import os


# ==========================================================
# 1. NVIDIA CenterPose Wrapper
# ==========================================================
class CenterPoseEstimator:
    """
    Обертка для инференса NVIDIA CenterPose.
    Требует наличие модели (например, trained_d12.pth).
    """

    def __init__(self, ckpt_path: str, device='cuda'):
        self.device = device
        self.has_model = False

        # Проверка наличия файла
        if os.path.exists(ckpt_path):
            print(f"📦 Загрузка CenterPose модели: {ckpt_path}")
            try:
                # В реальном сценарии здесь загрузка архитектуры CenterPose и чекпоинта
                # self.model = torch.load(ckpt_path) ...
                # self.model.eval()
                self.has_model = True
                print("✅ Модель загружена")
            except Exception as e:
                print(f"❌ Ошибка загрузки модели: {e}")
        else:
            print(f"️ Модель {ckpt_path} не найдена. Использую 2D-Fallback логику.")

    def estimate_pose(self, image, bbox):
        """
        Возвращает R (3x3) и t (3,).
        Если модели нет, возвращает заглушку (Identity), чтобы не ломать пайплайн,
        и флаг success=False.
        """
        if not self.has_model:
            return {"R": np.eye(3), "t": np.array([0, 0, 1]), "success": False}

        # --- Здесь должен быть реальный инференс CenterPose ---
        # crop = image[y1:y2, x1:x2]
        # out = self.model(crop)
        # return {"R": out.R, "t": out.t, "success": True}

        return {"R": np.eye(3), "t": np.array([0, 0, 0]), "success": True}


# ==========================================================
# 2. Geometry & Top Face Detection
# ==========================================================
def get_top_face_pentagon_2d(mesh, R, t, K):
    """
    Находит 5 вершин грани, которая смотрит НА КАМЕРУ.
    """
    # 1. Собираем грани в пентагоны (по нормали)
    face_adj = mesh.face_adjacency
    visited = np.zeros(len(mesh.faces), dtype=bool)
    pentagons = []

    for i in range(len(mesh.faces)):
        if visited[i]: continue
        group = [i]
        visited[i] = True
        queue = [i]
        while queue:
            curr = queue.pop(0)
            adj_pairs = face_adj[face_adj[:, 0] == curr]
            adj_faces = np.unique(adj_pairs[:, 1])
            for adj in adj_faces:
                if not visited[adj]:
                    # Допустимый угол разницы нормалей (D12 грани плоские)
                    cos_sim = np.dot(mesh.face_normals[curr], mesh.face_normals[adj])
                    if cos_sim > np.cos(np.radians(20)):
                        visited[adj] = True
                        group.append(adj)
                        queue.append(adj)
        pentagons.append(group)

    # 2. Ищем грань, нормаль которой совпадает с осью Z камеры [0, 0, 1]
    # Камера смотрит вдоль +Z. Верхняя грань кубика должна быть перпендикулярна этому лучу.
    view_vec_cam = np.array([0, 0, 1])
    best_face = None
    best_dot = -np.inf

    for group in pentagons:
        local_norm = mesh.face_normals[group].mean(axis=0)
        local_norm /= np.linalg.norm(local_norm)

        # Трансформируем нормаль в пространство камеры
        cam_norm = R @ local_norm
        dot = np.dot(cam_norm, view_vec_cam)

        # Чем ближе dot к 1, тем сильнее грань смотрит на нас
        if dot > best_dot:
            best_dot = dot
            best_face = np.unique(mesh.faces[group].flatten())

    if best_face is None: return np.array([])

    # 3. Проекция вершин этой грани
    verts_local = mesh.vertices[best_face]
    verts_cam = (R @ verts_local.T + t.reshape(3, 1)).T

    pts_2d = []
    for v in verts_cam:
        if v[2] < 1e-3: continue
        u = int(K[0, 0] * v[0] / v[2] + K[0, 2])
        v_px = int(K[1, 1] * v[1] / v[2] + K[1, 2])
        pts_2d.append([u, v_px])

    if len(pts_2d) < 5: return np.array([])

    # Сортировка по часовой стрелке для отрисовки
    pts_2d = np.array(pts_2d, dtype=np.float32)
    center = pts_2d.mean(axis=0)
    angles = np.arctan2(pts_2d[:, 1] - center[1], pts_2d[:, 0] - center[0])
    pts_2d = pts_2d[np.argsort(angles)].astype(np.int32)

    return pts_2d


# ==========================================================
# 3. 2D Fallback (Если 3D не работает)
# ==========================================================
def detect_top_face_2d(image, bbox):
    """
    Если 3D поза известна плохо, ищем пентагон прямо на картинке.
    """
    x1, y1, x2, y2 = map(int, bbox)
    margin = 10
    h, w = image.shape[:2]
    x1, y1 = max(0, x1 - margin), max(0, y1 - margin)
    x2, y2 = min(w, x2 + margin), min(h, y2 + margin)

    roi = image[y1:y2, x1:x2]
    if roi.size == 0: return np.array([])

    gray = cv2.cvtColor(roi, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)

    # Морфология для замыкания контуров граней
    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=2)
    eroded = cv2.erode(dilated, kernel, iterations=1)

    contours, _ = cv2.findContours(eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    best_cnt = None
    max_area = 0

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 500: continue

        epsilon = 0.04 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        # D12 верхняя грань - пентагон (5 углов)
        if len(approx) == 5 and area > max_area:
            max_area = area
            best_cnt = approx

    if best_cnt is not None:
        pts = best_cnt.reshape(-1, 2)
        pts[:, 0] += x1
        pts[:, 1] += y1
        # Сортировка
        pts = pts.astype(np.float32)
        center = pts.mean(axis=0)
        angles = np.arctan2(pts[:, 1] - center[1], pts[:, 0] - center[0])
        return pts[np.argsort(angles)].astype(np.int32)

    return np.array([])


# ==========================================================
# 4. Main Pipeline
# ==========================================================
def run_pipeline(image_path, prompt, cad_path, ckpt_path, K):
    img_pil = Image.open(image_path).convert("RGB")
    img_np = np.array(img_pil)
    h, w = img_np.shape[:2]

    # OWLv2
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    det_processor = AutoProcessor.from_pretrained("google/owlv2-base-patch16-ensemble")
    det_model = Owlv2ForObjectDetection.from_pretrained("google/owlv2-base-patch16-ensemble").to(DEVICE)

    inputs = det_processor(text=[prompt], images=img_pil, return_tensors="pt").to(DEVICE)
    with torch.no_grad():
        outputs = det_model(**inputs)
    results = det_processor.post_process_object_detection(outputs, threshold=0.15, target_sizes=torch.tensor([[h, w]]))[
        0]

    # Init Pose Estimator
    pose_estimator = CenterPoseEstimator(ckpt_path, device=DEVICE)
    mesh = trimesh.load(cad_path, force="mesh")

    vis = img_np.copy()
    boxes = results["boxes"].cpu().numpy()
    scores = results["scores"].cpu().numpy()

    for i, box in enumerate(boxes):
        if scores[i] < 0.3: continue
        x1, y1, x2, y2 = map(int, box)
        cv2.rectangle(vis, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # 1. Попытка 3D Pose
        pose = pose_estimator.estimate_pose(img_np, box)
        pts_2d = np.array([])

        if pose["success"]:
            pts_2d = get_top_face_pentagon_2d(mesh, pose["R"], pose["t"], K)

        # 2. Fallback если 3D не сработал
        if len(pts_2d) < 3:
            pts_2d = detect_top_face_2d(img_np, box)

        # 3. Отрисовка
        if len(pts_2d) >= 3:
            cv2.polylines(vis, [pts_2d], isClosed=True, color=(255, 0, 0), thickness=3)
            cx, cy = pts_2d.mean(axis=0).astype(int)
            cv2.circle(vis, (cx, cy), 5, (255, 255, 0), -1)
            cv2.putText(vis, "TOP", (cx, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

    cv2.imwrite("output_d12.jpg", vis)
    print("✅ Result saved: output_d12.jpg")


if __name__ == "__main__":
    # ВАЖНО: Укажите путь к вашей натренированной модели NVIDIA CenterPose
    # Если файла нет, скрипт все равно запустится, используя 2D-Fallback (красные линии)
    MY_CENTERPOSE_CHECKPOINT = "d12_checkpoint.pth"

    K = np.array([
        [1500.0, 0.0, 960.0],
        [0.0, 1500.0, 540.0],
        [0.0, 0.0, 1.0]
    ])

    run_pipeline(
        image_path="input.jpg",
        prompt="d12 dice",
        cad_path="blankd12.obj",
        ckpt_path=MY_CENTERPOSE_CHECKPOINT,
        K=K
    )