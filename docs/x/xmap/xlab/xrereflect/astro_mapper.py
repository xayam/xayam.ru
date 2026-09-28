"""
Маппинг астрономических данных на звуковые параметры.
Все правила собраны здесь — их легко менять и расширять.
"""
import numpy as np


# Соответствие знаков зодиака тональностям (по Кеплеру/традиции)
# 0 = C, 1 = C#, ... 11 = B
ZODIAC_TO_SCALE = {
    0:  [0, 4, 7],        # Овен:     C мажор
    1:  [2, 5, 9],        # Телец:    D минор
    2:  [4, 8, 11],       # Близнецы: E мажор
    3:  [5, 9, 0],        # Рак:      F минор
    4:  [7, 11, 2],       # Лев:      G мажор
    5:  [9, 0, 4],        # Дева:     A минор
    6:  [11, 3, 6],       # Весы:     B мажор
    7:  [0, 3, 7],        # Скорпион: C минор
    8:  [2, 6, 9],        # Стрелец:  D мажор
    9:  [4, 7, 11],       # Козерог:  E минор
    10: [5, 9, 0],        # Водолей:  F мажор
    11: [7, 10, 2],       # Рыбы:     G минор
}

# Интервалы аспектов в полутонах
ASPECT_INTERVALS = {
    'conjunction': 0,
    'sextile':     3,     # малая терция
    'square':      6,     # тритон (диссонанс)
    'trine':       4,     # большая терция
    'opposition':  12,    # октава
}


class AstroMapper:
    def __init__(self, base_freq: float = 220.0):
        self.base_freq = base_freq  # A3 = 220 Гц
    
    def map(self, astro_data: dict) -> dict:
        """
        Превращает астрономические данные в звуковые параметры.
        
        Возвращает:
        {
            'fundamental': float,      # базовая частота в Гц
            'scale': list,             # ноты лада в полутонах
            'tempo_bpm': float,        # темп
            'harmonics': list,         # активные гармоники [(freq, amp), ...]
            'filter_cutoff': float,    # частота среза фильтра
            'filter_q': float,         # резонанс фильтра
            'fm_index': float,         # индекс FM-модуляции
            'fm_ratio': float,         # отношение частот модулятора
            'reverb_size': float,      # размер реверберации 0..1
            'delay_time': float,       # время задержки в секундах
            'pan': float,              # панорама -1..1
            'aspect_tones': list,      # дополнительные тона от аспектов
        }
        """
        sun = astro_data['sun']
        moon = astro_data['moon']
        planets = astro_data['planets']
        aspects = astro_data['aspects']
        
        # === СЛОЙ 1: СОЛНЦЕ ===
        # Тональность от знака
        scale = ZODIAC_TO_SCALE[sun['sign']]
        
        # Фундаментальная частота: долгота Солнца → частота
        # 360° логарифмически маппятся на 2 октавы от базовой частоты
        freq_ratio = 2 ** (sun['longitude'] / 360 * 2)  # 0..4x
        fundamental = self.base_freq * freq_ratio
        
        # Громкость от высоты Солнца (день громче ночи)
        # altitude от -90 до +90, нормализуем в 0..1
        sun_amp = max(0.1, (sun['altitude'] + 90) / 180)
        
        # === СЛОЙ 2: ЛУНА ===
        # Темп: фаза Луны 0..1 → BPM 40..180
        tempo_bpm = 40 + moon['phase'] * 140
        
        # Активная гармоника: знак Луны → номер гармоники (1..12)
        active_harmonic = moon['sign'] + 1
        
        # Глубина вибрато: близость к узлам (упрощённо — от фазы)
        vibrato_depth = 0.02 + moon['phase'] * 0.05  # 2..7%
        
        # === СЛОЙ 3: ПЛАНЕТЫ ===
        # Меркурий → FM-модуляция
        mercury = planets['mercury']
        fm_index = (mercury['longitude'] % 360) / 360 * 5  # 0..5
        if mercury['retrograde']:
            fm_index *= -1  # инверсия
        
        # Венера → AM-модуляция (глубина)
        venus = planets['venus']
        am_depth = (venus['longitude'] % 360) / 360 * 0.8  # 0..0.8
        
        # Марс → фильтр
        mars = planets['mars']
        # Логарифмический маппинг долготы на частоту среза 200..8000 Гц
        filter_cutoff = 200 * (40 ** (mars['longitude'] / 360))
        
        # Юпитер → панорама
        jupiter = planets['jupiter']
        pan = (jupiter['longitude'] % 360) / 360 * 2 - 1  # -1..1
        
        # Сатурн → реверберация и задержка
        saturn = planets['saturn']
        reverb_size = (saturn['longitude'] % 360) / 360
        delay_time = 0.1 + reverb_size * 0.8  # 0.1..0.9 сек
        
        # === СЛОЙ 4: ГАРМОНИКИ ===
        # Строим спектр: фундаментал + активная гармоника Луны + аспекты
        harmonics = [(fundamental, sun_amp)]
        harmonics.append((fundamental * active_harmonic, sun_amp * 0.3))
        
        # === СЛОЙ 5: АСПЕКТЫ → дополнительные тона ===
        aspect_tones = []
        for p1, p2, angle, asp_type in aspects:
            interval = ASPECT_INTERVALS[asp_type]
            # Преобразуем интервал в частоту
            freq = fundamental * (2 ** (interval / 12))
            # Громкость зависит от точности аспекта (орбиса)
            amp = sun_amp * 0.2
            aspect_tones.append((freq, amp, asp_type))
        
        # Фильтр Q: больше при напряжённых аспектах (квадраты)
        square_count = sum(1 for *_, a in aspects if a == 'square')
        filter_q = 1.0 + square_count * 2.0
        
        return {
            'fundamental': fundamental,
            'scale': scale,
            'tempo_bpm': tempo_bpm,
            'harmonics': harmonics,
            'filter_cutoff': filter_cutoff,
            'filter_q': filter_q,
            'fm_index': fm_index,
            'fm_ratio': 1.5,  # отношение частоты модулятора к несущей
            'am_depth': am_depth,
            'reverb_size': reverb_size,
            'delay_time': delay_time,
            'pan': pan,
            'vibrato_depth': vibrato_depth,
            'aspect_tones': aspect_tones,
        }