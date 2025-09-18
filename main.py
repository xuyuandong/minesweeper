#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
扫雷游戏主程序
基于Pygame的扫雷游戏实现
"""

import pygame
import sys
from game.game_logic import GameLogic
from ui.renderer import Renderer
from ui.colors import Colors
from ui.fonts import Fonts


def main():
    """主游戏循环"""
    pygame.init()

    # 游戏设置
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 700
    FPS = 60

    # 创建游戏窗口
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("扫雷游戏")

    # 创建游戏对象
    game_logic = GameLogic()
    renderer = Renderer(screen)
    fonts = Fonts()
    colors = Colors()

    # 游戏时钟
    clock = pygame.time.Clock()

    # 游戏主循环
    running = True
    while running:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # 鼠标点击事件
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键
                    x, y = event.pos
                    game_logic.handle_left_click(x, y, renderer)
                elif event.button == 3:  # 右键
                    x, y = event.pos
                    game_logic.handle_right_click(x, y, renderer)

            # 键盘事件
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:  # N键开始新游戏
                    game_logic.new_game()
                elif event.key == pygame.K_1:  # 1键简单模式
                    game_logic.set_difficulty('easy')
                    game_logic.new_game()
                elif event.key == pygame.K_2:  # 2键困难模式
                    game_logic.set_difficulty('hard')
                    game_logic.new_game()
                elif event.key == pygame.K_s:  # S键切换音效
                    game_logic.sound_manager.toggle_sound()
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:  # +键增加音量
                    current_volume = game_logic.sound_manager.get_volume()
                    game_logic.sound_manager.set_volume(min(1.0, current_volume + 0.1))
                elif event.key == pygame.K_MINUS:  # -键减少音量
                    current_volume = game_logic.sound_manager.get_volume()
                    game_logic.sound_manager.set_volume(max(0.0, current_volume - 0.1))

        # 更新游戏状态
        game_logic.update()

        # 渲染游戏画面
        screen.fill(colors.background)
        renderer.draw_game(game_logic, fonts, colors)

        # 更新显示
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()