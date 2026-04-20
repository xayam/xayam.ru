import torch
from transformers import AutoProcessor, Owlv2ForObjectDetection
from PIL import Image, ImageDraw

# 1. Загрузка модели и процессора
MODEL_ID = "google/owlv2-base-patch16-ensemble"
processor = AutoProcessor.from_pretrained(MODEL_ID)
model = Owlv2ForObjectDetection.from_pretrained(MODEL_ID)

# Опционально: перенос на GPU для ускорения
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

def detect(prompts=("dice", "other"), img_source="input.jpg"):
    image = Image.open(img_source).convert("RGB")
    inputs = processor(text=list(prompts),
                       images=image,
                       return_tensors="pt",
                       padding=True,
                       truncation=True).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    # Постобработка и фильтрация по confidence threshold
    target_sizes = torch.tensor([image.size[::-1]])
    results = processor.post_process_object_detection(
        outputs=outputs, threshold=0.15, target_sizes=target_sizes
    )[0]
    # Отрисовка рамок на изображении
    draw = ImageDraw.Draw(image)
    # font = ImageFont.load_default()
    count = 0
    result = []
    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        if score > 0.39:
            count += 1
            box = [int(i) for i in box.tolist()]
            class_name = prompts[label]
            sizes = box[0] - 20, box[1] - 20, box[2] + 20, box[3] + 20
            output_path = f"{img_source}.output{count}.jpg"
            result.append(output_path)
            saver = image.crop(sizes)
            saver.save(output_path)
            print(class_name, str(box[2] - box[0]), str(score))
            draw.rectangle(sizes, outline="lime", width=3)
            # text = f"{class_name} {score:.2f}"
            # draw.text((box[0], box[1]), text, fill="lime", font=font)
    print(f"✅ Обнаружено {count} объектов")
    output_path = f"{img_source}.output.jpg"
    image.save(output_path)
    return result

def main():
    detect()

if __name__ == "__main__":
    main()
