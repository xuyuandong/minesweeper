# -*- coding: utf-8 -*-
"""
音效管理器
处理游戏中的音效播放
"""

import pygame
import os
from typing import Dict, Optional


class SoundManager:
    """音效管理器类"""

    def __init__(self):
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.enabled = True
        self.volume = 0.5

        # 初始化音效系统
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

        # 尝试加载音效文件
        self._load_sounds()

    def _load_sounds(self):
        """加载音效文件"""
        # 音效文件路径
        sound_files = {
            'click': 'assets/sounds/click.wav',
            'flag': 'assets/sounds/flag.wav',
            'mine': 'assets/sounds/mine.wav',
            'win': 'assets/sounds/win.wav',
            'game_over': 'assets/sounds/game_over.wav'
        }

        for name, path in sound_files.items():
            if os.path.exists(path):
                try:
                    self.sounds[name] = pygame.mixer.Sound(path)
                    self.sounds[name].set_volume(self.volume)
                except Exception as e:
                    print(f"无法加载音效 {name}: {e}")
            else:
                print(f"音效文件不存在: {path}")

    def play_sound(self, sound_name: str):
        """播放音效"""
        if not self.enabled or sound_name not in self.sounds:
            return

        try:
            self.sounds[sound_name].play()
        except Exception as e:
            print(f"播放音效失败 {sound_name}: {e}")

    def set_volume(self, volume: float):
        """设置音量"""
        self.volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.volume)

    def toggle_sound(self):
        """切换音效开关"""
        self.enabled = not self.enabled

    def is_enabled(self) -> bool:
        """检查音效是否启用"""
        return self.enabled

    def get_volume(self) -> float:
        """获取当前音量"""
        return self.volume

    def create_default_sounds(self):
        """创建默认的简单音效"""
        if not self.sounds:
            print("创建默认音效...")

            # 创建简单的点击音效
            self._create_click_sound()
            self._create_flag_sound()
            self._create_mine_sound()
            self._create_win_sound()
            self._create_game_over_sound()

    def _create_click_sound(self):
        """创建点击音效"""
        try:
            # 创建一个简单的正弦波作为点击音效
            sample_rate = 22050
            duration = 0.1
            frequency = 800

            frames = int(duration * sample_rate)
            arr = []
            for i in range(frames):
                wave = 4096 * (frequency / sample_rate * i)
                wave = int(wave % (2 * 4096) - 4096)
                arr.append([wave, wave])

            sound = pygame.sndarray.make_sound(arr)
            sound.set_volume(self.volume)
            self.sounds['click'] = sound
        except:
            pass

    def _create_flag_sound(self):
        """创建旗子音效"""
        try:
            sample_rate = 22050
            duration = 0.15
            frequency = 1200

            frames = int(duration * sample_rate)
            arr = []
            for i in range(frames):
                wave = 4096 * (frequency / sample_rate * i)
                wave = int(wave % (2 * 4096) - 4096)
                arr.append([wave, wave])

            sound = pygame.sndarray.make_sound(arr)
            sound.set_volume(self.volume)
            self.sounds['flag'] = sound
        except:
            pass

    def _create_mine_sound(self):
        """创建地雷音效"""
        try:
            sample_rate = 22050
            duration = 0.3
            frequency = 200

            frames = int(duration * sample_rate)
            arr = []
            for i in range(frames):
                wave = 4096 * (frequency / sample_rate * i)
                wave = int(wave % (2 * 4096) - 4096)
                arr.append([wave, wave])

            sound = pygame.sndarray.make_sound(arr)
            sound.set_volume(self.volume)
            self.sounds['mine'] = sound
        except:
            pass

    def _create_win_sound(self):
        """创建胜利音效"""
        try:
            sample_rate = 22050
            duration = 0.5
            frequency = 1600

            frames = int(duration * sample_rate)
            arr = []
            for i in range(frames):
                wave = 4096 * (frequency / sample_rate * i)
                wave = int(wave % (2 * 4096) - 4096)
                arr.append([wave, wave])

            sound = pygame.sndarray.make_sound(arr)
            sound.set_volume(self.volume)
            self.sounds['win'] = sound
        except:
            pass

    def _create_game_over_sound(self):
        """创建游戏结束音效"""
        try:
            sample_rate = 22050
            duration = 0.8
            frequency = 150

            frames = int(duration * sample_rate)
            arr = []
            for i in range(frames):
                wave = 4096 * (frequency / sample_rate * i)
                wave = int(wave % (2 * 4096) - 4096)
                arr.append([wave, wave])

            sound = pygame.sndarray.make_sound(arr)
            sound.set_volume(self.volume)
            self.sounds['game_over'] = sound
        except:
            pass