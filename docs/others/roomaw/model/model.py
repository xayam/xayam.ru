import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString, Polygon
import pyroomacoustics as pra
import pyaudio

# ========================================
# 1. Параметры
# ========================================
fs = 16000                    # Частота дискретизации
duration = 5                  # Длительность сигнала (сек)
room_dim = [5.4, 5.4]         # Размеры комнаты (м)
mic_pos = [2.7, 2.7]          # Микрофон в центре
speaker_radius = 0.135        # Радиус круга динамиков
n_speakers = 8                # Число динамиков

# Колонны: центр и радиус
columns = [
    {'center': (7 * 0.27, 7 * 0.27), 'radius': 0.135},
    {'center': (7 * 0.27, 13 * 0.27), 'radius': 0.135},
    {'center': (13 * 0.27, 13 * 0.27), 'radius': 0.135},
    {'center': (13 * 0.27, 7 * 0.27), 'radius': 0.135}
]

# Создаём Shapely-объекты для колонн
column_objects = [Point(col['center']).buffer(col['radius']) for col in columns]
obstacles = column_objects  # можно объединить: unary_union(column_objects), но для проверки проще по отдельности

# Функция: проверка, пересекает ли луч какие-либо колонны
def is_visible(pos1, pos2, obstacles):
    line = LineString([pos1, pos2])
    for obs in obstacles:
        if line.intersects(obs):
            return False
    return True

# ========================================
# 2. Генерация позиций динамиков
# ========================================
# angles = np.linspace(0, 2*np.pi, n_speakers, endpoint=False)
speakers = [
    [4 * 0.27, 4 * 0.27],
    [4 * 0.27, 10 * 0.27],
    [4 * 0.27, 16 * 0.27],
    [10 * 0.27, 16 * 0.27],
    [16 * 0.27, 16 * 0.27],
    [16 * 0.27, 10 * 0.27],
    [16 * 0.27, 4 * 0.27],
    [10 * 0.27, 4 * 0.27]
]
# for angle in angles:
#     x = speaker_radius * np.cos(angle)
#     y = speaker_radius * np.sin(angle)
#     speakers.append([x, y])
#     print(x, y)

# ========================================
# 3. Создание комнаты в pyroomacoustics
# ========================================
room = pra.ShoeBox(
    room_dim,
    fs=fs,
    max_order=10,           # число отражений (2 — достаточно для теста)
    absorption=0.1,        # поглощение стен (низкое — много реверберации)
    sigma2_awgn=None       # без шума
)

# Добавляем микрофон
mic_array = pra.MicrophoneArray(np.array([[mic_pos[0]], [mic_pos[1]]]), room.fs)
room.add_microphone_array(mic_array)

# ========================================
# 4. Подготовка сигналов и добавление источников
# ========================================
# Генерируем тестовый сигнал (импульс или синус)
t_signal = np.arange(0, duration, 1/fs)
freqs = [54, 108, 162, 216, 270, 324, 378, 432]
source_signal = [np.sin(2 * np.pi * f * t_signal) for f in freqs]
# source_signal = np.zeros_like(t_signal); source_signal[0] = 1  # импульс

# Добавляем только те динамики, которые "видны" (прямой путь не перекрыт)
for i, sp_pos in enumerate(speakers):
#     if is_visible(sp_pos, mic_pos, column_objects):
#     print(f"Динамик {i} в позиции {sp_pos} — ВИДИМ")
    room.add_source(sp_pos, signal=source_signal[i].copy(), delay=0.0)
#     else:
#         print(f"Динамик {i} в позиции {sp_pos} — ЗАБЛОКИРОВАН")

# ========================================
# 5. Запуск моделирования
# ========================================
room.simulate()

# Получаем сигнал на микрофоне
recorded_signal = room.mic_array.signals[0, :len(t_signal)]  # обрезаем до нужной длины

# ========================================
# 6. Визуализация
# ========================================
plt.figure(figsize=(10, 10))

# Рисуем комнату
plt.plot([0, room_dim[0], room_dim[0], 0, 0],
         [0, 0, room_dim[1], room_dim[1], 0], 'k-', linewidth=2)

# Рисуем колонны
for col in columns:
    circle = plt.Circle(col['center'], col['radius'], color='red', alpha=0.5, label='Колонна')
    plt.gca().add_patch(circle)

# Рисуем динамики и пути
for i, sp_pos in enumerate(speakers):
    visible = is_visible(sp_pos, mic_pos, column_objects)
    color = 'go' if visible else 'ro'
    plt.plot(sp_pos[0], sp_pos[1], color)
    style = 'g-' if visible else 'r--'
    plt.plot([sp_pos[0], mic_pos[0]], [sp_pos[1], mic_pos[1]], style, alpha=0.5)

# Микрофон
plt.plot(mic_pos[0], mic_pos[1], 'b^', markersize=12, label='Микрофон')

plt.axis('equal')
plt.grid(True)
plt.title("Акустическая комната: динамики, колонны, микрофон")
plt.xlabel("X (м)")
plt.ylabel("Y (м)")
plt.legend()
plt.tight_layout()
plt.show()

# ========================================
# 7. Построение сигнала на микрофоне
# ========================================
plt.figure(figsize=(10, 4))
plt.plot(t_signal, recorded_signal)
plt.title("Сигнал на микрофоне (с учётом блокировки колоннами)")
plt.xlabel("Время (с)")
plt.ylabel("Амплитуда")
plt.grid(True)
plt.tight_layout()
plt.show()


def play_audio(signal, fs):
    """
    Проигрывает аудиосигнал через систему.

    Параметры:
    - signal: массив NumPy (одноканальный)
    - fs: частота дискретизации
    """
    # Нормализация сигнала до диапазона [-1, 1], если нужно
    signal = signal / np.max(np.abs(signal))  # нормализация
    signal = (signal * 32767).astype(np.int16)  # преобразование в 16-битный формат

    # Инициализация PyAudio
    p = pyaudio.PyAudio()

    # Открытие потока
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,  # моно
        rate=fs,
        output=True
    )

    # Проигрывание
    stream.write(signal.tobytes())

    # Закрытие
    stream.stop_stream()
    stream.close()
    p.terminate()

play_audio(recorded_signal, fs)