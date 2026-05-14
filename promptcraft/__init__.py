"""
PromptCraft - 轻量级AI Prompt优化与管理工具
Lightweight AI Prompt Optimization & Management Tool

版本: 1.0.0
作者: PromptCraft Team
许可证: MIT
"""

__version__ = "1.0.0"
__author__ = "PromptCraft Team"
__license__ = "MIT"

from .core import PromptManager
from .optimizer import PromptOptimizer
from .storage import Storage

__all__ = ["PromptManager", "PromptOptimizer", "Storage"]
