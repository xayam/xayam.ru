import torch
import numpy as np
import cv2
import trimesh
from PIL import Image
from transformers import AutoProcessor, Owlv2ForObjectDetection

# ------------------------------------------------------------------
# 1. OWLv2: Open-Vocabulary Детекция
# ------------------------------------------------------------------
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
det_processor = AutoProcessor.from_pretrained("google/owlv2-base-patch16-ensemble")
det_model = Owlv2ForObjectDetection.from_pretrained("google/owlv2-base-patch16-ensemble").to(DEVICE)


# ------------------------------------------------------------------
# 2. CenterPose-style Keypoint Estimator (упрощённый)
# ------------------------------------------------------------------
class SimpleKeypointPose:
    """
    Упрощённая реализация логики CenterPose:
    детекция → 2D кейпоинты → PnP → 6D поза.

    Для продакшена замените на обученную CenterPose модель через TAO/Isaac ROS.
    """

    def __init__(self, cad_path: str, K: np.ndarray, num_keypoints: int = 8):
        self.K = K
        self.num_keypoints = num_keypoints

        # Загрузка CAD и извлечение 3D ключевых точек (вершины ограничивающего кубоида)
        mesh = trimesh.load(cad_path, force="mesh")
        self.keypoints_3d = self._extract_cuboid_vertices(mesh)  # (8, 3)

        print(f"✅ Инициализировано {num_keypoints} 3D кейпоинтов")

    def _extract_cuboid_vertices(self, mesh: trimesh.Trimesh) -> np.ndarray:
        """Извлекает 8 вершин ограничивающего кубоида из меша."""
        bounds = mesh.bounds  # (2, 3): [min, max]
        min_corner, max_corner = bounds[0], bounds[1]

        # Все 8 комбинаций координат кубоида
        vertices = []
        for x in [min_corner[0], max_corner[0]]:
            for y in [min_corner[1], max_corner[1]]:
                for z in [min_corner[2], max_corner[2]]:
                    vertices.append([x, y, z])
        return np.array(vertices)

    def estimate_pose(self, image: np.ndarray, bbox: np.ndarray) -> dict:
        """
        Оценка позы через детекцию кейпоинтов + PnP.
        В прототипе: кейпоинты аппроксимируются через grid внутри bbox.
        """
        x1, y1, x2, y2 = map(int, bbox)
        roi = image[y1:y2, x1:x2]
        h, w = roi.shape[:2]

        # 🎯 Прототип: генерация 2D кейпоинтов как равномерная сетка
        # В реальности: здесь должна быть нейросеть, предсказывающая кейпоинты
        keypoints_2d = []
        for i in range(self.num_keypoints):
            # Простая эвристика: распределить точки по периметру bbox
            t = i / self.num_keypoints
            if i < 4:  # верхняя грань
                px = x1 + int(w * t)
                py = y1
            elif i < 8:  # правая грань
                px = x2
                py = y1 + int(h * (t - 0.25) * 4)
            else:  # остальные — заглушка
                px = x1 + int(w * 0.5)
                py = y1 + int(h * 0.5)
            keypoints_2d.append([px, py])
        keypoints_2d = np.array(keypoints_2d, dtype=np.float32)

        # 🎯 PnP: решение задачи Perspective-n-Point
        # Используем RANSAC для робастности к выбросам
        success, rvec, tvec, _ = cv2.solvePnPRansac(
            objectPoints=self.keypoints_3d.astype(np.float32),
            imagePoints=keypoints_2d,
            cameraMatrix=self.K.astype(np.float32),
            distCoeffs=None,  # без дисторсии или добавьте коэффициенты
            iterationsCount=100,
            reprojectionError=8.0
        )

        if not success:
            return {"R": np.eye(3), "t": np.zeros(3), "success": False}

        # Конвертация rvec → матрица вращения
        R, _ = cv2.Rodrigues(rvec)

        return {
            "R": R,
            "t": tvec.flatten(),
            "keypoints_2d": keypoints_2d,
            "success": True
        }


# ------------------------------------------------------------------
# 3. Утилиты
# ------------------------------------------------------------------
def get_top_face_center_local(mesh: trimesh.Trimesh) -> np.ndarray:
    """Центр грани с нормалью, ближайшей к +Z."""
    z_axis = np.array([0, 0, 1])
    cos_angles = mesh.face_normals @ z_axis
    top_idx = np.argmax(cos_angles)
    return mesh.triangles_center[top_idx]


def project_3d_to_2d(point_3d: np.ndarray, K: np.ndarray):
    """Pinhole проекция."""
    p_cam = K @ point_3d
    if p_cam[2] <= 1e-3:
        return None
    return int(p_cam[0] / p_cam[2]), int(p_cam[1] / p_cam[2])


# ------------------------------------------------------------------
# 4. Основной пайплайн
# ------------------------------------------------------------------
def run_d12_centerpose_pipeline(
        image_path: str,
        prompt: str,
        cad_path: str,
        K: np.ndarray
):
    """Пайплайн: OWLv2 → CenterPose-style pose → центр верхней грани."""

    # Загрузка изображения
    img_pil = Image.open(image_path).convert("RGB")
    img_np = np.array(img_pil)
    h, w = img_np.shape[:2]

    # OWLv2 детекция
    inputs = det_processor(text=[prompt], images=img_pil, return_tensors="pt").to(DEVICE)
    with torch.no_grad():
        outputs = det_model(**inputs)
    target_sizes = torch.tensor([[h, w]])
    results = det_processor.post_process_object_detection(
        outputs, threshold=0.15, target_sizes=target_sizes
    )[0]

    if len(results["boxes"]) == 0:
        print("❌ Объекты не найдены.")
        return

    # Загрузка CAD
    mesh = trimesh.load(cad_path, force="mesh")
    top_center_local = get_top_face_center_local(mesh)

    # Инициализация pose-оценщика
    pose_estimator = SimpleKeypointPose(cad_path, K)

    # Инференс
    vis = img_np.copy()
    boxes = results["boxes"].cpu().numpy()
    scores = results["scores"].cpu().numpy()

    for i, box in enumerate(boxes):
        if scores[i] < 0.3:
            continue

        x1, y1, x2, y2 = map(int, box)
        cv2.rectangle(vis, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(vis, f"D12 {scores[i]:.2f}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Оценка позы
        pose = pose_estimator.estimate_pose(img_np, box)
        if not pose["success"]:
            continue

        R, t = pose["R"], pose["t"]

        # Перевод центра верхней грани в камеру
        top_center_cam = R @ top_center_local + t
        pt_2d = project_3d_to_2d(top_center_cam, K)

        if pt_2d:
            cv2.circle(vis, pt_2d, 6, (0, 0, 255), -1)
            cv2.putText(vis, "TOP", (pt_2d[0] + 10, pt_2d[1]),
                        cv2.FONT_HERSHEY_SIMPLEX, 2.5, (0, 0, 255), 2)

        # Отрисовка кейпоинтов (для отладки)
        for kp in pose["keypoints_2d"]:
            cv2.circle(vis, tuple(map(int, kp)), 3, (255, 0, 0), -1)

    out_path = "d12_centerpose_output.jpg"
    cv2.imwrite(out_path, vis)
    print(f"✅ Результат: {out_path}")
    return out_path


# ------------------------------------------------------------------
# 5. Запуск
# ------------------------------------------------------------------
if __name__ == "__main__":
    K = np.array([
        [1500.0, 0.0, 960.0],
        [0.0, 1500.0, 540.0],
        [0.0, 0.0, 1.0]
    ])

    run_d12_centerpose_pipeline(
        image_path="input.jpg",
        prompt="d12 dice",
        cad_path="blankd12.obj",
        K=K
    )