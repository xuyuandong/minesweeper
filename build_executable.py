# -*- coding: utf-8 -*-
"""
构建可执行文件脚本
使用PyInstaller创建独立的可执行文件
"""

import os
import sys
import subprocess
import shutil

def install_pyinstaller():
    """安装PyInstaller"""
    print("正在安装PyInstaller...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)

def build_executable():
    """构建可执行文件"""
    print("正在构建可执行文件...")

    # 清理之前的构建
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    if os.path.exists("build"):
        shutil.rmtree("build")

    # 构建命令
    cmd = [
        "pyinstaller",
        "--onefile",  # 单文件模式
        "--windowed",  # 无控制台窗口
        "--name", "Minesweeper",  # 输出文件名
        "--icon=assets/icon.ico" if os.path.exists("assets/icon.ico") else "",
        "--add-data", "assets:assets",  # 包含资源文件
        "main.py"  # 主程序文件
    ]

    # 移除空的参数
    cmd = [arg for arg in cmd if arg]

    # 执行构建
    subprocess.run(cmd, check=True)

    print("构建完成！")
    print(f"可执行文件位于: {os.path.abspath('dist/Minesweeper')}")

def create_installer():
    """创建安装程序（可选）"""
    print("创建安装程序...")

    # 这里可以添加创建安装程序的逻辑
    # 例如使用Inno Setup或NSIS

    print("安装程序创建功能暂未实现")

def main():
    """主函数"""
    print("=== 扫雷游戏打包工具 ===")

    try:
        # 检查PyInstaller是否已安装
        import PyInstaller
        print("PyInstaller已安装")
    except ImportError:
        print("PyInstaller未安装，正在安装...")
        install_pyinstaller()

    # 构建可执行文件
    build_executable()

    # 询问是否创建安装程序
    create_installer = input("是否创建安装程序？(y/n): ").lower().strip()
    if create_installer == 'y':
        create_installer()

    print("\n打包完成！")
    print("您可以将dist目录中的Minesweeper文件复制到任何地方运行。")

if __name__ == "__main__":
    main()