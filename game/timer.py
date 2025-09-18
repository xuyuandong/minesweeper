# -*- coding: utf-8 -*-
"""
游戏计时器
提供倒计时功能
"""

import time
from typing import Callable, Optional


class Timer:
    """游戏计时器类"""

    def __init__(self, duration_seconds: int):
        self.duration = duration_seconds
        self.time_left = duration_seconds
        self.is_running = False
        self.start_time = 0
        self.on_time_up_callback: Optional[Callable] = None
        self.on_tick_callback: Optional[Callable] = None

    def start(self):
        """启动计时器"""
        if not self.is_running:
            self.is_running = True
            self.start_time = time.time()

    def stop(self):
        """停止计时器"""
        self.is_running = False

    def reset(self, duration_seconds: Optional[int] = None):
        """重置计时器"""
        if duration_seconds is not None:
            self.duration = duration_seconds
        self.time_left = self.duration
        self.is_running = False
        self.start_time = 0

    def update(self):
        """更新计时器状态"""
        if self.is_running:
            elapsed = time.time() - self.start_time
            self.time_left = max(0, self.duration - int(elapsed))

            if self.time_left <= 0:
                self.stop()
                if self.on_time_up_callback:
                    self.on_time_up_callback()
            elif self.on_tick_callback:
                self.on_tick_callback(self.time_left)

    def get_formatted_time(self) -> str:
        """获取格式化的时间字符串"""
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        return f"{minutes}:{seconds:02d}"

    def set_time_up_callback(self, callback: Callable):
        """设置时间到期回调"""
        self.on_time_up_callback = callback

    def set_tick_callback(self, callback: Callable):
        """设置每秒回调"""
        self.on_tick_callback = callback

    def is_expired(self) -> bool:
        """检查时间是否已到期"""
        return self.time_left <= 0

    def get_time_left(self) -> int:
        """获取剩余时间"""
        return self.time_left

    def get_percentage_left(self) -> float:
        """获取剩余时间百分比"""
        if self.duration == 0:
            return 0.0
        return (self.time_left / self.duration) * 100