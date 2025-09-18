# -*- coding: utf-8 -*-
"""
游戏板测试
测试Board类和Cell类的功能
"""

import pytest
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from game.board import Board, Cell


class TestCell:
    """测试Cell类"""

    def test_cell_initialization(self):
        """测试格子初始化"""
        cell = Cell()
        assert not cell.is_mine
        assert not cell.is_revealed
        assert not cell.is_flagged
        assert cell.neighbor_mines == 0


class TestBoard:
    """测试Board类"""

    def test_board_creation(self):
        """测试游戏板创建"""
        board = Board(10, 10)
        assert board.rows == 10
        assert board.cols == 10
        assert board.total_mines == 0
        assert len(board.cells) == 10
        assert len(board.cells[0]) == 10

    def test_get_cell(self):
        """测试获取格子"""
        board = Board(10, 10)

        # 测试有效位置
        cell = board.get_cell(0, 0)
        assert cell is not None
        assert isinstance(cell, Cell)

        # 测试无效位置
        cell = board.get_cell(-1, 0)
        assert cell is None
        cell = board.get_cell(10, 10)
        assert cell is None

    def test_is_valid_position(self):
        """测试位置有效性检查"""
        board = Board(10, 10)

        # 有效位置
        assert board.is_valid_position(0, 0)
        assert board.is_valid_position(9, 9)
        assert board.is_valid_position(5, 5)

        # 无效位置
        assert not board.is_valid_position(-1, 0)
        assert not board.is_valid_position(10, 0)
        assert not board.is_valid_position(0, -1)
        assert not board.is_valid_position(0, 10)

    def test_place_mines(self):
        """测试地雷布置"""
        board = Board(10, 10)

        # 布置5个地雷，避开(5,5)位置
        board.place_mines(5, 5, 5)

        assert board.total_mines == 5

        # 检查排除位置没有地雷
        exclude_cell = board.get_cell(5, 5)
        assert not exclude_cell.is_mine

        # 检查地雷数量正确
        mine_count = 0
        for row in range(board.rows):
            for col in range(board.cols):
                if board.cells[row][col].is_mine:
                    mine_count += 1
        assert mine_count == 5

    def test_neighbor_mines_calculation(self):
        """测试周围地雷数量计算"""
        board = Board(5, 5)

        # 手动设置一些地雷
        board.cells[0][0].is_mine = True
        board.cells[0][1].is_mine = True
        board.cells[1][0].is_mine = True

        # 重新计算周围地雷数量
        board._calculate_neighbor_mines()

        # 检查(1,1)位置的周围地雷数量
        cell_1_1 = board.get_cell(1, 1)
        assert cell_1_1.neighbor_mines == 3

        # 检查(0,2)位置的周围地雷数量
        cell_0_2 = board.get_cell(0, 2)
        assert cell_0_2.neighbor_mines == 1  # 只有(0,1)是邻居地雷

    def test_get_neighbors(self):
        """测试获取邻居格子"""
        board = Board(5, 5)

        # 测试角落位置的邻居
        neighbors = board.get_neighbors(0, 0)
        assert len(neighbors) == 3  # 角落有3个邻居

        # 测试边缘位置的邻居
        neighbors = board.get_neighbors(0, 2)
        assert len(neighbors) == 5  # 边缘有5个邻居

        # 测试中心位置的邻居
        neighbors = board.get_neighbors(2, 2)
        assert len(neighbors) == 8  # 中心有8个邻居

    def test_reset(self):
        """测试游戏板重置"""
        board = Board(5, 5)

        # 设置一些地雷和标记
        board.place_mines(3, 2, 2)
        board.cells[0][0].is_flagged = True
        board.cells[1][1].is_revealed = True

        # 重置游戏板
        board.reset()

        # 检查所有格子都被重置
        for row in range(board.rows):
            for col in range(board.cols):
                cell = board.cells[row][col]
                assert not cell.is_mine
                assert not cell.is_revealed
                assert not cell.is_flagged
                assert cell.neighbor_mines == 0

        assert board.total_mines == 0

    def test_get_revealed_count(self):
        """测试已揭开格子计数"""
        board = Board(5, 5)

        # 初始应该为0
        assert board.get_revealed_count() == 0

        # 揭开一些格子
        board.cells[0][0].is_revealed = True
        board.cells[1][1].is_revealed = True

        assert board.get_revealed_count() == 2

    def test_get_flagged_count(self):
        """测试已标记格子计数"""
        board = Board(5, 5)

        # 初始应该为0
        assert board.get_flagged_count() == 0

        # 标记一些格子
        board.cells[0][0].is_flagged = True
        board.cells[1][1].is_flagged = True

        assert board.get_flagged_count() == 2

    def test_get_total_cells(self):
        """测试总格子数"""
        board = Board(5, 5)
        assert board.get_total_cells() == 25

        board = Board(10, 15)
        assert board.get_total_cells() == 150

    def test_mine_placement_exclusion(self):
        """测试地雷布置排除功能"""
        board = Board(5, 5)

        # 尝试在排除位置布置地雷
        board.place_mines(24, 2, 2)  # 几乎填满整个板子

        # 确保排除位置没有地雷
        exclude_cell = board.get_cell(2, 2)
        assert not exclude_cell.is_mine

        # 确保其他位置有地雷
        mine_count = 0
        for row in range(board.rows):
            for col in range(board.cols):
                if board.cells[row][col].is_mine:
                    mine_count += 1
        assert mine_count == 24