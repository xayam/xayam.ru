"""
Аудио-движок: генерация звука из параметров.
Использует аддитивный синтез + FM + эффекты.
"""
import numpy as np
import sounddevice as sd
import threading
import time


class AudioEngine:
    def __init__(self, sample_rate: int = 44100, duration: float = 30.0):
        self.sr = sample_rate
        self.duration = duration
        self.playing = False
        self.thread = None
    
    def render(self, params: dict) -> np.ndarray:
        """
        Рендерит звуковой буфер из параметров маппера.
        Возвращает stereo-массив формы (samples, 2).
        """
        t = np.linspace(0, self.duration, int(self.sr * self.duration), endpoint=False)
        
        # === Базовый тон с вибрато ===
        vibrato = 1 + params['vibrato_depth'] * np.sin(2 * np.pi * 5 * t)
        fundamental = params['fundamental'] * vibrato
        
        # Аддитивный синтез: сумма гармоник
        signal = np.zeros_like(t)
        for freq, amp in params['harmonics']:
            signal += amp * np.sin(2 * np.pi * freq * t / params['fundamental'] * vibrato)
        
        # === FM-модуляция (Меркурий) ===
        fm_mod = params['fm_index'] * np.sin(2 * np.pi * params['fundamental'] * params['fm_ratio'] * t)
        signal *= (1 + fm_mod)
        
        # === AM-модуляция (Венера) ===
        am_mod = 1 - params['am_depth'] * (0.5 + 0.5 * np.sin(2 * np.pi * 3 * t))
        signal *= am_mod
        
        # === Темп-пульсация (Луна) ===
        beat_freq = params['tempo_bpm'] / 60
        envelope = 0.7 + 0.3 * np.sin(2 * np.pi * beat_freq * t)
        signal *= envelope
        
        # === Тоны аспектов ===
        for freq, amp, asp_type in params['aspect_tones']:
            tone = amp * np.sin(2 * np.pi * freq * t)
            # Квадраты — с быстрым тремоло (напряжение)
            if asp_type == 'square':
                tone *= 0.5 + 0.5 * np.sin(2 * np.pi * 7 * t)
            signal += tone
        
        # === Фильтр (Марс) — простой one-pole lowpass ===
        signal = self._apply_lowpass(signal, params['filter_cutoff'], params['filter_q'])
        
        # === Панорама (Юпитер) ===
        pan = params['pan']
        left_gain = np.sqrt((1 - pan) / 2)
        right_gain = np.sqrt((1 + pan) / 2)
        stereo = np.column_stack([signal * left_gain, signal * right_gain])
        
        # === Простая реверберация (Сатурн) — через feedback delay ===
        stereo = self._apply_reverb(stereo, params['reverb_size'], params['delay_time'])
        
        # === Нормализация ===
        peak = np.max(np.abs(stereo))
        if peak > 0:
            stereo = stereo / peak * 0.8
        
        return stereo
    
    def _apply_lowpass(self, signal: np.ndarray, cutoff: float, q: float) -> np.ndarray:
        """Простой IIR lowpass-фильтр."""
        rc = 1.0 / (2 * np.pi * cutoff)
        dt = 1.0 / self.sr
        alpha = dt / (rc + dt)
        out = np.zeros_like(signal)
        out[0] = signal[0]
        for i in range(1, len(signal)):
            out[i] = out[i-1] + alpha * (signal[i] - out[i-1])
        return out
    
    def _apply_reverb(self, stereo: np.ndarray, size: float, delay_time: float) -> np.ndarray:
        """Простая реверберация через несколько delay-линий."""
        out = stereo.copy()
        delays = [int(self.sr * delay_time * (i + 1) * 0.7) for i in range(3)]
        gains = [0.3 * size, 0.2 * size, 0.1 * size]
        for delay, gain in zip(delays, gains):
            delayed = np.zeros_like(stereo)
            delayed[delay:] = stereo[:-delay] * gain
            out += delayed
        return out
    
    def play(self, params: dict):
        """Воспроизводит звук в реальном времени."""
        stereo = self.render(params)
        self.playing = True
        def _play():
            sd.play(stereo, self.sr)
            sd.wait()
            self.playing = False
        self.thread = threading.Thread(target=_play, daemon=True)
        self.thread.start()
    
    def stop(self):
        if self.playing:
            sd.stop()
            self.playing = False
    
    def save_wav(self, params: dict, filename: str):
        """Сохраняет звук в WAV-файл."""
        import wave
        import struct
        stereo = self.render(params)
        # Конвертируем в 16-bit PCM
        pcm = (stereo * 32767).astype(np.int16)
        with wave.open(filename, 'w') as wf:
            wf.setnchannels(2)
            wf.setsampwidth(2)
            wf.setframerate(self.sr)
            wf.writeframes(pcm.tobytes())