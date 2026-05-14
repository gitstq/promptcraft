#!/usr/bin/env python3
"""
Prompt优化引擎
提供Prompt质量分析和自动优化功能
"""
import re
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass


@dataclass
class OptimizationResult:
    """优化结果"""
    original: str
    optimized: str
    score_before: float
    score_after: float
    improvements: List[str]


class PromptOptimizer:
    """Prompt优化器"""
    
    # 优化规则
    RULES = {
        'clarity': {
            'name': '清晰度',
            'weight': 0.25,
            'checks': [
                ('模糊词汇', [
                    r'\b(一些东西|某些|有点|可能|大概|也许)\b',
                    r'\b(something|somewhat|maybe|probably|kind of)\b'
                ]),
                ('指令不明确', [
                    r'^(?!.*(?:请|请|Please|Can you)).*$'
                ])
            ]
        },
        'structure': {
            'name': '结构化',
            'weight': 0.25,
            'checks': [
                ('缺少分段', [
                    r'^[^\n]{200,}$'  # 超过200字符无换行
                ]),
                ('缺少列表', [
                    r'(?<!\d\.)[^\n]{100,}(?:和|以及|,|;)'  # 长句中使用连接词而非列表
                ])
            ]
        },
        'context': {
            'name': '上下文',
            'weight': 0.20,
            'checks': [
                ('缺少背景', [
                    r'^(?!.*(?:作为|扮演|你是|假设|背景|context|as a|you are)).*$'
                ]),
                ('缺少输出格式', [
                    r'^(?!.*(?:格式|输出|返回|format|output|return)).*$'
                ])
            ]
        },
        'specificity': {
            'name': '具体性',
            'weight': 0.15,
            'checks': [
                ('缺少示例', [
                    r'^(?!.*(?:例如|比如|示例|example|e\.g\.|for example)).*$'
                ]),
                ('缺少约束', [
                    r'^(?!.*(?:限制|约束|不超过|至少|maximum|minimum|limit)).*$'
                ])
            ]
        },
        'length': {
            'name': '长度适中',
            'weight': 0.15,
            'checks': [
                ('过短', [
                    r'^.{0,20}$'
                ]),
                ('过长', [
                    r'^.{2000,}$'
                ])
            ]
        }
    }
    
    # 优化模板
    TEMPLATES = {
        'general': """# 角色
{role}

# 任务
{task}

# 要求
{requirements}

# 输出格式
{format}

# 示例
{example}
""",
        'coding': """# 编程任务
{task}

## 技术栈
{tech_stack}

## 代码要求
{requirements}

## 输入
{input_data}

## 期望输出
{expected_output}
""",
        'writing': """# 写作任务
{task}

## 风格
{style}

## 目标读者
{audience}

## 要求
{requirements}

## 参考
{reference}
""",
        'analysis': """# 分析任务
{task}

## 数据
{data}

## 分析方法
{method}

## 输出要求
{output_requirements}
"""
    }
    
    def analyze(self, prompt: str) -> Dict[str, Any]:
        """
        分析Prompt质量
        
        Returns:
            包含各项得分和建议的字典
        """
        results = {}
        total_score = 0
        suggestions = []
        
        for category, config in self.RULES.items():
            category_score = 100
            category_issues = []
            
            for issue_name, patterns in config['checks']:
                for pattern in patterns:
                    if re.search(pattern, prompt, re.IGNORECASE):
                        category_score -= 20
                        category_issues.append(issue_name)
                        break
            
            category_score = max(0, category_score)
            results[category] = {
                'name': config['name'],
                'score': category_score,
                'weight': config['weight'],
                'issues': list(set(category_issues))
            }
            
            total_score += category_score * config['weight']
            
            if category_issues:
                suggestions.append(f"【{config['name']}】{', '.join(set(category_issues))}")
        
        return {
            'total_score': round(total_score, 1),
            'categories': results,
            'suggestions': suggestions,
            'grade': self._get_grade(total_score)
        }
    
    def optimize(self, prompt: str, prompt_type: str = 'general') -> OptimizationResult:
        """
        优化Prompt
        
        Args:
            prompt: 原始Prompt
            prompt_type: Prompt类型 (general/coding/writing/analysis)
        """
        # 分析原始Prompt
        analysis = self.analyze(prompt)
        score_before = analysis['total_score']
        
        # 应用优化规则
        optimized = prompt
        improvements = []
        
        # 1. 清理多余空格和换行
        optimized = self._clean_whitespace(optimized)
        
        # 2. 添加结构标记
        if prompt_type == 'general':
            optimized = self._add_structure_markers(optimized)
        
        # 3. 优化模糊词汇
        optimized, clarity_improvements = self._improve_clarity(optimized)
        improvements.extend(clarity_improvements)
        
        # 4. 添加缺失的上下文
        optimized, context_improvements = self._add_context(optimized)
        improvements.extend(context_improvements)
        
        # 5. 格式化列表
        optimized = self._format_lists(optimized)
        
        # 重新分析
        new_analysis = self.analyze(optimized)
        score_after = new_analysis['total_score']
        
        # 如果优化后分数反而降低，则返回原文
        if score_after < score_before:
            return OptimizationResult(
                original=prompt,
                optimized=prompt,
                score_before=score_before,
                score_after=score_before,
                improvements=["当前Prompt已较优化，无需修改"]
            )
        
        return OptimizationResult(
            original=prompt,
            optimized=optimized,
            score_before=score_before,
            score_after=score_after,
            improvements=improvements or ["已优化格式和结构"]
        )
    
    def _clean_whitespace(self, text: str) -> str:
        """清理空白字符"""
        # 移除行尾空格
        lines = [line.rstrip() for line in text.split('\n')]
        # 合并多个空行
        result = []
        prev_empty = False
        for line in lines:
            is_empty = not line.strip()
            if is_empty and prev_empty:
                continue
            result.append(line)
            prev_empty = is_empty
        return '\n'.join(result).strip()
    
    def _add_structure_markers(self, text: str) -> str:
        """添加结构标记"""
        # 如果已经有结构标记，跳过
        if any(marker in text for marker in ['# ', '## ', '### ']):
            return text
        
        # 检测内容类型并添加适当结构
        lines = text.split('\n')
        structured = []
        
        for line in lines:
            stripped = line.strip()
            # 检测可能的标题
            if stripped.endswith(':') or stripped.endswith('：'):
                structured.append(f"## {stripped[:-1]}")
            # 检测列表项
            elif re.match(r'^[\d\-\*]\.?\s', stripped):
                structured.append(line)
            else:
                structured.append(line)
        
        return '\n'.join(structured)
    
    def _improve_clarity(self, text: str) -> Tuple[str, List[str]]:
        """改进清晰度"""
        improvements = []
        
        # 替换模糊词汇
        replacements = {
            r'\b一些东西\b': '具体内容',
            r'\b某些\b': '特定的',
            r'\b有点\b': '在一定程度上',
            r'\bsomething\b': 'specific details',
            r'\bsomewhat\b': 'to some extent',
            r'\bkind of\b': 'specifically',
        }
        
        for pattern, replacement in replacements.items():
            if re.search(pattern, text, re.IGNORECASE):
                text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
                improvements.append(f"替换模糊词汇: '{pattern}' → '{replacement}'")
        
        return text, improvements
    
    def _add_context(self, text: str) -> Tuple[str, List[str]]:
        """添加上下文"""
        improvements = []
        
        # 如果没有角色定义，添加一个通用的
        if not re.search(r'(?:作为|扮演|你是|you are|as a)', text, re.IGNORECASE):
            if text.startswith('#'):
                # 已有标题，在第二行添加
                lines = text.split('\n')
                lines.insert(1, "\n请作为专业助手，帮助我完成以下任务。")
                text = '\n'.join(lines)
            else:
                text = "请作为专业助手，帮助我完成以下任务。\n\n" + text
            improvements.append("添加角色定义以明确上下文")
        
        # 如果没有输出格式要求，添加提示
        if not re.search(r'(?:格式|输出|format|output)', text, re.IGNORECASE):
            text += "\n\n请提供清晰、结构化的回答。"
            improvements.append("添加输出格式要求")
        
        return text, improvements
    
    def _format_lists(self, text: str) -> str:
        """格式化列表"""
        lines = text.split('\n')
        result = []
        
        for line in lines:
            # 将长句中的"和"转换为列表项
            if '和' in line and len(line) > 50 and not line.strip().startswith(('-', '*', '1.', '2.')):
                parts = re.split(r'[,，、]\s*(?![^（(]*[）)])', line)
                if len(parts) > 2:
                    result.append(parts[0])
                    for part in parts[1:]:
                        if part.strip():
                            result.append(f"- {part.strip()}")
                else:
                    result.append(line)
            else:
                result.append(line)
        
        return '\n'.join(result)
    
    def _get_grade(self, score: float) -> str:
        """获取等级评价"""
        if score >= 90:
            return "A+ (优秀)"
        elif score >= 80:
            return "A (良好)"
        elif score >= 70:
            return "B (中等)"
        elif score >= 60:
            return "C (及格)"
        else:
            return "D (需改进)"
    
    def suggest_template(self, prompt: str) -> str:
        """根据内容推荐模板"""
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ['code', '编程', 'function', '函数', 'class', '代码']):
            return 'coding'
        elif any(word in prompt_lower for word in ['write', '文章', 'essay', 'blog', '写作', '写']):
            return 'writing'
        elif any(word in prompt_lower for word in ['analyze', '分析', 'data', '数据', '统计']):
            return 'analysis'
        else:
            return 'general'
    
    def estimate_tokens(self, text: str, model: str = 'general') -> int:
        """
        估算Token数量（粗略估计）
        
        Args:
            text: 文本内容
            model: 模型类型
        """
        # 简单的估算：英文约1词=1.3 tokens，中文约1字=2 tokens
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        english_words = len(re.findall(r'[a-zA-Z]+', text))
        
        # 根据模型调整
        multipliers = {
            'gpt-4': 1.0,
            'gpt-3.5': 1.0,
            'claude': 1.0,
            'general': 1.2
        }
        
        multiplier = multipliers.get(model, 1.2)
        estimated = int((chinese_chars * 2 + english_words * 1.3) * multiplier)
        
        return estimated
