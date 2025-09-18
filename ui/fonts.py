# -*- coding: utf-8 -*-
"""
游戏字体管理
处理游戏中的字体加载和管理
"""

import pygame
import os
from typing import Dict, Optional


class Fonts:
    """游戏字体类"""

    def __init__(self):
        self.fonts: Dict[str, pygame.font.Font] = {}
        self._load_fonts()

    def _load_fonts(self):
        """加载游戏字体"""
        try:
            # 优先加载支持中文的字体
            chinese_fonts = ['adobesongstdlight', 'songti', 'stheitimedium', 'stheitilight', 'adobefangsongstd']

            # 尝试加载中文字体
            self.fonts['chinese_normal'] = self._load_chinese_font(chinese_fonts, 16)
            self.fonts['chinese_bold'] = self._load_chinese_font(chinese_fonts, 20, bold=True)
            self.fonts['chinese_large'] = self._load_chinese_font(chinese_fonts, 32, bold=True)
            self.fonts['chinese_small'] = self._load_chinese_font(chinese_fonts, 14)

            # 尝试加载英文字体（用于数字和英文字符）
            self.fonts['orbitron_bold'] = self._load_font_or_default(None, 20, bold=True)
            self.fonts['orbitron_normal'] = self._load_font_or_default(None, 16)
            self.fonts['orbitron_large'] = self._load_font_or_default(None, 32, bold=True)
            self.fonts['orbitron_small'] = self._load_font_or_default(None, 14)

        except Exception as e:
            print(f"字体加载失败，使用默认字体: {e}")
            # 使用默认字体
            self.fonts['chinese_normal'] = pygame.font.Font(None, 16)
            self.fonts['chinese_bold'] = pygame.font.Font(None, 20)
            self.fonts['chinese_large'] = pygame.font.Font(None, 32)
            self.fonts['chinese_small'] = pygame.font.Font(None, 14)
            self.fonts['orbitron_bold'] = pygame.font.Font(None, 20)
            self.fonts['orbitron_normal'] = pygame.font.Font(None, 16)
            self.fonts['orbitron_large'] = pygame.font.Font(None, 32)
            self.fonts['orbitron_small'] = pygame.font.Font(None, 14)

    def _load_chinese_font(self, font_names: list, size: int, bold: bool = False) -> pygame.font.Font:
        """加载中文字体"""
        system_fonts = pygame.font.get_fonts()

        # 优先尝试中文字体
        for font_name in font_names:
            if font_name.lower() in [f.lower() for f in system_fonts]:
                try:
                    return pygame.font.SysFont(font_name, size, bold)
                except:
                    continue

        # 如果没有中文字体，尝试其他可能支持中文的字体
        fallback_fonts = ['arialunicode', 'arial', 'helvetica', 'verdana', 'tahoma']
        for font_name in fallback_fonts:
            if font_name in system_fonts:
                try:
                    return pygame.font.SysFont(font_name, size, bold)
                except:
                    continue

        # 最后使用默认字体
        return pygame.font.Font(None, size)

    def _load_font_or_default(self, font_path: Optional[str], size: int, bold: bool = False) -> pygame.font.Font:
        """加载字体或使用默认字体"""
        if font_path and os.path.exists(font_path):
            try:
                return pygame.font.Font(font_path, size)
            except:
                pass

        # 使用系统字体
        system_fonts = pygame.font.get_fonts()
        preferred_fonts = ['arial', 'verdana', 'tahoma', 'helvetica']

        for font_name in preferred_fonts:
            if font_name in system_fonts:
                try:
                    font = pygame.font.SysFont(font_name, size, bold)
                    return font
                except:
                    continue

        # 使用默认字体
        return pygame.font.Font(None, size)

    def get_font(self, name: str) -> pygame.font.Font:
        """获取指定字体"""
        return self.fonts.get(name, self.fonts['orbitron_normal'])

    def render_text(self, text: str, font_name: str, color: tuple, center: tuple = None) -> pygame.Surface:
        """渲染文本"""
        font = self.get_font(font_name)
        text_surface = font.render(text, True, color)

        if center:
            text_rect = text_surface.get_rect(center=center)
            return text_surface, text_rect

        return text_surface

    def render_text_centered(self, text: str, font_name: str, color: tuple, center: tuple) -> pygame.Surface:
        """渲染居中文本"""
        return self.render_text(text, font_name, color, center)

    def render_text_smart(self, text: str, font_name: str, color: tuple, center: tuple = None):
        """智能文本渲染：根据文本内容选择合适的字体"""
        # 检查文本是否包含中文字符
        has_chinese = any('\u4e00' <= char <= '\u9fff' for char in text)

        if has_chinese:
            # 使用中文字体
            chinese_font_map = {
                'orbitron_large': 'chinese_large',
                'orbitron_bold': 'chinese_bold',
                'orbitron_normal': 'chinese_normal',
                'orbitron_small': 'chinese_small'
            }
            actual_font = chinese_font_map.get(font_name, 'chinese_normal')
        else:
            # 使用英文字体
            actual_font = font_name

        return self.render_text(text, actual_font, color, center)