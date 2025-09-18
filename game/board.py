# -*- coding: utf-8 -*-
"""
游戏板数据结构
定义格子状态和游戏板操作
"""

import random
from typing import List, Tuple, Optional


class Cell:
    """游戏格子类"""

    def __init__(self):
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.neighbor_mines = 0


class Board:
    """游戏板类"""

    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.cells: List[List[Cell]] = []
        self.total_mines = 0
        self._create_board()

    def _create_board(self):
        """创建空白游戏板"""
        self.cells = [[Cell() for _ in range(self.cols)] for _ in range(self.rows)]

    def get_cell(self, row: int, col: int) -> Optional[Cell]:
        """获取指定位置的格子"""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.cells[row][col]
        return None

    def is_valid_position(self, row: int, col: int) -> bool:
        """检查位置是否有效"""
        return 0 <= row < self.rows and 0 <= col < self.cols

    def place_mines(self, total_mines: int, exclude_row: int, exclude_col: int):
        """布置地雷，避开指定位置"""
        self.total_mines = total_mines
        mines_placed = 0

        while mines_placed < total_mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)

            # 避开排除位置和已有地雷位置
            if (row != exclude_row or col != exclude_col) and not self.cells[row][col].is_mine:
                self.cells[row][col].is_mine = True
                mines_placed += 1

        # 计算每个格子周围的地雷数量
        self._calculate_neighbor_mines()

    def _calculate_neighbor_mines(self):
        """计算每个格子周围的地雷数量"""
        for row in range(self.rows):
            for col in range(self.cols):
                if not self.cells[row][col].is_mine:
                    self.cells[row][col].neighbor_mines = self._count_neighbor_mines(row, col)

    def _count_neighbor_mines(self, row: int, col: int) -> int:
        """计算指定格子周围的地雷数量"""
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue

                new_row, new_col = row + dr, col + dc
                if self.is_valid_position(new_row, new_col):
                    if self.cells[new_row][new_col].is_mine:
                        count += 1

        return count

    def get_neighbors(self, row: int, col: int) -> List[Tuple[int, int]]:
        """获取指定格子的所有有效邻居位置"""
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue

                new_row, new_col = row + dr, col + dc
                if self.is_valid_position(new_row, new_col):
                    neighbors.append((new_row, new_col))

        return neighbors

    def reset(self):
        """重置游戏板"""
        self._create_board()
        self.total_mines = 0

    def get_revealed_count(self) -> int:
        """获取已揭开的格子数量"""
        count = 0
        for row in range(self.rows):
            for col in range(self.cols):
                if self.cells[row][col].is_revealed:
                    count += 1
        return count

    def get_flagged_count(self) -> int:
        """获取已标记的格子数量"""
        count = 0
        for row in range(self.rows):
            for col in range(self.cols):
                if self.cells[row][col].is_flagged:
                    count += 1
        return count

    def get_total_cells(self) -> int:
        """获取总格子数量"""
        return self.rows * self.cols