#!/usr/bin/env python3
"""
核心业务逻辑 - Prompt管理器
"""
import re
import json
from typing import List, Dict, Optional, Any
from datetime import datetime

from .storage import Storage
from .optimizer import PromptOptimizer, OptimizationResult


class PromptManager:
    """Prompt管理器 - 提供完整的Prompt管理功能"""
    
    def __init__(self, db_path: Optional[str] = None):
        """
        初始化Prompt管理器
        
        Args:
            db_path: 数据库路径，默认使用 ~/.promptcraft/prompts.db
        """
        self.storage = Storage(db_path)
        self.optimizer = PromptOptimizer()
    
    # ==================== CRUD 操作 ====================
    
    def create(self, title: str, content: str, **kwargs) -> int:
        """
        创建新Prompt
        
        Args:
            title: 标题
            content: 内容
            **kwargs: 可选参数 (description, category, tags, variables, model_type, is_favorite)
        
        Returns:
            新创建的Prompt ID
        """
        prompt_data = {
            'title': title,
            'content': content,
            'description': kwargs.get('description', ''),
            'category': kwargs.get('category', 'general'),
            'tags': kwargs.get('tags', []),
            'variables': kwargs.get('variables', []),
            'model_type': kwargs.get('model_type', 'general'),
            'is_favorite': kwargs.get('is_favorite', False)
        }
        
        # 自动提取变量
        if not prompt_data['variables']:
            prompt_data['variables'] = self._extract_variables(content)
        
        return self.storage.create_prompt(prompt_data)
    
    def get(self, prompt_id: int) -> Optional[Dict[str, Any]]:
        """获取Prompt详情"""
        return self.storage.get_prompt(prompt_id)
    
    def list(self, **filters) -> List[Dict[str, Any]]:
        """
        列出Prompts
        
        Args:
            category: 分类筛选
            tag: 标签筛选
            favorite_only: 仅显示收藏
            search: 搜索关键词
        """
        return self.storage.list_prompts(**filters)
    
    def update(self, prompt_id: int, **kwargs) -> bool:
        """更新Prompt"""
        return self.storage.update_prompt(prompt_id, kwargs)
    
    def delete(self, prompt_id: int) -> bool:
        """删除Prompt"""
        return self.storage.delete_prompt(prompt_id)
    
    # ==================== 收藏功能 ====================
    
    def toggle_favorite(self, prompt_id: int) -> bool:
        """切换收藏状态"""
        prompt = self.get(prompt_id)
        if prompt:
            new_status = not prompt.get('is_favorite', False)
            return self.update(prompt_id, is_favorite=new_status)
        return False
    
    def get_favorites(self) -> List[Dict[str, Any]]:
        """获取收藏列表"""
        return self.storage.list_prompts(favorite_only=True)
    
    # ==================== 使用功能 ====================
    
    def use(self, prompt_id: int, variables: Optional[Dict[str, str]] = None) -> str:
        """
        使用Prompt，替换变量
        
        Args:
            prompt_id: Prompt ID
            variables: 变量值字典
        
        Returns:
            替换变量后的最终Prompt
        """
        prompt = self.get(prompt_id)
        if not prompt:
            raise ValueError(f"Prompt ID {prompt_id} 不存在")
        
        content = prompt['content']
        
        # 替换变量
        if variables:
            for var_name, var_value in variables.items():
                content = content.replace(f"{{{{{var_name}}}}}", str(var_value))
        
        # 增加使用计数
        self.storage.increment_use_count(prompt_id)
        
        return content
    
    def preview(self, prompt_id: int, variables: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        预览Prompt（不增加使用计数）
        
        Returns:
            包含原始内容、处理后内容、缺失变量等信息的字典
        """
        prompt = self.get(prompt_id)
        if not prompt:
            raise ValueError(f"Prompt ID {prompt_id} 不存在")
        
        content = prompt['content']
        original_content = content
        
        # 替换变量
        missing_vars = []
        if variables:
            for var_name, var_value in variables.items():
                content = content.replace(f"{{{{{var_name}}}}}", str(var_value))
        
        # 检查未替换的变量
        remaining_vars = self._extract_variables(content)
        missing_vars = [v for v in remaining_vars if f"{{{{{v}}}}}" in content]
        
        return {
            'title': prompt['title'],
            'original': original_content,
            'processed': content,
            'variables_used': variables or {},
            'variables_missing': missing_vars,
            'model_type': prompt['model_type'],
            'category': prompt['category']
        }
    
    # ==================== 优化功能 ====================
    
    def analyze(self, prompt_id: int) -> Dict[str, Any]:
        """分析Prompt质量"""
        prompt = self.get(prompt_id)
        if not prompt:
            raise ValueError(f"Prompt ID {prompt_id} 不存在")
        
        return self.optimizer.analyze(prompt['content'])
    
    def optimize(self, prompt_id: int, save: bool = False) -> OptimizationResult:
        """
        优化Prompt
        
        Args:
            prompt_id: Prompt ID
            save: 是否保存优化结果
        """
        prompt = self.get(prompt_id)
        if not prompt:
            raise ValueError(f"Prompt ID {prompt_id} 不存在")
        
        result = self.optimizer.optimize(prompt['content'], prompt['model_type'])
        
        # 保存优化历史
        self.storage.add_optimization_history({
            'prompt_id': prompt_id,
            'original_content': result.original,
            'optimized_content': result.optimized,
            'improvements': result.improvements,
            'score_before': result.score_before,
            'score_after': result.score_after
        })
        
        # 如果要求保存，更新Prompt内容
        if save and result.score_after > result.score_before:
            self.update(prompt_id, content=result.optimized)
        
        return result
    
    def get_optimization_history(self, prompt_id: int) -> List[Dict[str, Any]]:
        """获取优化历史"""
        return self.storage.get_optimization_history(prompt_id)
    
    # ==================== 导入导出 ====================
    
    def export(self, format_type: str = 'json', file_path: Optional[str] = None) -> str:
        """
        导出Prompts
        
        Args:
            format_type: 'json' 或 'markdown'
            file_path: 导出文件路径，为None则返回内容
        """
        content = self.storage.export_data(format_type)
        
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return content
    
    def import_from_file(self, file_path: str, format_type: str = 'json'):
        """从文件导入"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.storage.import_data(content, format_type)
    
    def import_from_string(self, content: str, format_type: str = 'json'):
        """从字符串导入"""
        self.storage.import_data(content, format_type)
    
    # ==================== 统计信息 ====================
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return self.storage.get_stats()
    
    def get_categories(self) -> List[Dict[str, Any]]:
        """获取分类列表"""
        return self.storage.get_categories()
    
    # ==================== 辅助方法 ====================
    
    def _extract_variables(self, content: str) -> List[str]:
        """从内容中提取变量 {{variable}}"""
        pattern = r'\{\{(\w+)\}\}'
        matches = re.findall(pattern, content)
        return list(set(matches))  # 去重
    
    def suggest_tags(self, title: str, content: str) -> List[str]:
        """根据内容推荐标签"""
        text = (title + " " + content).lower()
        suggestions = []
        
        tag_keywords = {
            '编程': ['code', 'programming', '函数', 'class', 'api', 'debug'],
            '写作': ['write', 'essay', 'article', 'blog', 'content', '文案'],
            '翻译': ['translate', 'translation', 'english', 'chinese', '语言'],
            '分析': ['analyze', 'analysis', 'data', '统计', '报告'],
            '创意': ['creative', 'idea', 'brainstorm', '创意', '灵感'],
            '学习': ['learn', 'study', 'tutorial', '学习', '教程'],
            '商业': ['business', 'marketing', '销售', '市场', '客户'],
        }
        
        for tag, keywords in tag_keywords.items():
            if any(kw in text for kw in keywords):
                suggestions.append(tag)
        
        return suggestions[:3]  # 最多返回3个建议
    
    def duplicate(self, prompt_id: int, new_title: Optional[str] = None) -> int:
        """复制Prompt"""
        prompt = self.get(prompt_id)
        if not prompt:
            raise ValueError(f"Prompt ID {prompt_id} 不存在")
        
        prompt_data = {
            'title': new_title or f"{prompt['title']} (复制)",
            'content': prompt['content'],
            'description': prompt.get('description', ''),
            'category': prompt['category'],
            'tags': prompt.get('tags', []),
            'variables': prompt.get('variables', []),
            'model_type': prompt['model_type'],
            'is_favorite': False
        }
        
        return self.storage.create_prompt(prompt_data)
    
    def search_by_content(self, query: str) -> List[Dict[str, Any]]:
        """全文搜索"""
        return self.storage.list_prompts(search=query)
    
    def get_popular(self, limit: int = 10) -> List[Dict[str, Any]]:
        """获取最常用的Prompts"""
        all_prompts = self.storage.list_prompts()
        sorted_prompts = sorted(all_prompts, key=lambda x: x.get('use_count', 0), reverse=True)
        return sorted_prompts[:limit]
