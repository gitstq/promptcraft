#!/usr/bin/env python3
"""
Storage模块测试
"""
import pytest
import tempfile
import os
from promptcraft.storage import Storage


class TestStorage:
    """测试Storage类"""
    
    @pytest.fixture
    def storage(self):
        """创建临时存储实例"""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            db_path = f.name
        storage = Storage(db_path)
        yield storage
        # 清理
        os.unlink(db_path)
    
    def test_create_prompt(self, storage):
        """测试创建Prompt"""
        prompt_data = {
            'title': '测试Prompt',
            'content': '这是一个测试内容',
            'description': '测试描述',
            'category': 'test',
            'tags': ['test', 'demo'],
            'variables': ['var1', 'var2'],
            'model_type': 'gpt-4',
            'is_favorite': True
        }
        
        prompt_id = storage.create_prompt(prompt_data)
        assert prompt_id > 0
        
        # 验证创建成功
        prompt = storage.get_prompt(prompt_id)
        assert prompt is not None
        assert prompt['title'] == '测试Prompt'
        assert prompt['content'] == '这是一个测试内容'
        assert prompt['category'] == 'test'
        assert prompt['is_favorite'] is True
        assert 'test' in prompt['tags']
    
    def test_list_prompts(self, storage):
        """测试列出Prompts"""
        # 创建测试数据
        for i in range(3):
            storage.create_prompt({
                'title': f'Prompt {i}',
                'content': f'Content {i}',
                'category': 'test' if i < 2 else 'other',
                'tags': ['tag1'] if i == 0 else ['tag2']
            })
        
        # 测试列出所有
        all_prompts = storage.list_prompts()
        assert len(all_prompts) == 3
        
        # 测试按分类筛选
        test_prompts = storage.list_prompts(category='test')
        assert len(test_prompts) == 2
        
        # 测试按标签筛选
        tag1_prompts = storage.list_prompts(tag='tag1')
        assert len(tag1_prompts) == 1
    
    def test_update_prompt(self, storage):
        """测试更新Prompt"""
        prompt_id = storage.create_prompt({
            'title': '原始标题',
            'content': '原始内容'
        })
        
        # 更新
        success = storage.update_prompt(prompt_id, {
            'title': '新标题',
            'content': '新内容'
        })
        assert success is True
        
        # 验证更新
        prompt = storage.get_prompt(prompt_id)
        assert prompt['title'] == '新标题'
        assert prompt['content'] == '新内容'
    
    def test_delete_prompt(self, storage):
        """测试删除Prompt"""
        prompt_id = storage.create_prompt({
            'title': '待删除',
            'content': '内容'
        })
        
        # 删除
        success = storage.delete_prompt(prompt_id)
        assert success is True
        
        # 验证删除
        prompt = storage.get_prompt(prompt_id)
        assert prompt is None
    
    def test_get_stats(self, storage):
        """测试统计信息"""
        # 创建测试数据
        storage.create_prompt({'title': 'P1', 'content': 'C1', 'is_favorite': True})
        storage.create_prompt({'title': 'P2', 'content': 'C2', 'is_favorite': False})
        
        stats = storage.get_stats()
        assert stats['total_prompts'] == 2
        assert stats['favorite_count'] == 1
        assert stats['category_count'] > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
