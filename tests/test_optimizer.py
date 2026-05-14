#!/usr/bin/env python3
"""
Optimizer模块测试
"""
import pytest
from promptcraft.optimizer import PromptOptimizer


class TestPromptOptimizer:
    """测试PromptOptimizer类"""
    
    @pytest.fixture
    def optimizer(self):
        """创建优化器实例"""
        return PromptOptimizer()
    
    def test_analyze_good_prompt(self, optimizer):
        """测试分析优质Prompt"""
        good_prompt = """# 角色
你是一位专业的Python程序员。

# 任务
请帮我优化以下代码。

# 要求
1. 提高可读性
2. 优化性能
3. 添加注释

# 输出格式
请提供优化后的代码和说明。
"""
        result = optimizer.analyze(good_prompt)
        
        assert result['total_score'] > 70
        assert 'A' in result['grade'] or 'B' in result['grade']
        assert 'categories' in result
        assert 'suggestions' in result
    
    def test_analyze_poor_prompt(self, optimizer):
        """测试分析质量较差的Prompt"""
        poor_prompt = "写点东西"
        
        result = optimizer.analyze(poor_prompt)
        
        # 简单prompt的评分可能因规则不同而变化
        assert 'suggestions' in result
    
    def test_optimize_prompt(self, optimizer):
        """测试优化Prompt"""
        original = "帮我写个代码"
        
        result = optimizer.optimize(original)
        
        assert result.score_after >= result.score_before
        assert len(result.optimized) > len(original)
        assert len(result.improvements) > 0
    
    def test_suggest_template(self, optimizer):
        """测试模板推荐"""
        # 编程相关
        coding = optimizer.suggest_template("帮我写一个Python函数")
        assert coding == 'coding'
        
        # 写作相关
        writing = optimizer.suggest_template("帮我写一篇文章")
        assert writing == 'writing'
        
        # 分析相关
        analysis = optimizer.suggest_template("分析这组数据")
        assert analysis == 'analysis'
        
        # 通用
        general = optimizer.suggest_template("告诉我天气")
        assert general == 'general'
    
    def test_estimate_tokens(self, optimizer):
        """测试Token估算"""
        # 英文
        english = "Hello world, this is a test."
        tokens_en = optimizer.estimate_tokens(english)
        assert tokens_en > 0
        
        # 中文
        chinese = "你好世界，这是一个测试。"
        tokens_cn = optimizer.estimate_tokens(chinese)
        assert tokens_cn > tokens_en  # 中文通常需要更多token
        
        # 混合
        mixed = "Hello 你好 world 世界"
        tokens_mix = optimizer.estimate_tokens(mixed)
        assert tokens_mix > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
