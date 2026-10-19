import trimesh
import pyvista as pv
import numpy as np

from pathlib import Path

script_dir = str(Path(__file__).resolve().parent)

# --- НАСТРОЙКИ ---
GLB_FILES = [
    f'{script_dir}/v5.d6.chess-classic.black-white.glb', 
    f'{script_dir}/v5.d6.chess-classic.white-black.glb', 
    # f'{script_dir}/v5.d12.chess-adds.black-white.glb', 
    # f'{script_dir}/v5.d12.chess-adds.white-black.glb', 
    # f'{script_dir}/v5.d12.chess-classic.glb'
    ]
OUTPUT_GIF = f'{script_dir}/presentation_colored.gif'

RESOLUTION = (800, 800)
TARGET_SIZE = 1.0
ORBIT_RADIUS = 2.2
NUM_FRAMES = 60
FPS = 30
SPIN_MULTIPLIER = 2

# --- 1. ЗАГРУЗКА С ПРАВИЛЬНЫМ ИЗВЛЕЧЕНИЕМ МАТЕРИАЛОВ ---
model_groups = []  # список групп акторов (по одной группе на GLB файл)

print("Загрузка GLB файлов...")
for path in GLB_FILES:
    scene = trimesh.load(path, force='scene')
    
    group_actors = []  # все акторы этой модели (будут вращаться вместе)
    
    # Правильно обходим геометрии сцены
    for geom_name, geom in scene.geometry.items():
        # Нормализация и центрирование
        geom.apply_scale(TARGET_SIZE / max(geom.extents))
        geom.apply_translation(-geom.centroid)
        
        # Конвертация в PyVista
        faces = np.hstack([[3, *f] for f in geom.faces]).astype(np.int64)
        pv_mesh = pv.PolyData(
            np.asarray(geom.vertices, dtype=float),
            faces
        )
        
        # UV-координаты
        if hasattr(geom.visual, 'uv') and geom.visual.uv is not None:
            pv_mesh.active_t_coords = np.asarray(geom.visual.uv, dtype=float)
        
        # ПРАВИЛЬНОЕ извлечение материала
        material = getattr(geom.visual, 'material', None)
        
        # Создаём актор
        if material is not None and hasattr(material, 'baseColorTexture'):
            pil_img = material.baseColorTexture
            if pil_img is not None:
                texture = pv.Texture(np.asarray(pil_img))
                actor = pv_mesh  # временно, потом добавим в plotter
                group_actors.append((pv_mesh, texture, geom_name))
                continue
        
        # Fallback: vertex_colors или face_colors
        colors, loc = None, None
        for attr in ('vertex_colors', 'face_colors'):
            c = getattr(geom.visual, attr, None)
            if c is None:
                continue
            c = np.asarray(c)
            if c.ndim == 2 and c.shape[0] > 0 and c.shape[1] >= 3:
                c = np.clip(c, 0, 255).astype(np.uint8)[:, :3]
                if c.std() > 3 or c.mean() < 245:
                    colors, loc = c, ('point' if attr == 'vertex_colors' else 'cell')
                    break
        
        if colors is not None:
            (pv_mesh.point_data if loc == 'point' else pv_mesh.cell_data)['colors'] = colors
            group_actors.append((pv_mesh, 'colors', geom_name))
        else:
            group_actors.append((pv_mesh, 'gray', geom_name))
    
    model_groups.append(group_actors)
    print(f"  {Path(path).name}: {len(group_actors)} геометрий загружено")

# --- 2. СЦЕНА ---
plotter = pv.Plotter(off_screen=True, window_size=RESOLUTION)
plotter.set_background('white')
plotter.enable_lightkit()

# Добавляем все акторы, группируем по моделям
all_actors = []  # плоский список всех акторов
model_actor_groups = []  # список списков акторов (по моделям)

for group in model_groups:
    group_actor_list = []
    for pv_mesh, tex_or_colors, geom_name in group:
        if isinstance(tex_or_colors, pv.Texture):
            actor = plotter.add_mesh(
                pv_mesh,
                texture=tex_or_colors,
                smooth_shading=True,
                specular=0.4
            )
        elif tex_or_colors == 'colors':
            actor = plotter.add_mesh(
                pv_mesh,
                scalars='colors',
                rgb=True,
                smooth_shading=True,
                specular=0.4
            )
        else:  # 'gray'
            actor = plotter.add_mesh(
                pv_mesh,
                color='gray',
                smooth_shading=True,
                specular=0.4
            )
        
        all_actors.append(actor)
        group_actor_list.append(actor)
    
    model_actor_groups.append(group_actor_list)

# --- 3. КАМЕРА ---
def set_frame(t):
    orbit = 2 * np.pi * t
    spin = 2 * np.pi * t * SPIN_MULTIPLIER
    
    for i, group in enumerate(model_actor_groups):
        phase = 2 * np.pi * i / len(model_actor_groups)
        x = ORBIT_RADIUS * np.cos(orbit + phase)
        y = ORBIT_RADIUS * np.sin(orbit + phase)
        
        c, s = np.cos(spin), np.sin(spin)
        R = np.array([[c, -s, 0, 0], [s, c, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        T = np.eye(4)
        T[0:3, 3] = [x, y, 0]
        transform = T @ R
        
        # Применяем ОДИНАКОВЫЙ трансформ ко всем акторам группы
        for actor in group:
            actor.user_matrix = transform

set_frame(0)
plotter.reset_camera()
plotter.camera.zoom(0.85)

# --- 4. РЕНДЕР ---
print("Рендеринг GIF...")
plotter.open_gif(OUTPUT_GIF, fps=FPS)

for frame in range(NUM_FRAMES):
    set_frame(frame / NUM_FRAMES)
    plotter.write_frame()

plotter.close()
print(f"Готово! {OUTPUT_GIF}")