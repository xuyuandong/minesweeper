# -*- coding: utf-8 -*-
"""
游戏核心逻辑
处理游戏状态、用户输入和游戏规则
"""

from enum import Enum
from typing import List, Tuple, Optional, Set
from .board import Board, Cell
from .timer import Timer
from .sound_manager import SoundManager


class GameState(Enum):
    """游戏状态枚举"""
    READY = "ready"
    PLAYING = "playing"
    WON = "won"
    LOST = "lost"


class GameLogic:
    """游戏逻辑类"""

    def __init__(self, difficulty: str = 'easy'):
        self.difficulties = {
            'easy': {
                'rows': 10,
                'cols': 10,
                'mines': 10,
                'time': 900  # 15分钟
            },
            'hard': {
                'rows': 16,
                'cols': 16,
                'mines': 40,
                'time': 600  # 10分钟
            }
        }

        self.current_difficulty = difficulty
        self.game_state = GameState.READY
        self.first_click = True

        # 初始化游戏板、计时器和音效
        self._init_game()
        self._setup_timer_callbacks()
        self.sound_manager = SoundManager()

    def _init_game(self):
        """初始化游戏组件"""
        config = self.difficulties[self.current_difficulty]
        self.board = Board(config['rows'], config['cols'])
        self.timer = Timer(config['time'])

    def _setup_timer_callbacks(self):
        """设置计时器回调"""
        self.timer.set_time_up_callback(self._on_time_up)
        self.timer.set_tick_callback(self._on_timer_tick)

    def set_difficulty(self, difficulty: str):
        """设置游戏难度"""
        if difficulty in self.difficulties:
            self.current_difficulty = difficulty
            self.new_game()

    def new_game(self):
        """开始新游戏"""
        self.game_state = GameState.READY
        self.first_click = True
        self.board.reset()

        config = self.difficulties[self.current_difficulty]
        self.timer.reset(config['time'])

    def handle_left_click(self, x: int, y: int, renderer) -> bool:
        """处理左键点击"""
        if self.game_state in [GameState.WON, GameState.LOST]:
            return False

        # 转换屏幕坐标到游戏板坐标
        board_x, board_y = renderer.screen_to_board(x, y)
        if board_x is None or board_y is None:
            return False

        row, col = board_y, board_x
        cell = self.board.get_cell(row, col)

        if not cell or cell.is_revealed or cell.is_flagged:
            return False

        # 揭开格子
        self.reveal_cell(row, col)
        self.sound_manager.play_sound('click')

        # 检查游戏是否结束
        self._check_game_end()

        return True

    def handle_right_click(self, x: int, y: int, renderer) -> bool:
        """处理右键点击"""
        if self.game_state in [GameState.WON, GameState.LOST]:
            return False

        # 转换屏幕坐标到游戏板坐标
        board_x, board_y = renderer.screen_to_board(x, y)
        if board_x is None or board_y is None:
            return False

        row, col = board_y, board_x
        cell = self.board.get_cell(row, col)

        if not cell or cell.is_revealed:
            return False

        # 切换旗子标记
        self.toggle_flag(row, col)
        self.sound_manager.play_sound('flag')
        return True

    def reveal_cell(self, row: int, col: int):
        """揭开指定格子"""
        cell = self.board.get_cell(row, col)
        if not cell or cell.is_revealed or cell.is_flagged:
            return

        # 首次点击保护
        if self.first_click:
            self.first_click = False
            self.game_state = GameState.PLAYING
            self.board.place_mines(
                self.difficulties[self.current_difficulty]['mines'],
                row, col
            )
            self.timer.start()

        cell.is_revealed = True

        # 如果踩到地雷，游戏结束
        if cell.is_mine:
            self.sound_manager.play_sound('mine')
            self.game_over(False)
            return

        # 如果是空格子，递归揭开周围的格子
        if cell.neighbor_mines == 0:
            self.reveal_empty_cells(row, col)

    def reveal_empty_cells(self, row: int, col: int):
        """递归揭开空格子"""
        visited = set()
        self._reveal_empty_cells_recursive(row, col, visited)

    def _reveal_empty_cells_recursive(self, row: int, col: int, visited: Set[Tuple[int, int]]):
        """递归揭开空格子的内部实现"""
        if (row, col) in visited:
            return

        visited.add((row, col))
        cell = self.board.get_cell(row, col)

        if not cell or cell.is_revealed or cell.is_flagged or cell.is_mine:
            return

        cell.is_revealed = True

        # 如果周围没有地雷，继续递归
        if cell.neighbor_mines == 0:
            neighbors = self.board.get_neighbors(row, col)
            for n_row, n_col in neighbors:
                self._reveal_empty_cells_recursive(n_row, n_col, visited)

    def toggle_flag(self, row: int, col: int):
        """切换旗子标记"""
        cell = self.board.get_cell(row, col)
        if cell and not cell.is_revealed:
            cell.is_flagged = not cell.is_flagged

    def game_over(self, won: bool):
        """游戏结束"""
        self.game_state = GameState.WON if won else GameState.LOST
        self.timer.stop()

        # 播放相应的音效
        if won:
            self.sound_manager.play_sound('win')
        else:
            self.sound_manager.play_sound('game_over')
            # 显示所有地雷
            self._reveal_all_mines()

    def _reveal_all_mines(self):
        """显示所有地雷"""
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                cell = self.board.get_cell(row, col)
                if cell and cell.is_mine:
                    cell.is_revealed = True

    def _check_game_end(self):
        """检查游戏是否结束"""
        if self.game_state != GameState.PLAYING:
            return

        # 检查是否胜利
        total_cells = self.board.get_total_cells()
        revealed_cells = self.board.get_revealed_count()
        mines_count = self.board.total_mines

        if revealed_cells == total_cells - mines_count:
            self.game_over(True)

    def _on_time_up(self):
        """时间到期回调"""
        if self.game_state == GameState.PLAYING:
            self.game_over(False)

    def _on_timer_tick(self, time_left: int):
        """计时器每秒回调"""
        # 可以在这里添加每秒更新逻辑
        pass

    def update(self):
        """更新游戏状态"""
        self.timer.update()

    def get_mines_left(self) -> int:
        """获取剩余地雷数量"""
        return self.board.total_mines - self.board.get_flagged_count()

    def get_game_state(self) -> GameState:
        """获取游戏状态"""
        return self.game_state

    def get_difficulty_config(self) -> dict:
        """获取当前难度配置"""
        return self.difficulties[self.current_difficulty]

    def get_board(self) -> Board:
        """获取游戏板"""
        return self.board

    def get_timer(self) -> Timer:
        """获取计时器"""
        return self.timer

    def is_first_click(self) -> bool:
        """是否为首次点击"""
        return self.first_click