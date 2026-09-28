"""
Модуль вычисления положений небесных тел.
Возвращает структуру данных, которую дальше маппит на звук.
"""
from skyfield.api import load, wgs84
from skyfield.constants import DAY_S
from datetime import datetime
import numpy as np


class EphemerisEngine:
    def __init__(self):
        self.ts = load.timescale()
        self.ephemeris = load('de421.bsp')
        self.earth = self.ephemeris['earth']
    
    def compute(self, dt: datetime, lat: float, lon: float) -> dict:
        """
        Вычисляет положения всех небесных тел для заданного момента.
        
        Возвращает:
        {
            'sun': {'longitude': float, 'altitude': float, 'sign': int},
            'moon': {'longitude': float, 'phase': float, 'sign': int},
            'planets': {
                'mercury': {'longitude': float, 'retrograde': bool, 'sign': int},
                'venus':   {...},
                'mars':    {...},
                'jupiter': {...},
                'saturn':  {...}
            },
            'aspects': [(planet1, planet2, angle_degrees, aspect_type), ...]
        }
        """
        print(dt.tzinfo)
        t = self.ts.from_datetime(dt.astimezone())
        observer = self.earth + wgs84.latlon(lat, lon)
        
        # Солнце
        sun_obs = observer.at(t).observe(self.ephemeris['sun'])
        sun_lon = self._ecliptic_longitude(sun_obs)
        sun_alt = sun_obs.apparent().altaz()[0].degrees
        
        # Луна
        moon_obs = observer.at(t).observe(self.ephemeris['moon'])
        moon_lon = self._ecliptic_longitude(moon_obs)
        moon_phase = self._moon_phase(t)
        
        # Планеты
        # planet_names = ['mercury', 'venus', 'mars', 'jupiter', 'saturn']
        planet_names = {'mercury': 1, 'venus': 2, 'mars': 4, 'jupiter': 5, 'saturn': 6}
        planets = {}
        for name in planet_names:
            p_obs = observer.at(t).observe(self.ephemeris[planet_names[name]])
            p_lon = self._ecliptic_longitude(p_obs)
            retro = self._is_retrograde(planet_names[name], t)
            planets[name] = {
                'longitude': p_lon,
                'retrograde': retro,
                'sign': int(p_lon // 30)
            }
        
        # Аспекты (угловые расстояния между планетами)
        all_bodies = {
            'sun': sun_lon, 'moon': moon_lon, **{k: v['longitude'] for k, v in planets.items()}
        }
        aspects = self._compute_aspects(all_bodies)
        
        return {
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
    
    def _ecliptic_longitude(self, astrometric) -> float:
        """Преобразует RA/Dec в эклиптическую долготу (0-360°)."""
        ra, dec, _ = astrometric.radec()
        # Упрощённое преобразование (для музыкальных целей достаточно)
        lat_ecl = np.arcsin(
            np.sin(np.radians(dec.degrees)) * np.cos(23.44) -
            np.cos(np.radians(dec.degrees)) * np.sin(23.44) * np.sin(np.radians(ra.hours * 15))
        )
        lon_ecl = np.arctan2(
            np.sin(np.radians(ra.hours * 15)) * np.cos(23.44) +
            np.tan(np.radians(dec.degrees)) * np.sin(23.44),
            np.cos(np.radians(ra.hours * 15))
        )
        lon_deg = np.degrees(lon_ecl) % 360
        return float(lon_deg)
    
    def _moon_phase(self, t) -> float:
        """Фаза Луны 0..1 (0 = новолуние, 0.5 = полнолуние)."""
        sun = self.ephemeris['sun']
        moon = self.ephemeris['moon']
        sun_lon = self._ecliptic_longitude(self.earth.at(t).observe(sun))
        moon_lon = self._ecliptic_longitude(self.earth.at(t).observe(moon))
        diff = (moon_lon - sun_lon) % 360
        # 0° = новолуние, 180° = полнолуние
        # Возвращаем 0..1 где 0.5 = полнолуние
        return diff / 360.0
    
    def _is_retrograde(self, planet_name: str, t) -> bool:
        """Определяет ретроградное движение по сравнению позиций через 1 день."""
        planet = self.ephemeris[planet_name]
        pos1 = self.earth.at(t).observe(planet)
        t2 = t + 1  # +1 день
        pos2 = self.earth.at(t2).observe(planet)
        lon1 = self._ecliptic_longitude(pos1)
        lon2 = self._ecliptic_longitude(pos2)
        diff = (lon2 - lon1) % 360
        return diff > 180  # если "движется назад" по зодиаку
    
    def _compute_aspects(self, bodies: dict, orb: float = 8.0) -> list:
        """
        Находит аспекты между всеми парами тел.
        orb — допуск в градусах (орбис).
        """
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