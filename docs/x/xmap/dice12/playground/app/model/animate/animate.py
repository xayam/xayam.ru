import pyvista as pv

from pathlib import Path

script_dir = str(Path(__file__).resolve().parent)

# 1. Настройки сцены
MODEL_PATH = f'{script_dir}/v5.d6.chess-classic.black-white.glb'
OUTPUT_VIDEO = f'{script_dir}/v5.d6-d12-presentation.gif'
BG_COLOR = "#2a2a2a" # Темно-серый нейтральный фон
# 2. Загрузка модели
mesh = pv.read(MODEL_PATH)
mesh = mesh.get_block(0)
# 3. Инициализируем скрытый плоттер (без открытия окна во время генерации)
plotter = pv.Plotter(off_screen=True)
plotter.background_color = BG_COLOR
# Устанавливаем цвета блоков модели
for m in range(mesh.n_blocks):
    actor = plotter.add_mesh(
        mesh=mesh.get_block(m), 
        color=mesh.get_block(m).get_block(0).get_block(0). \
            field_data['BaseColorMultiplier'][0])
# Центрируем камеру на объекте
plotter.camera_position = 'iso'
plotter.reset_camera()
# 4. Рендеринг анимации вращения
plotter.open_movie(OUTPUT_VIDEO, framerate=30) 
# Сделаем полный оборот на 360 градусов за 150 кадров (5 секунд при 30 fps)
frames = 150
for _ in range(frames):
    # Вращаем саму модель вокруг вертикальной оси Z
    mesh.rotate_z(360 / frames, inplace=True)
    # Записываем текущий кадр в видео
    plotter.write_frame()
# Финализируем и сохраняем файл
plotter.close()
print(f"Готово! Видео вращения сохранено в: {OUTPUT_VIDEO}")
