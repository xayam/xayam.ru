"""
Модуль вычисления положений небесных тел.
Исправленная версия с поддержкой исторических дат.
"""
from pathlib import Path
from skyfield.api import load, wgs84
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
import numpy as np

# Диапазон, корректно покрываемый de421.bsp
EPHEMERIS_START = datetime(1899, 1, 1, tzinfo=timezone.utc)
EPHEMERIS_END = datetime(2053, 12, 31, tzinfo=timezone.utc)


class EphemerisEngine:
    def __init__(self, ephemeris_file: str = 'de421.bsp'):
        self.ts = load.timescale()
        load.directory = str(Path(__file__).resolve().parent)
        self.ephemeris = load(ephemeris_file)
        self.earth = self.ephemeris['earth']
    
    def compute(self, dt: datetime, lat: float, lon: float, 
                tz_name: str = 'UTC') -> dict:
        """
        Вычисляет положения всех небесных тел.
        
        Параметры:
            dt: наивный datetime (локальное время) или aware datetime
            lat, lon: координаты наблюдателя
            tz_name: имя временной зоны (например 'Europe/Moscow'),
                     используется только если dt наивный
        """
        # === Нормализация datetime ===
        dt_aware = self._normalize_datetime(dt, tz_name)
        self._check_range(dt_aware)
        
        # === Перевод в skyfield Time ===
        # Самый надёжный способ — через ts.utc(), минуя все проблемы с tz
        t = self.ts.utc(
            dt_aware.year, dt_aware.month, dt_aware.day,
            dt_aware.hour, dt_aware.minute, dt_aware.second
        )
        
        observer = self.earth + wgs84.latlon(lat, lon)
        
        # === Солнце ===
        sun_obs = observer.at(t).observe(self.ephemeris['sun'])
        sun_lon = self._ecliptic_longitude(sun_obs)
        sun_alt = sun_obs.apparent().altaz()[0].degrees
        
        # === Луна ===
        moon_obs = observer.at(t).observe(self.ephemeris['moon'])
        moon_lon = self._ecliptic_longitude(moon_obs)
        moon_phase = self._moon_phase(t)
        
        # === Планеты ===
        planet_names = {'mercury': 1, 'venus': 2, 'mars': 4, 'jupiter': 5, 'saturn': 6}
        planets = {}
        for name in planet_names:
            p_obs = observer.at(t).observe(self.ephemeris[planet_names[name]])
            p_lon = self._ecliptic_longitude(p_obs)
            retro = self._is_retrograde_safe(planet_names[name], t)
            planets[name] = {
                'longitude': p_lon,
                'retrograde': retro,
                'sign': int(p_lon // 30)
            }
        
        # === Аспекты ===
        all_bodies = {
            'sun': sun_lon, 
            'moon': moon_lon, 
            **{k: v['longitude'] for k, v in planets.items()}
        }
        aspects = self._compute_aspects(all_bodies)
        
        return {
            'datetime': dt_aware.isoformat(),
            'location': {'lat': lat, 'lon': lon},
            'sun': {
                'longitude': sun_lon,
                'altitude': sun_alt,
                'sign': int(sun_lon // 30)
            },
            'moon': {
                'longitude': moon_lon,
                'phase': moon_phase,
                'sign': int(moon_lon // 30)
            },
            'planets': planets,
            'aspects': aspects
        }
    
    def _normalize_datetime(self, dt: datetime, tz_name: str) -> datetime:
        """Приводит datetime к aware UTC."""
        if dt.tzinfo is None:
            # Наивный datetime — интерпретируем в заданной временной зоне
            try:
                local_tz = ZoneInfo(tz_name)
            except Exception:
                local_tz = timezone.utc
            dt = dt.replace(tzinfo=local_tz)
        # Переводим в UTC для единообразия
        return dt.astimezone(timezone.utc)
    
    def _check_range(self, dt: datetime):
        """Проверяет, что дата в пределах эфемерид."""
        if dt < EPHEMERIS_START or dt > EPHEMERIS_END:
            raise ValueError(
                f"Дата {dt.year} вне диапазона эфемерид "
                f"({EPHEMERIS_START.year}–{EPHEMERIS_END.year}). "
                f"Используйте более точный файл (de440.bsp) для старых дат."
            )
    
    def _ecliptic_longitude(self, astrometric) -> float:
        """Преобразует RA/Dec в эклиптическую долготу (0-360°)."""
        ra, dec, _ = astrometric.radec()
        ra_rad = np.radians(ra.hours * 15)
        dec_rad = np.radians(dec.degrees)
        eps = np.radians(23.43928)  # наклон эклиптики
        
        sin_lon = (np.sin(ra_rad) * np.cos(eps) + 
                   np.tan(dec_rad) * np.sin(eps))
        cos_lon = np.cos(ra_rad)
        
        lon_rad = np.arctan2(sin_lon, cos_lon)
        return float(np.degrees(lon_rad) % 360)
    
    def _moon_phase(self, t) -> float:
        """Фаза Луны 0..1 (0 = новолуние, 0.5 = полнолуние)."""
        sun = self.ephemeris['sun']
        moon = self.ephemeris['moon']
        sun_lon = self._ecliptic_longitude(self.earth.at(t).observe(sun))
        moon_lon = self._ecliptic_longitude(self.earth.at(t).observe(moon))
        diff = (moon_lon - sun_lon) % 360
        return diff / 360.0
    
    def _is_retrograde_safe(self, planet_name: str, t) -> bool:
        """
        Безопасное определение ретроградного движения.
        Использует малый шаг (1 час) и проверяет границы эфемерид.
        """
        planet = self.ephemeris[planet_name]
        
        # Проверяем, что t + 1 час не выходит за границы
        t_plus = t + 1/24  # 1 час в сутках
        try:
            pos1 = self.earth.at(t).observe(planet)
            pos2 = self.earth.at(t_plus).observe(planet)
        except (ValueError, KeyError):
            # Если вышли за границы — используем меньший шаг
            t_plus = t + 1/24/60  # 1 минута
            pos1 = self.earth.at(t).observe(planet)
            pos2 = self.earth.at(t_plus).observe(planet)
        
        lon1 = self._ecliptic_longitude(pos1)
        lon2 = self._ecliptic_longitude(pos2)
        diff = (lon2 - lon1) % 360
        # Ретроградное = движение "назад" по зодиаку
        return diff > 180
    
    def _compute_aspects(self, bodies: dict, orb: float = 8.0) -> list:
        """Находит аспекты между всеми парами тел."""
        aspect_angles = {
            'conjunction': 0,
            'sextile': 60,
            'square': 90,
            'trine': 120,
            'opposition': 180
        }
        aspects = []
        names = list(bodies.keys())
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                diff = abs(bodies[names[i]] - bodies[names[j]])
                diff = min(diff, 360 - diff)
                for asp_name, asp_angle in aspect_angles.items():
                    if abs(diff - asp_angle) <= orb:
                        aspects.append((names[i], names[j], diff, asp_name))
        return aspects