import pyvista as pv
import numpy as np
import random

from pathlib import Path
from collections import defaultdict

script_dir = str(Path(__file__).resolve().parent)

# Настройки сцены
MODEL_PATHS = [
    f'{script_dir}/v5.d6.chess-classic.black-white.glb',
    f"{script_dir}/v5.d6.chess-classic.white-black.glb",
    f"{script_dir}/v5.d12.chess-classic.glb",
    f"{script_dir}/v5.d12.chess-adds.white-black.glb",
    f"{script_dir}/v5.d12.chess-adds.black-white.glb"
]
OUTPUT_GIF = f'{script_dir}/d6-d12-presentation.gif'
BG_COLOR = "#aaaaaa"

plotter = pv.Plotter(off_screen=True)
plotter.background_color = BG_COLOR

model_actors = [] 
max_model_dim = 0.0

print("Загрузка моделей...")
for model_path in MODEL_PATHS:
    print(f"Загрузка модели {model_path.split('/')[-1]}...")
    mesh = pv.read(model_path).get_block(0)
    
    bounds = mesh.bounds
    dim = max(bounds[1]-bounds[0], bounds[3]-bounds[2], bounds[5]-bounds[4])
    if dim > max_model_dim:
        max_model_dim = dim
        
    mesh.translate(-np.array(mesh.center), inplace=True)
    
    # === ГРУППИРОВКА БЛОКОВ ПО ЦВЕТУ ===
    color_groups = defaultdict(list)
    
    for m in range(mesh.n_blocks):
        block = mesh.get_block(m)
        color_raw = block.get_block(0).get_block(0).field_data['BaseColorMultiplier'][0]
        
        # ИСПРАВЛЕНИЕ: преобразуем pyvista_ndarray в кортеж (tuple).
        # Кортежи хэшируемы, поэтому их можно использовать как ключи словаря.
        color_key = tuple(color_raw) 
        
        # Сохраняем в словарь пару: (сам блок, исходный формат цвета)
        color_groups[color_key].append((block, color_raw))
        
    current_actors = []
    for color_key, blocks_data in color_groups.items():
        # Извлекаем только блоки для их объединения
        blocks = [item[0] for item in blocks_data]
        # Берем исходный формат цвета для корректной передачи в движок рендера
        original_color = blocks_data[0][1] 
        
        combined_mesh = pv.MultiBlock(blocks).combine()
        actor = plotter.add_mesh(combined_mesh, color=original_color)
        current_actors.append(actor)
        
    model_actors.append(current_actors)

N = len(model_actors)

R = max_model_dim * 1.4 

angles = []
for i, actors in enumerate(model_actors):
    angle = i * (360.0 / N)
    x = R * np.cos(np.radians(angle))
    y = R * np.sin(np.radians(angle))
    angles.append([])
    for actor in actors:
        actor.position = (x, y, 0.0)
        angles[i].append([0.0, 0.0, 54.0])
        actor.orientation = angles[i][-1]

plotter.camera_position = 'iso'
plotter.camera.focal_point = (0.0, 0.0, 0.0)
plotter.reset_camera()
plotter.camera.zoom(1.3)

print("Рендеринг анимации...")
plotter.open_gif(OUTPUT_GIF, loop=0, fps=30)

loops = 1
frames = 360 * loops
orbit_step = 1.0 
spin_step  = 1.0

for frame in range(frames):
    print(f"Рендеринг фрейма {frame + 1}/{frames}")
    
    theta_orbit = frame * orbit_step
    
    for i, actors in enumerate(model_actors):
        angle = theta_orbit + i * (360.0 / N)
        x = R * np.cos(np.radians(angle))
        y = R * np.sin(np.radians(angle))
        index = 0
        for actor in actors:
            actor.position = (x, y, 0.0)
            angles[i][index][0] += spin_step
            angles[i][index][1] += spin_step
            actor.orientation = (angles[i][index][0], angles[i][index][1], angles[i][index][2])
            index += 1
            
    plotter.write_frame()

plotter.close()
print(f"Готово! Видео вращения сохранено в: {OUTPUT_GIF}")