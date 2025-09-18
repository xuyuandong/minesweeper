# -*- coding: utf-8 -*-
"""
游戏颜色定义
包含游戏中使用的所有颜色
"""

import pygame


class Colors:
    """游戏颜色类"""

    def __init__(self):
        # 背景颜色
        self.background = (102, 126, 234)  # 渐变背景主色
        self.background_dark = (118, 75, 162)  # 渐变背景深色

        # 游戏板颜色
        self.board_bg = (0, 0, 0, 51)  # 半透明黑色
        self.board_border = (255, 255, 255, 51)  # 半透明白色

        # 格子颜色
        self.cell_unrevealed = (255, 255, 255, 204)  # 未揭开的格子
        self.cell_revealed = (0, 0, 0, 204)  # 已揭开的格子
        self.cell_hover = (255, 255, 255, 230)  # 鼠标悬停
        self.cell_flagged = (255, 217, 61)  # 旗子标记
        self.cell_mine = (255, 107, 107)  # 地雷

        # 数字颜色（1-8）
        self.number_colors = {
            1: (25, 118, 210),    # 蓝色
            2: (56, 142, 60),     # 绿色
            3: (211, 47, 47),     # 红色
            4: (123, 31, 162),    # 紫色
            5: (245, 124, 0),     # 橙色
            6: (0, 121, 107),     # 青色
            7: (48, 63, 159),     # 深蓝色
            8: (66, 66, 66)       # 灰色
        }

        # UI颜色
        self.text_white = (255, 255, 255)
        self.text_black = (0, 0, 0)
        self.button_green = (76, 175, 80)
        self.button_red = (255, 107, 107)
        self.button_blue = (33, 150, 243)

        # 游戏状态颜色
        self.win_color = (76, 175, 80)
        self.lose_color = (255, 107, 107)

    def get_number_color(self, number: int) -> tuple:
        """获取数字颜色"""
        return self.number_colors.get(number, self.text_white)

    def create_gradient_surface(self, width: int, height: int) -> pygame.Surface:
        """创建渐变背景表面"""
        surface = pygame.Surface((width, height))

        # 创建渐变效果
        for y in range(height):
            ratio = y / height
            r = int(self.background[0] * (1 - ratio) + self.background_dark[0] * ratio)
            g = int(self.background[1] * (1 - ratio) + self.background_dark[1] * ratio)
            b = int(self.background[2] * (1 - ratio) + self.background_dark[2] * ratio)
            pygame.draw.line(surface, (r, g, b), (0, y), (width, y))

        return surface