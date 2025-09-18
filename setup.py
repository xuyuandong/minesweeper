# -*- coding: utf-8 -*-
"""
扫雷游戏打包脚本
使用PyInstaller创建可执行文件
"""

from setuptools import setup, find_packages
import os

# 读取README文件
def read_readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()

# 读取requirements文件
def read_requirements():
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="minesweeper",
    version="1.0.0",
    description="Python扫雷游戏",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Claude",
    packages=find_packages(),
    install_requires=read_requirements(),
    entry_points={
        'console_scripts': [
            'minesweeper=main:main',
        ],
    },
    include_package_data=True,
    package_data={
        '': ['assets/**/*'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Games/Entertainment :: Puzzle Games",
    ],
    python_requires=">=3.7",
)