import torch
import cv2
import numpy as np
import matplotlib.pyplot as plt
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel, UniPCMultistepScheduler
from diffusers.utils import load_image
import warnings

from finder import main as find_finder

warnings.filterwarnings("ignore")


class CannyEdgeDetector:
    def __init__(self, device="cuda" if torch.cuda.is_available() else "cpu"):
        self.device = device
        print(f"🚀 Загрузка модели на {device}...")
        # 1. Загружаем ControlNet Canny
        controlnet = ControlNetModel.from_pretrained(
            "lllyasviel/control_v11p_sd15_canny",
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            use_safetensors=True
        )
        # 2. Загружаем основную модель Stable Diffusion
        pipe = StableDiffusionControlNetPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            controlnet=controlnet,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            use_safetensors=True
        )
        # 3. Оптимизация скорости
        pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config)
        pipe.enable_model_cpu_offload() if device == "cuda" else None
        self.pipe = pipe
        print("✅ Модель готова!")

    def extract_canny_edges(self, input_image,
                            low_threshold=100,
                            high_threshold=200):
        """
        Извлекает Canny края через ControlNet
        """
        # Загрузка изображения
        # input_image = load_image(image_path)

        # Конвертация в numpy для OpenCV
        img_np = np.array(input_image)
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

        # Классический Canny для сравнения
        classical_edges = cv2.Canny(gray, low_threshold, high_threshold)

        # ControlNet автоматически извлекает края при генерации
        # Но мы можем получить их через детектор Canny из ControlNet
        control_image = input_image

        # Генерация (мы не используем результат генерации, а получаем края)
        # Для простоты - используем прямой Canny детектор
        # ControlNet сам использует Canny внутри

        # Сохраняем края
        # edges_pil = Image.fromarray(classical_edges)
        # edges_pil.save(save_path)

        return classical_edges, input_image

def main(mark_input):
    detector = CannyEdgeDetector(device="cpu")  # или "cuda" для GPU
    images = []
    for mark in mark_input:
        edges, original = detector.extract_canny_edges(
            mark["input_image"],  # ваше изображение
            low_threshold=9,  # ниже = больше деталей
            high_threshold=27  # выше = только сильные края
        )
        img_cv = np.array(mark["input_image"])
        gray_cv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray_cv, (9, 9), 0)
        edges_cv = cv2.Canny(blurred, 9, 27)
        images.append({
            "result": find_finder(mark, original, edges_cv),
            "edges": edges_cv
        })
    fig, axes = plt.subplots(2, len(images), figsize=(len(images), 2))
    index = 0
    for j in range(len(images)):
        if index >= len(images):
            break
        axes[0][j].imshow(images[index]["result"], cmap='gray')
        axes[0][j].set_title(str(index))
        axes[0][j].axis('off')
        axes[1][j].imshow(images[index]["edges"], cmap='gray')
        axes[1][j].set_title(str(index))
        axes[1][j].axis('off')
        index += 1
    plt.tight_layout()
    plt.savefig("comparison.png", dpi=150)
    plt.show()

if __name__ == "__main__":
    pass
