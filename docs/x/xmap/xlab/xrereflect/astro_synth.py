"""
Астрологический синтезатор.
Запуск: python astro_synth.py
"""
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from ephemeris_engine import EphemerisEngine
from astro_mapper import AstroMapper
from audio_engine import AudioEngine


SIGNS = [
    'Овен', 'Телец', 'Близнецы', 'Рак', 'Лев', 'Дева',
    'Весы', 'Скорпион', 'Стрелец', 'Козерог', 'Водолей', 'Рыбы'
]


class AstroSynthApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Астрологический синтезатор')
        self.root.geometry('600x500')
        
        self.engine = EphemerisEngine()
        self.mapper = AstroMapper(base_freq=72.0)
        self.audio = AudioEngine(sample_rate=44100, duration=30.0)
        
        self._build_ui()
    
    def _build_ui(self):
        # === Блок даты/времени ===
        frame_dt = ttk.LabelFrame(self.root, text='Дата и время', padding=10)
        frame_dt.pack(fill='x', padx=10, pady=5)

        # В методе _build_ui, в блоке frame_dt:
        ttk.Label(frame_dt, text='Временная зона:').grid(row=2, column=2, sticky='w', padx=(20, 0))
        self.entry_tz = ttk.Entry(frame_dt, width=15)
        self.entry_tz.insert(0, 'UTC')
        self.entry_tz.grid(row=2, column=3, padx=5)

        # Пресеты городов
        ttk.Button(frame_dt, text='Москва', 
                command=lambda: self._set_city(55.7558, 37.6176, 'Europe/Moscow')).grid(row=3, column=0, pady=2)
        ttk.Button(frame_dt, text='Нью-Йорк', 
                command=lambda: self._set_city(40.7128, -74.0060, 'America/New_York')).grid(row=3, column=1, pady=2)
        ttk.Button(frame_dt, text='Байконур', 
                command=lambda: self._set_city(45.965, 63.305, 'Asia/Almaty')).grid(row=3, column=2, pady=2)
        
        ttk.Label(frame_dt, text='Дата (ГГГГ-ММ-ДД):').grid(row=0, column=0, sticky='w')
        self.entry_date = ttk.Entry(frame_dt, width=15)
        self.entry_date.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.entry_date.grid(row=0, column=1, padx=5)
        
        ttk.Label(frame_dt, text='Время (ЧЧ:ММ):').grid(row=1, column=0, sticky='w')
        self.entry_time = ttk.Entry(frame_dt, width=15)
        self.entry_time.insert(0, datetime.now().strftime('%H:%M'))
        self.entry_time.grid(row=1, column=1, padx=5)
        
        ttk.Label(frame_dt, text='Широта:').grid(row=0, column=2, sticky='w', padx=(20, 0))
        self.entry_lat = ttk.Entry(frame_dt, width=10)
        self.entry_lat.insert(0, '55.7558')  # Москва
        self.entry_lat.grid(row=0, column=3, padx=5)
        
        ttk.Label(frame_dt, text='Долгота:').grid(row=1, column=2, sticky='w', padx=(20, 0))
        self.entry_lon = ttk.Entry(frame_dt, width=10)
        self.entry_lon.insert(0, '37.6176')
        self.entry_lon.grid(row=1, column=3, padx=5)
        
        ttk.Button(frame_dt, text='Сейчас', command=self._set_now).grid(row=2, column=1, pady=5)
        
        # === Блок информации ===
        frame_info = ttk.LabelFrame(self.root, text='Небесная конфигурация', padding=10)
        frame_info.pack(fill='x', padx=10, pady=5)
        
        self.info_text = tk.Text(frame_info, height=10, width=65, state='disabled')
        self.info_text.pack()
        
        # === Кнопки управления ===
        frame_ctrl = ttk.Frame(self.root, padding=10)
        frame_ctrl.pack(fill='x', padx=10)
        
        ttk.Button(frame_ctrl, text='▶ Воспроизвести', command=self._play).pack(side='left', padx=5)
        ttk.Button(frame_ctrl, text='■ Стоп', command=self._stop).pack(side='left', padx=5)
        ttk.Button(frame_ctrl, text='💾 Сохранить WAV', command=self._save).pack(side='left', padx=5)
        
        # === Длительность ===
        ttk.Label(frame_ctrl, text='Длительность (сек):').pack(side='left', padx=(20, 0))
        self.entry_dur = ttk.Entry(frame_ctrl, width=5)
        self.entry_dur.insert(0, '30')
        self.entry_dur.pack(side='left', padx=5)

    def _set_city(self, lat, lon, tz):
        self.entry_lat.delete(0, tk.END)
        self.entry_lat.insert(0, str(lat))
        self.entry_lon.delete(0, tk.END)
        self.entry_lon.insert(0, str(lon))
        self.entry_tz.delete(0, tk.END)
        self.entry_tz.insert(0, tz)
    
    def _set_now(self):
        now = datetime.now()
        self.entry_date.delete(0, tk.END)
        self.entry_date.insert(0, now.strftime('%Y-%m-%d'))
        self.entry_time.delete(0, tk.END)
        self.entry_time.insert(0, now.strftime('%H:%M'))
    
    def _parse_datetime(self) -> datetime:
        date_str = self.entry_date.get()
        time_str = self.entry_time.get()
        return datetime.strptime(f'{date_str} {time_str}', '%Y-%m-%d %H:%M')
    
    def _compute_and_display(self):
        dt = self._parse_datetime()
        lat = float(self.entry_lat.get())
        lon = float(self.entry_lon.get())
        tz = self.entry_tz.get()
        
        astro = self.engine.compute(dt, lat, lon, tz_name=tz)
        params = self.mapper.map(astro)
        
        # Формируем текстовое описание
        lines = []
        lines.append(f'📅 {dt.strftime("%Y-%m-%d %H:%M")}  📍 {lat:.2f}, {lon:.2f}')
        lines.append('')
        lines.append(f'☀  Солнце: {astro["sun"]["longitude"]:.1f}° — {SIGNS[astro["sun"]["sign"]]}')
        lines.append(f'   Высота: {astro["sun"]["altitude"]:.1f}°')
        lines.append(f'🌙 Луна:   {astro["moon"]["longitude"]:.1f}° — {SIGNS[astro["moon"]["sign"]]}')
        lines.append(f'   Фаза:   {astro["moon"]["phase"]*100:.0f}%')
        lines.append('')
        lines.append('🪐 Планеты:')
        for name, data in astro['planets'].items():
            retro = ' ℞' if data['retrograde'] else ''
            lines.append(f'   {name.capitalize():8s} {data["longitude"]:6.1f}° {SIGNS[data["sign"]]}{retro}')
        lines.append('')
        lines.append(f'🎵 Звук:')
        lines.append(f'   Фундаментальная: {params["fundamental"]:.2f} Гц')
        lines.append(f'   Темп: {params["tempo_bpm"]:.1f} BPM')
        lines.append(f'   Фильтр: {params["filter_cutoff"]:.0f} Гц (Q={params["filter_q"]:.1f})')
        lines.append(f'   FM-индекс: {params["fm_index"]:.2f}')
        lines.append(f'   Панорама: {params["pan"]:.2f}')
        lines.append(f'   Реверберация: {params["reverb_size"]:.2f}')
        lines.append(f'   Аспектов: {len(astro["aspects"])}')
        
        self.info_text.config(state='normal')
        self.info_text.delete('1.0', tk.END)
        self.info_text.insert(tk.END, '\n'.join(lines))
        self.info_text.config(state='disabled')
        
        return params
    
    def _play(self):
        # try:
        params = self._compute_and_display()
        self.audio.duration = float(self.entry_dur.get())
        self.audio.play(params)
        # except Exception as e:
        #     pass
            # self._show_error(str(e))
    
    def _stop(self):
        self.audio.stop()
    
    def _save(self):
        try:
            params = self._compute_and_display()
            self.audio.duration = float(self.entry_dur.get())
            dt = self._parse_datetime()
            filename = f'astro_{dt.strftime("%Y%m%d_%H%M")}.wav'
            self.audio.save_wav(params, filename)
            self._show_info(f'Сохранено: {filename}')
        except Exception as e:
            self._show_error(str(e))
    
    def _show_error(self, msg):
        from tkinter import messagebox
        messagebox.showerror('Ошибка', msg)
    
    def _show_info(self, msg):
        from tkinter import messagebox
        messagebox.showinfo('Информация', msg)


if __name__ == '__main__':
    root = tk.Tk()
    app = AstroSynthApp(root)
    root.mainloop()