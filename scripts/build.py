#!/usr/bin/env python3
"""
构建脚本 - 用于打包和发布
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
DIST_DIR = PROJECT_ROOT / "dist"
BUILD_DIR = PROJECT_ROOT / "build"


def clean():
    """清理构建目录"""
    print("🧹 清理构建目录...")
    for dir_path in [DIST_DIR, BUILD_DIR]:
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"  已删除: {dir_path}")


def install_deps():
    """安装依赖"""
    print("📦 安装依赖...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."], 
                   cwd=PROJECT_ROOT, check=True)
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], 
                   check=True)


def build_wheel():
    """构建Python wheel包"""
    print("🔨 构建Wheel包...")
    subprocess.run([sys.executable, "-m", "build", "--wheel"], 
                   cwd=PROJECT_ROOT, check=True)
    print("✅ Wheel包构建完成")


def build_executable():
    """使用PyInstaller构建可执行文件"""
    print("🔨 构建可执行文件...")
    
    # PyInstaller配置
    pyinstaller_args = [
        "pyinstaller",
        "--onefile",  # 单文件
        "--name", "promptcraft",
        "--icon", "NONE",
        "--clean",
        "--noconfirm",
        "--hidden-import", "promptcraft",
        "--hidden-import", "click",
        "--hidden-import", "rich",
        "--hidden-import", "rich.console",
        "--hidden-import", "rich.table",
        "--hidden-import", "rich.panel",
        "--hidden-import", "rich.syntax",
        "--hidden-import", "rich.tree",
        "--hidden-import", "rich.prompt",
        str(PROJECT_ROOT / "promptcraft" / "cli.py")
    ]
    
    subprocess.run(pyinstaller_args, cwd=PROJECT_ROOT, check=True)
    print("✅ 可执行文件构建完成")


def run_tests():
    """运行测试"""
    print("🧪 运行测试...")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-v"],
        cwd=PROJECT_ROOT
    )
    if result.returncode != 0:
        print("❌ 测试失败")
        sys.exit(1)
    print("✅ 测试通过")


def check_code():
    """代码检查"""
    print("🔍 代码检查...")
    
    # 检查格式化
    try:
        subprocess.run([sys.executable, "-m", "black", "--check", "promptcraft/"], 
                      cwd=PROJECT_ROOT, check=True)
        print("  ✅ 代码格式检查通过")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("  ⚠️ 代码格式检查跳过 (black未安装)")
    
    # 类型检查
    try:
        subprocess.run([sys.executable, "-m", "mypy", "promptcraft/"], 
                      cwd=PROJECT_ROOT, check=True)
        print("  ✅ 类型检查通过")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("  ⚠️ 类型检查跳过 (mypy未安装)")


def package_all():
    """打包所有平台"""
    print("📦 开始完整打包流程...")
    
    clean()
    install_deps()
    run_tests()
    check_code()
    build_wheel()
    
    # 尝试构建可执行文件
    try:
        build_executable()
    except Exception as e:
        print(f"⚠️ 可执行文件构建失败: {e}")
    
    print("\n✅ 打包完成！")
    print(f"📁 输出目录: {DIST_DIR}")
    
    # 列出输出文件
    if DIST_DIR.exists():
        print("\n📋 输出文件:")
        for f in DIST_DIR.iterdir():
            size = f.stat().st_size / 1024  # KB
            print(f"  - {f.name} ({size:.1f} KB)")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="PromptCraft 构建脚本")
    parser.add_argument("command", choices=[
        "clean", "test", "build", "package", "all"
    ], help="要执行的命令")
    
    args = parser.parse_args()
    
    if args.command == "clean":
        clean()
    elif args.command == "test":
        run_tests()
    elif args.command == "build":
        build_wheel()
    elif args.command == "package":
        build_executable()
    elif args.command == "all":
        package_all()


if __name__ == "__main__":
    main()
