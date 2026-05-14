#!/usr/bin/env python3
"""
Core模块测试
"""
import pytest
import tempfile
import os
from promptcraft.core import PromptManager


class TestPromptManager:
    """测试PromptManager类"""
    
    @pytest.fixture
    def manager(self):
        """创建临时管理器实例"""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            db_path = f.name
        manager = PromptManager(db_path)
        yield manager
        # 清理
        os.unlink(db_path)
    
    def test_create_and_get(self, manager):
        """测试创建和获取Prompt"""
        prompt_id = manager.create(
            title="测试标题",
            content="测试内容 {{name}}",
            description="测试描述",
            category="test",
            tags=["tag1", "tag2"]
        )
        
        assert prompt_id > 0
        
        prompt = manager.get(prompt_id)
        assert prompt['title'] == "测试标题"
        assert prompt['content'] == "测试内容 {{name}}"
        assert 'name' in prompt['variables']
    
    def test_use_prompt(self, manager):
        """测试使用Prompt"""
        prompt_id = manager.create(
            title="问候",
            content="你好，{{name}}！今天是{{day}}。"
        )
        
        result = manager.use(prompt_id, {
            'name': '张三',
            'day': '星期一'
        })
        
        assert '张三' in result
        assert '星期一' in result
        assert '{{' not in result
    
    def test_toggle_favorite(self, manager):
        """测试收藏功能"""
        prompt_id = manager.create(title="测试", content="内容")
        
        # 初始状态
        prompt = manager.get(prompt_id)
        assert prompt['is_favorite'] is False
        
        # 切换收藏
        manager.toggle_favorite(prompt_id)
        prompt = manager.get(prompt_id)
        assert prompt['is_favorite'] is True
        
        # 再次切换
        manager.toggle_favorite(prompt_id)
        prompt = manager.get(prompt_id)
        assert prompt['is_favorite'] is False
    
    def test_duplicate(self, manager):
        """测试复制Prompt"""
        original_id = manager.create(
            title="原始",
            content="内容",
            category="test"
        )
        
        new_id = manager.duplicate(original_id)
        
        original = manager.get(original_id)
        new_prompt = manager.get(new_id)
        
        assert new_prompt['title'] == "原始 (复制)"
        assert new_prompt['content'] == original['content']
        assert new_prompt['category'] == original['category']
        assert new_prompt['is_favorite'] is False
    
    def test_extract_variables(self, manager):
        """测试变量提取"""
        content = "你好 {{name}}，你的年龄是 {{age}} 岁。"
        variables = manager._extract_variables(content)
        
        assert 'name' in variables
        assert 'age' in variables
        assert len(variables) == 2


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
