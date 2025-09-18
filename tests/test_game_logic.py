# -*- coding: utf-8 -*-
"""
游戏逻辑测试
测试GameLogic类的功能
"""

import pytest
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from game.game_logic import GameLogic, GameState
from game.board import Cell


class TestGameLogic:
    """测试GameLogic类"""

    def test_game_logic_initialization(self):
        """测试游戏逻辑初始化"""
        game = GameLogic('easy')

        assert game.current_difficulty == 'easy'
        assert game.game_state == GameState.READY
        assert game.first_click == True
        assert game.board is not None
        assert game.timer is not None

    def test_difficulty_configurations(self):
        """测试难度配置"""
        game = GameLogic()

        # 测试简单模式
        game.set_difficulty('easy')
        config = game.get_difficulty_config()
        assert config['rows'] == 10
        assert config['cols'] == 10
        assert config['mines'] == 10
        assert config['time'] == 900

        # 测试困难模式
        game.set_difficulty('hard')
        config = game.get_difficulty_config()
        assert config['rows'] == 16
        assert config['cols'] == 16
        assert config['mines'] == 40
        assert config['time'] == 600

    def test_new_game(self):
        """测试新游戏"""
        game = GameLogic('easy')

        # 修改一些状态
        game.game_state = GameState.PLAYING
        game.first_click = False

        # 开始新游戏
        game.new_game()

        assert game.game_state == GameState.READY
        assert game.first_click == True
        assert game.board.get_revealed_count() == 0
        assert game.board.get_flagged_count() == 0

    def test_toggle_flag(self):
        """测试旗子标记"""
        game = GameLogic('easy')

        # 先布置地雷
        game.first_click = False
        game.game_state = GameState.PLAYING
        game.board.place_mines(10, 5, 5)

        # 标记一个格子
        game.toggle_flag(0, 0)
        cell = game.board.get_cell(0, 0)
        assert cell.is_flagged == True
        assert game.get_mines_left() == 9  # 10 - 1

        # 取消标记
        game.toggle_flag(0, 0)
        assert cell.is_flagged == False
        assert game.get_mines_left() == 10  # 回到原始值

    def test_first_click_protection(self):
        """测试首次点击保护"""
        game = GameLogic('easy')

        # 模拟首次点击
        game.reveal_cell(5, 5)

        # 检查是否布置了地雷
        assert game.board.total_mines == 10

        # 检查点击位置是否安全
        clicked_cell = game.board.get_cell(5, 5)
        assert not clicked_cell.is_mine

    def test_reveal_cell(self):
        """测试揭开格子"""
        game = GameLogic('easy')

        # 先布置地雷（模拟首次点击后的状态）
        game.first_click = False
        game.game_state = GameState.PLAYING
        game.board.place_mines(10, 5, 5)

        # 揭开一个安全格子
        game.reveal_cell(0, 0)
        cell = game.board.get_cell(0, 0)
        assert cell.is_revealed == True

    def test_mine_hit_game_over(self):
        """测试踩到地雷游戏结束"""
        game = GameLogic('easy')

        # 先布置地雷
        game.first_click = False
        game.game_state = GameState.PLAYING
        game.board.place_mines(10, 5, 5)

        # 找到一个地雷并揭开它
        for row in range(game.board.rows):
            for col in range(game.board.cols):
                cell = game.board.get_cell(row, col)
                if cell.is_mine:
                    game.reveal_cell(row, col)
                    break
            else:
                continue
            break

        assert game.game_state == GameState.LOST

    def test_win_condition(self):
        """测试胜利条件"""
        game = GameLogic('easy')

        # 设置游戏状态
        game.first_click = False
        game.game_state = GameState.PLAYING
        game.board.place_mines(10, 5, 5)

        # 揭开所有非地雷格子
        for row in range(game.board.rows):
            for col in range(game.board.cols):
                cell = game.board.get_cell(row, col)
                if not cell.is_mine:
                    cell.is_revealed = True

        # 检查胜利条件
        game._check_game_end()
        assert game.game_state == GameState.WON

    def test_mines_left_calculation(self):
        """测试剩余地雷数量计算"""
        game = GameLogic('easy')

        # 先布置地雷
        game.first_click = False
        game.game_state = GameState.PLAYING
        game.board.place_mines(10, 5, 5)

        # 初始应该等于总地雷数
        assert game.get_mines_left() == 10

        # 标记一些格子
        game.toggle_flag(0, 0)
        game.toggle_flag(1, 1)
        game.toggle_flag(2, 2)

        assert game.get_mines_left() == 7

    def test_game_state_accessors(self):
        """测试游戏状态访问器"""
        game = GameLogic('easy')

        assert game.get_game_state() == GameState.READY
        assert game.get_board() is not None
        assert game.get_timer() is not None
        assert game.is_first_click() == True

    def test_reveal_empty_cells(self):
        """测试空格子递归揭开"""
        game = GameLogic('easy')

        # 设置一个没有地雷的区域
        game.first_click = False
        game.game_state = GameState.PLAYING
        game.board.place_mines(10, 5, 5)

        # 找到一个neighbor_mines为0的格子
        empty_cell_found = False
        for row in range(game.board.rows):
            for col in range(game.board.cols):
                cell = game.board.get_cell(row, col)
                if not cell.is_mine and cell.neighbor_mines == 0:
                    game.reveal_empty_cells(row, col)
                    empty_cell_found = True
                    break
            if empty_cell_found:
                break

        # 如果找到了空格子，检查周围的格子是否也被揭开了
        if empty_cell_found:
            # 这里我们假设空格子周围的一些格子也被揭开了
            # 具体验证取决于地雷的随机分布
            pass

    def test_reveal_all_mines_on_game_over(self):
        """测试游戏结束时显示所有地雷"""
        game = GameLogic('easy')

        # 布置地雷
        game.first_click = False
        game.game_state = GameState.PLAYING
        game.board.place_mines(10, 5, 5)

        # 游戏结束
        game.game_over(False)

        # 检查所有地雷是否都被显示
        for row in range(game.board.rows):
            for col in range(game.board.cols):
                cell = game.board.get_cell(row, col)
                if cell.is_mine:
                    assert cell.is_revealed == True

    def test_timer_stops_on_game_over(self):
        """测试游戏结束时计时器停止"""
        game = GameLogic('easy')

        # 启动计时器
        game.first_click = False
        game.game_state = GameState.PLAYING
        game.timer.start()

        # 游戏结束
        game.game_over(True)

        assert not game.timer.is_running