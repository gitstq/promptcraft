#!/usr/bin/env python3
"""
PromptCraft - 轻量级AI Prompt优化与管理工具
安装脚本
"""
from setuptools import setup, find_packages
from pathlib import Path

# 读取README
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

# 读取requirements
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_path.exists():
    requirements = [
        line.strip() 
        for line in requirements_path.read_text().splitlines() 
        if line.strip() and not line.startswith('#')
    ]

setup(
    name="promptcraft",
    version="1.0.0",
    author="PromptCraft Team",
    author_email="promptcraft@example.com",
    description="轻量级AI Prompt优化与管理工具 / Lightweight AI Prompt Optimization & Management Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitstq/promptcraft",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "promptcraft=promptcraft.cli:main",
            "pc=promptcraft.cli:main",
        ],
    },
    keywords="prompt ai llm claude gpt management optimization cli",
    project_urls={
        "Bug Reports": "https://github.com/gitstq/promptcraft/issues",
        "Source": "https://github.com/gitstq/promptcraft",
    },
)
