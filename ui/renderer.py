# -*- coding: utf-8 -*-
"""
游戏渲染引擎
负责绘制游戏画面和UI元素
"""

import pygame
import math
from typing import Tuple, Optional
from game.game_logic import GameLogic, GameState
from game.board import Cell


class Renderer:
    """游戏渲染器类"""

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        # 游戏板设置
        self.cell_size = 30
        self.board_offset_x = 50
        self.board_offset_y = 150
        self.board_padding = 10

        # UI设置
        self.ui_height = 100
        self.button_width = 120
        self.button_height = 40

    def screen_to_board(self, x: int, y: int) -> Tuple[Optional[int], Optional[int]]:
        """将屏幕坐标转换为游戏板坐标"""
        board_x = x - self.board_offset_x - self.board_padding
        board_y = y - self.board_offset_y - self.board_padding

        if board_x < 0 or board_y < 0:
            return None, None

        col = board_x // (self.cell_size + 2)
        row = board_y // (self.cell_size + 2)

        return col, row

    def board_to_screen(self, row: int, col: int) -> Tuple[int, int]:
        """将游戏板坐标转换为屏幕坐标"""
        x = self.board_offset_x + self.board_padding + col * (self.cell_size + 2)
        y = self.board_offset_y + self.board_padding + row * (self.cell_size + 2)
        return x, y

    def draw_game(self, game_logic: GameLogic, fonts, colors):
        """绘制完整游戏画面"""
        # 绘制背景
        self._draw_background(colors)

        # 绘制游戏标题
        self._draw_title(fonts, colors)

        # 绘制UI面板
        self._draw_ui_panel(game_logic, fonts, colors)

        # 绘制游戏板
        self._draw_board(game_logic, fonts, colors)

        # 绘制游戏结束画面
        if game_logic.get_game_state() in [GameState.WON, GameState.LOST]:
            self._draw_game_over(game_logic, fonts, colors)

    def _draw_background(self, colors):
        """绘制背景"""
        # 创建渐变背景
        gradient_surface = colors.create_gradient_surface(
            self.screen_width, self.screen_height
        )
        self.screen.blit(gradient_surface, (0, 0))

    def _draw_title(self, fonts, colors):
        """绘制游戏标题"""
        title_text = "扫雷游戏"
        title_surface, title_rect = fonts.render_text_smart(
            title_text, 'orbitron_large', colors.text_white,
            (self.screen_width // 2, 40)
        )
        self.screen.blit(title_surface, title_rect)

    def _draw_ui_panel(self, game_logic: GameLogic, fonts, colors):
        """绘制UI面板"""
        # 绘制面板背景
        panel_rect = pygame.Rect(
            self.board_offset_x,
            self.board_offset_y - 80,
            self._get_board_width(game_logic),
            70
        )
        panel_surface = pygame.Surface((panel_rect.width, panel_rect.height))
        panel_surface.set_alpha(51)  # 半透明
        panel_surface.fill((0, 0, 0))
        self.screen.blit(panel_surface, panel_rect)

        # 绘制剩余雷数
        mines_left = game_logic.get_mines_left()
        mines_text = f"剩余雷数: {mines_left}"
        mines_surface = fonts.render_text_smart(
            mines_text, 'orbitron_bold', colors.text_white
        )
        mines_rect = mines_surface.get_rect(
            left=panel_rect.left + 20,
            centery=panel_rect.centery
        )
        self.screen.blit(mines_surface, mines_rect)

        # 绘制计时器
        timer_text = f"时间: {game_logic.get_timer().get_formatted_time()}"
        timer_surface = fonts.render_text_smart(
            timer_text, 'orbitron_bold', colors.text_white
        )
        timer_rect = timer_surface.get_rect(
            right=panel_rect.right - 20,
            centery=panel_rect.centery
        )
        self.screen.blit(timer_surface, timer_rect)

        # 绘制难度指示
        difficulty = game_logic.current_difficulty
        diff_text = "难度: " + ("简单" if difficulty == 'easy' else "困难")
        diff_surface = fonts.render_text_smart(
            diff_text, 'orbitron_normal', colors.text_white
        )
        diff_rect = diff_surface.get_rect(
            centerx=panel_rect.centerx,
            centery=panel_rect.centery
        )
        self.screen.blit(diff_surface, diff_rect)

    def _draw_board(self, game_logic: GameLogic, fonts, colors):
        """绘制游戏板"""
        board = game_logic.get_board()
        board_width = self._get_board_width(game_logic)
        board_height = self._get_board_height(game_logic)

        # 绘制游戏板背景
        board_rect = pygame.Rect(
            self.board_offset_x,
            self.board_offset_y,
            board_width,
            board_height
        )
        board_surface = pygame.Surface((board_rect.width, board_rect.height))
        board_surface.set_alpha(51)  # 半透明
        board_surface.fill((0, 0, 0))
        self.screen.blit(board_surface, board_rect)

        # 绘制所有格子
        for row in range(board.rows):
            for col in range(board.cols):
                self._draw_cell(board.cells[row][col], row, col, fonts, colors)

    def _draw_cell(self, cell: Cell, row: int, col: int, fonts, colors):
        """绘制单个格子"""
        x, y = self.board_to_screen(row, col)
        cell_rect = pygame.Rect(x, y, self.cell_size, self.cell_size)

        # 绘制格子背景
        if cell.is_revealed:
            pygame.draw.rect(self.screen, colors.cell_revealed[:3], cell_rect)
        elif cell.is_flagged:
            pygame.draw.rect(self.screen, colors.cell_flagged, cell_rect)
        else:
            pygame.draw.rect(self.screen, colors.cell_unrevealed[:3], cell_rect)

        # 绘制格子边框
        pygame.draw.rect(self.screen, colors.text_white, cell_rect, 1)

        # 绘制格子内容
        if cell.is_flagged:
            # 绘制旗子
            flag_text = "🚩"
            flag_surface = fonts.render_text(flag_text, 'orbitron_small', colors.text_black)
            flag_rect = flag_surface.get_rect(center=cell_rect.center)
            self.screen.blit(flag_surface, flag_rect)

        elif cell.is_revealed:
            if cell.is_mine:
                # 绘制地雷
                mine_text = "💣"
                mine_surface = fonts.render_text(mine_text, 'orbitron_small', colors.text_white)
                mine_rect = mine_surface.get_rect(center=cell_rect.center)
                self.screen.blit(mine_surface, mine_rect)
            elif cell.neighbor_mines > 0:
                # 绘制数字
                number_text = str(cell.neighbor_mines)
                number_color = colors.get_number_color(cell.neighbor_mines)
                number_surface = fonts.render_text(number_text, 'orbitron_bold', number_color)
                number_rect = number_surface.get_rect(center=cell_rect.center)
                self.screen.blit(number_surface, number_rect)

    def _draw_game_over(self, game_logic: GameLogic, fonts, colors):
        """绘制游戏结束画面"""
        # 绘制半透明遮罩
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # 绘制结束信息
        if game_logic.get_game_state() == GameState.WON:
            title_text = "恭喜获胜！"
            title_color = colors.win_color
            message_text = f"你成功找到了所有地雷！"
        else:
            title_text = "游戏结束"
            title_color = colors.lose_color
            message_text = "很遗憾，你踩到地雷了！"

        # 绘制标题
        title_surface, title_rect = fonts.render_text_smart(
            title_text, 'orbitron_large', title_color,
            (self.screen_width // 2, self.screen_height // 2 - 50)
        )
        self.screen.blit(title_surface, title_rect)

        # 绘制消息
        message_surface, message_rect = fonts.render_text_smart(
            message_text, 'orbitron_bold', colors.text_white,
            (self.screen_width // 2, self.screen_height // 2)
        )
        self.screen.blit(message_surface, message_rect)

        # 绘制操作提示
        hint_text = "按 N 键开始新游戏"
        hint_surface, hint_rect = fonts.render_text_smart(
            hint_text, 'orbitron_normal', colors.text_white,
            (self.screen_width // 2, self.screen_height // 2 + 50)
        )
        self.screen.blit(hint_surface, hint_rect)

    def _get_board_width(self, game_logic: GameLogic) -> int:
        """获取游戏板宽度"""
        board = game_logic.get_board()
        return (self.cell_size + 2) * board.cols + self.board_padding * 2

    def _get_board_height(self, game_logic: GameLogic) -> int:
        """获取游戏板高度"""
        board = game_logic.get_board()
        return (self.cell_size + 2) * board.rows + self.board_padding * 2

    def get_board_rect(self, game_logic: GameLogic) -> pygame.Rect:
        """获取游戏板矩形区域"""
        return pygame.Rect(
            self.board_offset_x,
            self.board_offset_y,
            self._get_board_width(game_logic),
            self._get_board_height(game_logic)
        )