# -*- coding: utf-8 -*-
"""
计时器测试
测试Timer类的功能
"""

import pytest
import sys
import os
import time

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from game.timer import Timer


class TestTimer:
    """测试Timer类"""

    def test_timer_initialization(self):
        """测试计时器初始化"""
        timer = Timer(60)
        assert timer.duration == 60
        assert timer.time_left == 60
        assert not timer.is_running

    def test_timer_start_stop(self):
        """测试计时器启动和停止"""
        timer = Timer(10)

        # 启动计时器
        timer.start()
        assert timer.is_running
        assert timer.start_time > 0

        # 停止计时器
        timer.stop()
        assert not timer.is_running

    def test_timer_reset(self):
        """测试计时器重置"""
        timer = Timer(30)

        # 启动并等待一会儿
        timer.start()
        time.sleep(0.1)
        timer.update()

        # 记录当前时间
        time_before_reset = timer.time_left

        # 重置计时器
        timer.reset()
        assert timer.time_left == 30
        assert not timer.is_running
        assert timer.start_time == 0

        # 确保时间被重置（如果时间确实减少了）
        if time_before_reset < timer.duration:
            assert timer.time_left > time_before_reset

    def test_timer_reset_with_duration(self):
        """测试重置计时器并设置新的持续时间"""
        timer = Timer(10)

        # 重置为新的持续时间
        timer.reset(20)
        assert timer.duration == 20
        assert timer.time_left == 20

    def test_timer_update(self):
        """测试计时器更新"""
        timer = Timer(2)

        # 未启动时更新
        timer.update()
        assert timer.time_left == 2

        # 启动后更新
        timer.start()
        time.sleep(1.5)  # 等待足够长时间确保时间减少
        timer.update()
        assert timer.time_left < 2

    def test_timer_expiration(self):
        """测试计时器到期"""
        timer = Timer(1)
        time_up_called = False

        def time_up_callback():
            nonlocal time_up_called
            time_up_called = True

        timer.set_time_up_callback(time_up_callback)
        timer.start()

        # 等待计时器到期
        while timer.time_left > 0:
            timer.update()
            time.sleep(0.01)

        assert timer.is_expired()
        assert not timer.is_running
        assert time_up_called

    def test_timer_tick_callback(self):
        """测试计时器每秒回调"""
        timer = Timer(3)
        tick_calls = []

        def tick_callback(time_left):
            tick_calls.append(time_left)

        timer.set_tick_callback(tick_callback)
        timer.start()

        # 等待一段时间
        time.sleep(2.5)
        timer.update()

        # 应该有几次tick调用
        assert len(tick_calls) > 0

    def test_formatted_time(self):
        """测试格式化时间输出"""
        timer = Timer(90)

        # 测试初始时间
        assert timer.get_formatted_time() == "1:30"

        # 测试剩余时间
        timer.time_left = 65
        assert timer.get_formatted_time() == "1:05"

        timer.time_left = 0
        assert timer.get_formatted_time() == "0:00"

        timer.time_left = 125
        assert timer.get_formatted_time() == "2:05"

    def test_percentage_left(self):
        """测试剩余时间百分比"""
        timer = Timer(100)

        # 初始应该为100%
        assert timer.get_percentage_left() == 100.0

        # 一半时间
        timer.time_left = 50
        assert timer.get_percentage_left() == 50.0

        # 四分之一时间
        timer.time_left = 25
        assert timer.get_percentage_left() == 25.0

        # 时间到期
        timer.time_left = 0
        assert timer.get_percentage_left() == 0.0

    def test_zero_duration_timer(self):
        """测试零持续时间计时器"""
        timer = Timer(0)

        # 应该立即到期
        assert timer.is_expired()
        assert timer.get_percentage_left() == 0.0
        assert timer.get_formatted_time() == "0:00"